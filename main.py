
from SSH_ENUM.SSH_ENUM import SSH_ENUM

if __name__ == '__main__':
    ssh_enum = SSH_ENUM('127.0.0.1', '/mnt/data/Hacking/Cracker/PasswordList/SecLists-master/Usernames/xato-net-10-million-usernames.txt', port=22, use_list=True)
    ssh_enum.run()
