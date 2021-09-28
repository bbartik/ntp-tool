from netmiko import ConnectHandler
import argparse
import getpass
import pdb
import sys
import textfsm


# set good ntp servers
NTP1 = "ntp server 129.6.15.28"
NTP2 = "ntp server 129.6.15.29"
NTP_LIST = [NTP1, NTP2]



def update_ntp(device_list, NTP_LIST):
    """ Check for incorrect servers, removes them and update with new """

    for device in device_list:

        node = {
            'device_type': 'cisco_ios',
            'host':   device,
            'username': username,
            'password': password,
        }

        net_connect = ConnectHandler(**node)
        command = "show run | inc ntp server"

        # get current lists of ntp servers and create 2 lists: incorrect and missing
        ntp_lines = net_connect.send_command(command).splitlines()
        incorrect = list(set(ntp_lines)-set(NTP_LIST))
        missing = list(set(NTP_LIST)-set(ntp_lines))
        
        # remove empty strings from lists
        incorrect = list(filter(None, incorrect))

        #pdb.set_trace()
        if len(incorrect) > 0:
            try:
                config_commands = [f"no {i}" for i in incorrect]
                #print(config_commands)
                net_connect.send_config_set(config_commands)
                print(f"{device} has old servers removed")
            except:
                print(f"{device} did not have old servers or there was a problem removing them")

        # add new servers
        try:
            config_commands = [f"{m}" for m in missing]
            #print(config_commands)
            net_connect.send_config_set(config_commands)
            print(f"{device} has new servers configured")
        except:
            print(f"{device} already had new servers configured")        


def ntp_sync_check(device_list):
    """ Check if NTP is synced """

    for device in device_list:

        node = {
            'device_type': 'cisco_ios',
            'host':   device,
            'username': username,
            'password': password,
        }

        net_connect = ConnectHandler(**node)
        command = "show ntp status"

        #output = net_connect.send_command(command).splitlines()
        #output = list(filter(None, output))
        output = net_connect.send_command(command)

        template = open("cisco_ios_show_ntp_status.textfsm")
        re_table = textfsm.TextFSM(template)
        data = re_table.ParseText(output)

        try:
            print(f"{device} is synchronized to {data[0][2]}")
        except:
            print(f"{device} is NOT syncronized")

        

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='NTP Updater for Cisco IOS')
    parser.add_argument('-u', '--update', action="store_true", help='Update NTP')
    parser.add_argument('-c', '--check', action="store_true", help='Check if NTP is Synced')
    args = parser.parse_args()

    username = input("\nEnter username: ")
    password = getpass.getpass("Enter password: ")

    with open('devices') as f:
        device_list = [line.rstrip('\n') for line in f]
    
    if args.update == True:
        print("Updating NTP...")
        update_ntp(device_list, NTP_LIST)

    if args.check == True:
        print("Running NTP sync check...")
        ntp_sync_check(device_list)
