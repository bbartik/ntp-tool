# NTP Update and Validator tool

## Usage

```
ntp_validator$ python ntp_updater.py -h
usage: ntp_updater.py [-h] [-u] [-c]

NTP Updater for Cisco IOS

optional arguments:
  -h, --help    show this help message and exit
  -u, --update  Update NTP
  -c, --check   Check if NTP is Synced

automation/ntp_validator$ python ntp_updater.py -c

Enter username: admin
Enter password: 
Running NTP sync check...
172.28.87.44 is synchronized to 129.6.15.28
172.28.87.45 is NOT syncronized

$ python ntp_updater.py -u

Enter username: admin
Enter password: 
Updating NTP...
172.28.87.44 has new servers configured
172.28.87.45 has new servers configured

$ python ntp_updater.py -c

Enter username: admin
Enter password: 
Running NTP sync check...
172.28.87.44 is synchronized to 129.6.15.28
172.28.87.45 is synchronized to 129.6.15.28
```

