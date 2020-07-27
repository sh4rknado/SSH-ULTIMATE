
import time
import paramiko

class SSH:

    def __init__(self, host, port):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self.host = host
        self.port = port
        self.banner = None

    def get_banner(self, host, port):
        try:
            self.ssh.connect(hostname=host, port=port, username='invalidinvalidinvalid', password='invalidinvalidinvalid')
        except:
            self.banner = self.ssh.get_transport().remote_version
            self.ssh.close()
            return self.banner

    def connect(self, host, port, user):
      global args
      endtime = 0.0
      p = 'B' * int(args.bytes)
      starttime = time.clock()
      try:
        self.ssh.connect(hostname=host, port=port, username=user, password=p, look_for_keys=False, gss_auth=False, gss_kex=False, gss_deleg_creds=False, gss_host=None, allow_agent=False)
      except:
        endtime = time.clock()
      finally:
        self.ssh.close()
        return endtime - starttime
