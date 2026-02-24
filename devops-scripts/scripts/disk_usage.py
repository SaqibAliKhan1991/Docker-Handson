import psutil
import datetime

def check_disk():
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'[{timestamp}] Disk Usage Report')
    print('-' * 40)

    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            print(f'  Partition:  {partition.mountpoint}')
            print(f'  Total:      {usage.total // 1024**3} GB')
            print(f'  Used:       {usage.used // 1024**3} GB')
            print(f'  Free:       {usage.free // 1024**3} GB')
            print(f'  Usage:      {usage.percent}%')
            if usage.percent > 90:
                print(f'  ALERT: Low disk space on {partition.mountpoint}!')
            print('-' * 40)
        except PermissionError:
            pass

if __name__ == '__main__':
    check_disk()
