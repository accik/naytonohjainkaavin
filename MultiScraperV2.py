import sys
from urllib.request import urlopen # To open URL provided
import urllib.request # To make the request
from bs4 import BeautifulSoup # To properly manage html tags later
import re # For regex operations
import time # For time.sleep()

class BASE():
    base_url = "NA"
    version = 2.0
    datafile = "D:\Acci\code\Gpu_Scraper\data_s.txt"
    timelimit = 5

class LENGHTS():
    total_url_list_len = 0
    vk_n = 0
    j_n = 0

def importer(): # Loading URL from a file specified
    filename = BASE.datafile
    vk_url_list = [] # Making the lists
    j_url_list = []
    try:
        f = open(filename, "r") # Opening the file with read
    except FileNotFoundError:
        print("File not found")
        sys.exit(0)
    except Exception:
        print("Error opening")
        sys.exit(0)
    while True:
        try:
            row = f.readline() # Reading one line from the file
        except Exception:
            print("Error reading line from the file")
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
        else:
            print("Not supported line/URL")
            # continue
    f.close() # Closing the file
    LENGHTS.total_url_list_len = LENGHTS.vk_n + LENGHTS.j_n # Calculating total lines
    print("Successfully loaded total of", LENGHTS.total_url_list_len, "rows from the file")
    return vk_url_list, j_url_list

def start():
    print("Welcome to version 2 of the program")
    print("Attention! Currently using a 'cooldown' in searches of", BASE.timelimit, "seconds.") # New addition
    time.sleep(0.5)
    print("Starting with base datafile from:", BASE.datafile)
    return None

def get_html(url):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0" # Use what user agent you want, new one to be sure
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','User-Agent': user_agent} # header from Google :P
    req = urllib.request.Request(url,None, headers) # Making the request
    try:
        page = urlopen(req) # "Opening" the url with previous parameters
        html_bytes = page.read() # Reading the page
        html = html_bytes.decode("utf-8") # Decoding to utf-8 to get proper Ä,Ö and Å
    except Exception:
        print("Cannot access webpage, exiting for now") # If we get timed out or other issues
        sys.exit(0)
    return html

def j_scraper(html):
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find("meta", property="og:title").get('content')
    title = title.replace(u'\xa0', u' ')
    price_pattern = "[-|1] \d{2,4},\d\d€"
    price = re.findall(price_pattern, title)
    price = price[0]
    price = price.replace("- ", "")
    price_fixed = price
    fix = " - " + price
    name = title.replace(fix, "")
    name = name.replace(" -näytönohjain", "")
    name = "'" + name + "'"
    try: # If "web-myynti" is not found
        mydivs = soup.find_all("div", {"class": "whrow"})
        mydivs = mydivs[1]
        mydivs = str(mydivs)
        avail = mydivs.replace("<div class=\"whrow\"><div class=\"whname\"><b>Web-myynti:</b></div><div class=\"whqty\">", "")
        avail = avail.replace("</div></div>", "")
        avail = avail + " web"
    except:
        avail = "Not available or error" # Skipping the check and hardcoding an error value
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
    pattern = "out of stock|available for order"
    avail = re.findall(pattern, html)
    avail = avail[0]
    return avail

def printer(price_fixed, name, avail, total_counter):
    print("This product is in stock:", name, "price:", price_fixed, "euro", "availability:", avail)
    total_counter += 1
    return total_counter

def totals(total_avail, total_items):
    print("Found total", total_avail, "out of",total_items, "products available.")

def mainp():
    start()
    vk_url_list, j_url_list = importer()
    print("Checking for Verkkokauppa.com URLs")
    total_counter = 0
    vk_n = 0 # List item counter
    vk_t0 = time.time() # Start time
    while True: # Verkkokauppa.com
        url = vk_url_list[vk_n]
        html = get_html(url)
        price_fixed = vk_pricescraper(html)
        name = vk_namescraper(html)
        avail = vk_avaibscraper(html)
        if avail == "available for order":
            total_counter = printer(price_fixed, name, avail, total_counter)
        vk_n += 1
        time.sleep(BASE.timelimit) # For now to not spam
        if vk_n == LENGHTS.vk_n:
            break
    totals(total_counter, LENGHTS.vk_n)
    vk_t1 = time.time() # End time
    vk_timer = vk_t1-vk_t0 # Verkkokauppa timer
    print("That took", '{:.2f}'.format(vk_timer - (LENGHTS.vk_n * BASE.timelimit)), "seconds for", LENGHTS.vk_n, "item(s)") # Two decimals fine?
    print("Checking for Jimms URLs")
    total_counter = 0 # Resetting the total for the next site
    j_t0 = time.time()
    j_n = 0
    while True:
        try:
            url = j_url_list[j_n]
            html = get_html(url)
            price_fixed, name, avail = j_scraper(html)
            if avail.startswith("0 kpl web"):
                pass
            else:
                total_counter = printer(name,price_fixed, avail,total_counter)
            j_n += 1
            time.sleep(BASE.timelimit) # For now to not spam
        except Exception:
            print("Jimms links not found, stopping.")
            break
        if j_n == LENGHTS.j_n:
            break
    totals(total_counter, LENGHTS.j_n)
    j_t1 = time.time()
    j_timer = j_t1-j_t0 # Jimms timer
    print("That took", '{:.2f}'.format(j_timer - (LENGHTS.j_n * BASE.timelimit)), "seconds for", LENGHTS.j_n, "item(s)")
mainp()