import os
import time
import sys
import paramiko
import signal

class DirectoryMonitor:
    def __init__(self, monitored_directory, remote_directory,
                 ssh_server, ssh_username, ssh_password, loop_interval=5,
                 file_filter=lambda x: os.path.splitext(x)[1] ==".pcap"):
        self.monitored_directory = os.path.realpath(monitored_directory)
        self.remote_directory = remote_directory
        self.ssh_server = ssh_server
        self.ssh_username = ssh_username
        self.ssh_password = ssh_password
        self.file_filter = file_filter
        self.loop_interval = loop_interval
        self.break_loop = False
        self.files = []
        

    def loop(self):
        while True:
            if self.break_loop:
                break
            self.update_files()
            time.sleep(self.loop_interval)

    def update_files(self, copy_all=False):
        all_files = os.listdir(self.monitored_directory)
        all_files = filter(self.file_filter, all_files)
        existing = filter(lambda f: f in self.files, all_files)
        new = filter(lambda f: f not in self.files, all_files)
        if new or copy_all:
            for f in existing:
                try:
                    print "writing {} to remote".format(f)
                    self.write_to_remote(f)
                    os.remove(os.path.join(self.monitored_directory, f))
                except Exception as e:
                    new.append(f)
                    print e
            self.files = new

    def write_to_remote(self, f):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.ssh_server, username=self.ssh_username, password=self.ssh_password)
        sftp = ssh.open_sftp()
        sftp.put(os.path.join(self.monitored_directory, f), os.path.join(self.remote_directory, f))
        sftp.close()
        ssh.close()

    def sigint_handler(self):
        self.break_loop = True
        self.update_files(copy_all=True)
        

def main():
    if len(sys.argv) != 6:
        print "Usage: python {} [monitored_directory] [ssh_username] [ssh_server] [remote_directory [ssh_password]".format(sys.argv[0])
        sys.exit()

    monitored_directory = sys.argv[1]
    ssh_username = sys.argv[2]
    ssh_server = sys.argv[3]
    remote_directory = sys.argv[4]
    ssh_password = sys.argv[5]
    print "Monitoring {} to {}@{}:{} using password {}".format(
        monitored_directory, ssh_username, ssh_server, remote_directory, ssh_password)

    monitor = DirectoryMonitor(monitored_directory, remote_directory,
                               ssh_server, ssh_username, ssh_password)
    def sigint_handler(signal, frame):
        monitor.sigint_handler()
        sys.exit()
    signal.signal(signal.SIGINT, sigint_handler)
        
    monitor.loop()


main()
