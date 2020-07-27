
import argparse
from SSH_ENUM.SSH_ENUM import SSH_ENUM

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip", help="ip address", type=str)
    parser.add_argument("-u", "--username", help="username or user list", type=str)
    parser.add_argument("-p", "--port", help="port", type=int, default=22)
    args = parser.parse_args()

    ip = None
    username = None
    port = args.port

    if args.ip:
        ip = args.ip
    if args.username:
        username = args.username

    ssh_enum = SSH_ENUM(ip, username, port=port, use_list=True)
    ssh_enum.run()
