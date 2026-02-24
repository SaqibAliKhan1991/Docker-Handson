import psutil
import datetime

def check_system():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    print(f'[{timestamp}] System Health Check')
    print(f'  CPU Usage:    {cpu}%')
    print(f'  Memory Used:  {memory.percent}% ({memory.used // 1024**2} MB used)')
    print(f'  Disk Used:    {disk.percent}%')

    if cpu > 80:
        print('  ALERT: High CPU usage!')
    if memory.percent > 85:
        print('  ALERT: High memory usage!')
    if disk.percent > 90:
        print('  ALERT: Low disk space!')

if __name__ == '__main__':
    check_system()
