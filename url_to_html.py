from urllib.request import urlopen # To open URL provided
import urllib.request # To make the request
from urllib.error import HTTPError
import sys # Keeping for now

class bcolors: # Grabbed from https://stackoverflow.com/questions/287871/how-to-print-colored-text-to-the-terminal
    # These should work on every terminal with python3+
    WARNING = '\033[93m' # Yellow
    FAIL = '\033[91m' # Red
    ENDC = '\033[0m' # Normal
    
class settings():
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0" # Use what user agent you want, new one to be sure
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','User-Agent': user_agent} # header from Google :P
    debug = 0

def get_html(url, *args):
    try:
        if args[0] == "-d" or args[0] == "debug":
            print("Debug is on")
            settings.debug = 1
    except IndexError:
        pass
    req = urllib.request.Request(url,None, settings.headers) # Making the request
    try:
        page = urlopen(req) # "Opening" the url with previous parameters
        html_bytes = page.read() # Reading the page
        html = html_bytes.decode("utf-8") # Decoding to utf-8 to get proper Ä,Ö and Å
    except HTTPError as err: # https://stackoverflow.com/questions/3193060/catch-specific-http-error-in-python
        if err.code == 404:
            print(f"{bcolors.WARNING}HTTP Error 404{bcolors.ENDC}")
            html = False # Just to make sure
            if settings.debug == 1:
                print("404 url:", url) # DEBUG
        elif err.code == 403: # Forbidden
            print(f"{bcolors.WARNING}HTTP Error 403 forbidden, most likely getting rate limited{bcolors.ENDC}")
        else:
            raise
        return err.code # Returns if any error happens
    except Exception:
        print(f"{bcolors.FAIL}Cannot access webpage{bcolors.ENDC}") # If we get timed out or other issues
        # sys.exit(0) # Not sure
    return html # If no errors