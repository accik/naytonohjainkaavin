import sys
from urllib.request import urlopen # To open URL provided
import urllib.request # To make the request
from urllib.error import HTTPError
from bs4 import BeautifulSoup # To properly manage html tags later
import re # For regex operations
import time # For time
import progressbar # Local import
import findlinefromfile # local import

class BASE():
    version = 2.23
    version_name = "TESTING:BETA"
    datafile = "example_datafiles/full_list.txt" # This the default file, change to your <datafile>.txt
    timelimit = 3 # Default value
    debug = 0 # To monitor debug status, only set here to force

class LENGHTS(): # Global class to track file lengths
    total_url_list_len = 0
    vk_n = 0
    j_n = 0
    pro_n = 0

class bcolors: # Grabbed from https://stackoverflow.com/questions/287871/how-to-print-colored-text-to-the-terminal
    # These should work on every terminal
    HEADER = '\033[95m' # Violet
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m' # Yellow
    FAIL = '\033[91m' # Red
    ENDC = '\033[0m' # Normal
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def importer(): # Loading URL from a file specified
    filename = BASE.datafile
    vk_url_list = [] # Making the lists
    j_url_list = []
    pros_list = []
    try:
        f = open(filename, "r", encoding='utf-8') # Opening the file with read
    except FileNotFoundError:
        print(f"{bcolors.FAIL}File not found{bcolors.ENDC}")
        sys.exit(0)
    except Exception:
        print(f"{bcolors.FAIL}Error opening{bcolors.ENDC}")
        sys.exit(0)
    while True:
        try:
            row = f.readline() # Reading one line from the file
        except Exception:
            print(f"{bcolors.FAIL}Error reading line from the file{bcolors.ENDC}")
            sys.exit(0)
        row = row.rstrip()
        if len(row) == 0:
            break
        elif row.startswith("https://www.jimms.fi/"): # Checking if the line matches what we want
            j_url_list.append(row)
            LENGHTS.j_n += 1
        elif row.startswith("https://www.verkkokauppa.com"):
            vk_url_list.append(row)
            LENGHTS.vk_n += 1
        elif row.startswith("https://www.proshop.fi/"):
            pros_list.append(row)
            LENGHTS.pro_n += 1
        else:
            print("Not supported line/URL. Line:", row, "line number:", (LENGHTS.j_n + LENGHTS.vk_n + 1)) # Prints what line is not allowed
            # continue
    f.close() # Closing the file
    LENGHTS.total_url_list_len = LENGHTS.vk_n + LENGHTS.j_n + LENGHTS.pro_n # Calculating total lines
    print(f"{bcolors.OKGREEN}Successfully loaded total of {LENGHTS.total_url_list_len} rows from the file{bcolors.ENDC}")
    return vk_url_list, j_url_list, pros_list

def start():
    print(f"{bcolors.HEADER}Welcome to version {BASE.version} {BASE.version_name} of the program!{bcolors.ENDC}")
    print(f"{bcolors.WARNING}Attention! Currently using a 'cooldown' in searches of {BASE.timelimit} seconds{bcolors.ENDC}") # New addition
    time.sleep(0.5)
    print("Starting with datafile:", BASE.datafile)
    return None

def get_html(url): # This is going to be replaced with url_to_html.py
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0" # Use what user agent you want, new one to be sure
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','User-Agent': user_agent} # header from Google :P
    req = urllib.request.Request(url,None, headers) # Making the request
    try:
        page = urlopen(req) # "Opening" the url with previous parameters
        html_bytes = page.read() # Reading the page
        html = html_bytes.decode("utf-8") # Decoding to utf-8 to get proper Ä,Ö and Å
    except HTTPError as err: # https://stackoverflow.com/questions/3193060/catch-specific-http-error-in-python
        if err.code == 404:
            print(f"{bcolors.WARNING}HTTP Error 404 with a line, skipping{bcolors.ENDC}")
            html = "" # Just to make sure
            if BASE.debug == 1:
                print("404 url:", url) # DEBUG
                s, n = findlinefromfile.check(url, BASE.datafile) # Prints linenumber where url is located
                if s == True:
                    print("Line number:", n)
        elif err.code == 403: # Forbidden
            print(f"{bcolors.WARNING}HTTP Error 403 forbidden, most likely getting rate limited. Stopping{bcolors.ENDC}")
            sys.exit(0)
        else:
            raise
    except Exception:
        print(f"{bcolors.FAIL}Cannot access webpage, exiting for now{bcolors.ENDC}") # If we get timed out or other issues
        sys.exit(0)
    return html

