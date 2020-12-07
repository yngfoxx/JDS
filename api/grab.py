# SCRIPT BY OSUNRINDE STEPHEN ADEBAYO
import time, request, argparse
from pySmartDL import SmartDL

# accepts argument from command e.g "python grab.py -u https://www.filedomain.com/file.zip"
parser = argparse.ArgumentParser(prog='grab', description='download files from internet using Python')

# accept URL with "-u" or "--url"
parser.add_argument('-u', '--url', type=str, required=True, help='The URL of the target file')
parser.add_argument('-i', '--id', type=str, help='The user/session id for further processing')

# assign arguments to object
args = parser.parse_args()

# Assign arguments in object to variables
URL = args.url
USER_ID = args.id


# FILE DOWNLOAD MANAGER
url = "https://www.exodusleague.com/media/img/logo/exodusleague.png"
dest = "C:/Users/YoungFox/Downloads/"

obj = SmartDL(url, dest)

obj.start() 

# [*] 0.23 Mb / 0.37 Mb @ 88.00Kb/s [##########——–] [60%, 2s left]

path = obj.get_dest()