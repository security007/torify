import sys
from colorama import Fore,init
from mod.torify_linux import TorifyLinux
from mod.torify_win import TorifyWin

# initialize color
init()


if __name__ == "__main__":
    platform = sys.platform.lower()
    banner = f"""{Fore.BLUE}
___________          .__  _____       
\__    ___/__________|__|/ ____\__.__. 
  |    | /  _ \_  __ \  \   __<   |  |
  |    |(  <_> )  | \/  ||  |  \___  |
  |____| \____/|__|  |__||__|  / ____| ({platform})
                               \/  
  v1.1 - Security007  
  Auto Rotate TOR IP Address
  {Fore.RESET}
"""
    print(banner)
    if platform == 'linux':
        app = TorifyLinux()
    elif 'win' in platform:
        app = TorifyWin()
    try:
        app.run(times=int(sys.argv[1]))
    except IndexError:
        app.run()