def j_scraper(html):
    try:
        soup = BeautifulSoup(html, 'html.parser') # Parsing the raw html data
        title = soup.find("meta", property="og:title").get('content') # Finding meta titles
        title = title.replace(u'\xa0', u' ') # Cleaning
        price_pattern = "[-|1] \d{2,4},\d\d€" # Creating price pattern
        price = re.findall(price_pattern, title) # Then finding it
        price = price[0] # Selecting the first one
        price = price.replace("- ", "") # Cleaning
        price_fixed = price
        fix = " - " + price
        name = title.replace(fix, "")
        name = name.replace(" -näytönohjain", "")
        name = "'" + name + "'"
    except Exception: # If the search fails at some point
        print(f"{bcolors.WARNING}Error getting title, price or name{bcolors.ENDC}")
        price_fixed = 0 # Hardcoding values to be sure
        name = ""
    try: # Getting the status of the product
        mydivs = soup.find_all("div", {"class": "whrow"})
        mydivs = mydivs[1]
        mydivs = str(mydivs)
        avail = mydivs.replace("<div class=\"whrow\"><div class=\"whname\"><b>Web-myynti:</b></div><div class=\"whqty\">", "")
        avail = avail.replace("</div></div>", "")
        avail = avail + " web"
    except Exception:
        avail = "Not found" # Skipping the check and hardcoding an error value
    return name, price_fixed, avail

def vk_pricescraper(html):
    pattern = "\\bcontent=\"\d{2,4}.\d\d\""
    price = re.findall(pattern, html)
    pattern_fixed = "\d{2,4}.\d\d"
    price = price[0]
    price_fixed = re.findall(pattern_fixed,price)
    price_fixed = price_fixed[0]
    return price_fixed

def vk_namescraper(html):
    pattern = "<title data-rh=\"true\">[\s\S]*?Näytönohjaimet"
    name = re.findall(pattern, html)
    name = name[0]
    name = name.replace("<title data-rh=\"true\">", "")
    new_pattern = "[\s\S]*?näytönohjain"
    name = re.findall(new_pattern, name)
    name = name[0]
    name = name.replace(" -näytönohjain", "")
    name = "'" + name + "'"
    return name

def vk_avaibscraper(html):
    pattern = "out of stock|available for order|in stock"
    avail = re.findall(pattern, html)
    try:
        avail = avail[0]
    except Exception:
        print(f"{bcolors.WARNING}Availability not found{bcolors.ENDC}")
        avail = "Null"
    return avail

def pros_scraper(html):
    soup = BeautifulSoup(html, 'html.parser')
    price_fixed = "NaN"
    name = ""
    avail = "Tilattu"
    try:
        price = soup.find_all("span", {"class": "site-currency-attention"})
        price = str(price[0])
        price = price.rstrip()
        price = price.replace("<span class=\"site-currency-attention\">", "")
        price_fixed = price.replace("</span>", "")
        name = soup.find("meta", property="og:title").get('content')
        name = name.replace("GDDR6 RAM - Näytönohjaimet", "")
        avail = soup.find_all("div", {"class": "site-stock-text site-inline"})
        avail = str(avail[0])
        avail = avail.replace("<div class=\"site-stock-text site-inline\">", "")
        avail = avail.replace("</div>", "")
    except Exception:
        pass
    return name, price_fixed, avail

def printer(price_fixed, name, avail, total_counter):
    print("This product is in stock:", name, "price:", price_fixed, "euro", "availability:", avail)
    total_counter += 1
    return total_counter

def totals(total_avail, total_items):
    print("Found total", total_avail, "out of",total_items, "products available")

def arg_parser(): # Enabling file loading from arguments and debug prints This is to be replaced by arg_parser.py
    n = 0
    try:
        argv_list = sys.argv[1:] # Making a list out of the arguments minus the filename
        for i in range(len(argv_list)): # Going through the list
            item = argv_list[i]
            if item == "-d": # If the given argument is -d
                print(f"{bcolors.WARNING}Debug is turned on{bcolors.ENDC}")
                BASE.debug = 1
            elif item == "-f":
                filename = argv_list[n + 1]
                print(f"{bcolors.OKBLUE}Loaded a datafile from argument \"{filename}\"{bcolors.ENDC}")
                BASE.datafile = filename # Setting the filename global variable
            elif item == "-t":
                timelimit = int(argv_list[n + 1])
                if timelimit != BASE.timelimit:
                    print(f"Timelimit was set to {timelimit} seconds")
                    BASE.timelimit = timelimit
            elif item == "-h":
                print("Help page"+'\n'+""+'\n'+"Usage:"+'\n'+"use -f <filename> to load specific file"+'\n'+"-d to activate debug prints"+'\n'+"-t to change timelimit"+'\n'+"")
                sys.exit(0)
            elif BASE.datafile != "data.txt": # Not sure
                pass
            else: # Kinda works, not sure
                print("Argument", item, "not identified.")
            n+=1
    except Exception: # In case user input is somehow wrong
            print(f"{bcolors.FAIL}Error with arguments{bcolors.ENDC}")
            sys.exit(0)

