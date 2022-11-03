import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import paramiko


class Watcher:
    DIRECTORY_TO_WATCH = "/home/ubuntu/Desktop/Logs"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print ("Error")
           
        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            print ("Received modified event - %s." % event.src_path)
            update()

def update():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='xx.xx.xx.xx', username='xxxx', password='xxxx')
    sftp = ssh.open_sftp()
    sftp.put('/home/ubuntu/Desktop/Logs/xx.log', '/home/ubuntu/Desktop/Logs/xx.log')
    sftp.close()
    ssh.close

if __name__ == '__main__':	
    w = Watcher()
    w.run()
