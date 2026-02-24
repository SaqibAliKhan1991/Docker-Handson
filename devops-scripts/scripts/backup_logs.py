import os
import shutil
import datetime

def backup_logs():
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    backup_dir = f'/tmp/backup_{timestamp}'
    os.makedirs(backup_dir, exist_ok=True)

    log_files = [
        '/var/log/syslog',
        '/var/log/auth.log',
        '/var/log/kern.log'
    ]

    print(f'[{timestamp}] Log Backup Started')
    print(f'  Backup folder: {backup_dir}')
    print('-' * 40)

    backed_up = 0
    for log_file in log_files:
        if os.path.exists(log_file):
            shutil.copy2(log_file, backup_dir)
            print(f'  Backed up: {log_file}')
            backed_up += 1
        else:
            print(f'  Skipped:   {log_file} (not found)')

    print('-' * 40)
    print(f'  Total backed up: {backed_up} files')
    print(f'  Backup complete!')

if __name__ == '__main__':
    backup_logs()