def mainp():
    arg_parser() # To be replaced by arg_parser.py
    start()
    vk_url_list, j_url_list, pros_list = importer()
    print("Checking for Verkkokauppa.com URLs")
    total_counter = 0
    vk_n = 0 # List item counter
    vk_t0 = time.time() # Start time
    while True: # Verkkokauppa.com
        try:
            url = vk_url_list[vk_n] # Getting the url line by line
            html = get_html(url) # Getting the raw html
            if html == "": # If the html value is empty/error happened we skip
                pass       # Best for now
            else:
                price_fixed = vk_pricescraper(html) # Getting price
                name = vk_namescraper(html) # Getting product name
                avail = vk_avaibscraper(html) # Getting availability
            progressbar.progress_bar2(LENGHTS.vk_n - 1, vk_n)
            if avail == "available for order": # If the avail is good we print the details
                total_counter = printer(price_fixed, name, avail, total_counter)
            elif avail == "in stock": # New version
                total_counter = printer(price_fixed, name, avail, total_counter)
            elif BASE.debug == 1: # If debug is on
                print(f"Debuginfo {name} price: {price_fixed} eur, status: {avail}") # Prints all lines
            vk_n += 1 # Counter
            time.sleep(BASE.timelimit) # For now to not spam
        except Exception: # If vk links aren't found
            print("Verkkokauppa.com links not found, skipping")
            break         # We break from the loop
        if vk_n == LENGHTS.vk_n: # Stopping when list ends
            break
    totals(total_counter, LENGHTS.vk_n)
    vk_t1 = time.time() # End time
    vk_timer = vk_t1-vk_t0 # Verkkokauppa timer
    print("Page loads took", '{:.2f}'.format(abs(vk_timer - (LENGHTS.vk_n * BASE.timelimit))), "seconds for", LENGHTS.vk_n, "item(s)") # Two decimals fine?
    print("Checking for Jimms URLs")
    total_counter = 0 # Resetting the total for the next site
    j_t0 = time.time()
    j_n = 0
    while True:
        try:
            url = j_url_list[j_n]
            html = get_html(url)
            name, price_fixed, avail = j_scraper(html)
            progressbar.progress_bar2(LENGHTS.j_n - 1, j_n)
            if avail.startswith("0 kpl web"):
                pass
            else:
                total_counter = printer(price_fixed, name, avail,total_counter)
            if BASE.debug == 1:
                print(f"{name} price: {price_fixed} eur, status: {avail}")
            j_n += 1
            time.sleep(BASE.timelimit) # For now to not spam
        except Exception:
            print("Jimms links not found, skipping")
            break
        if j_n == LENGHTS.j_n:
            break
    totals(total_counter, LENGHTS.j_n)
    j_t1 = time.time()
    j_timer = j_t1-j_t0 # Jimms timer
    print("Page loads took", '{:.2f}'.format(abs(j_timer - (LENGHTS.j_n * BASE.timelimit))), "seconds for", LENGHTS.j_n, "item(s)")
    
    total_counter = 0
    pro_t0 = time.time()
    pro_n = 0
    while True: # Proshop
        url = pros_list[pro_n]
        html = get_html(url)
        name, price_fixed, avail = pros_scraper(html)
        progressbar.progress_bar2(LENGHTS.pro_n - 1, pro_n)
        if avail.startswith("Tilattu"):
            pass
        else:
            total_counter = printer(price_fixed, name, avail, total_counter)
        pro_n += 1
        time.sleep(BASE.timelimit) # For now to not spam
        if pro_n == LENGHTS.pro_n:
            break
    totals(total_counter, LENGHTS.pro_n)
    pro_t1 = time.time()
    pro_timer = pro_t1-pro_t0
    print("Page loads took", '{:.2f}'.format(abs(pro_timer - (LENGHTS.pro_n * BASE.timelimit))), "seconds for", LENGHTS.pro_n, "item(s)")
try:
    if __name__ == "__main__": # Fancy
        mainp()
except KeyboardInterrupt:
    print(f"{bcolors.WARNING}Stopping......{bcolors.ENDC}")
    time.sleep(0.1)
    sys.exit(0)