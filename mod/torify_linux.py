import requests
import subprocess
import psutil
import time
import sys
from stem import Signal
from stem.control import Controller
from colorama import Fore,init

# initialize color
init()

class TorifyLinux:
    def __init__(self):
        self.tor_proxy_host = '127.0.0.1'
        self.tor_proxy_port = 9050
        self.ip_check = 'https://api.my-ip.io/v2/ip.json'

    def run_command_in_background(self,command, output_file):
        # Run the command in the background and redirect the output to a file
        process = subprocess.Popen(command, shell=True, stdout=open(output_file, 'w'), stderr=subprocess.STDOUT)
        # Return the process object
        return process
    
    def make_tor_request(self,url):
        session = requests.Session()
        session.proxies = {'http': f'socks5://{self.tor_proxy_host}:{self.tor_proxy_port}',
                        'https': f'socks5://{self.tor_proxy_host}:{self.tor_proxy_port}'}

        try:
            response = session.get(url)
            return response.json()['ip']
        except requests.exceptions.RequestException as e:
            return "Error making request"
        
    def killtor(self,process_name):
        try:
            for process in psutil.process_iter(['pid', 'name']):
                if process.info['name'] == process_name:
                    pid = process.info['pid']
                    psutil.Process(pid).terminate()
                    print(f"[{Fore.GREEN}INF{Fore.RESET}] Process with name {process_name} (PID: {pid}) terminated successfully.")
        except Exception as e:
            print(f"[{Fore.RED}ERR{Fore.RESET}] Error terminating process with name {process_name}: {e}")
    
    def renew(self):
        with Controller.from_port(port=9051) as controller:
            controller.authenticate()
            controller.signal(Signal.NEWNYM)
    
    def run(self,times=10):
        # Attempt to get a new IP address
        print(f"[{Fore.GREEN}INF{Fore.RESET}] Time to rotate the ip address is ({times}s)")
        print(f"[{Fore.GREEN}INF{Fore.RESET}] Please run your browser or tools over this proxy => socks5://{self.tor_proxy_host}:{self.tor_proxy_port}")
        print(f"[{Fore.GREEN}INF{Fore.RESET}] Starting new tor...")
        pid = self.run_command_in_background("tor &","log.txt")
        time.sleep(2)
        while True:
            try:
                initial_ip = self.make_tor_request(self.ip_check)
                print(f"[{Fore.GREEN}INF{Fore.RESET}] Initial IP address: {initial_ip}")
                for timesec in range(times):
                    try:
                        print(f"[{Fore.GREEN}INF{Fore.RESET}] {times-timesec}s To renew the ip address ",end="\r")
                        time.sleep(1)
                    except KeyboardInterrupt:
                        self.killtor('tor')
                        sys.exit()
                self.renew()
            except Exception as e:
                print(f"[{Fore.RED}ERR{Fore.RESET}] {e}")
                self.killtor('tor')
                sys.exit()

