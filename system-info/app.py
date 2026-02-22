import platform
import datetime

print("=" * 40)
print("   SYSTEM INFO - Docker Container")
print("=" * 40)
print(f"Date/Time : {datetime.datetime.now()}")
print(f"OS        : {platform.system()}")
print(f"OS Version: {platform.version()}")
print(f"Machine   : {platform.machine()}")
print(f"Python    : {platform.python_version()}")
print("=" * 40)
print(f"Developer : Saqib Ali Khan - Berlin")
