import sys
from urllib.request import urlopen # To open URL provided
import re # For regex operations
import time # For time.sleep()

class BASE():
    base_url = "verkkokauppa.com"
    datafile = "D:\Acci\code\Gpu_Scraper\data.txt"

def importer(): # Loading URL from a file specified
    filename = BASE.datafile
    url_list = []
    n = 0
    try:
        f = open(filename, "r")
    except FileNotFoundError:
        print("File not found")
        sys.exit(0)
    except Exception:
        print("Error opening")
        sys.exit(0)
    while True:
        try:
            row = f.readline()
        except Exception:
            print("Error reading line from the file")
            sys.exit(0)
        row = row.rstrip()
        if len(row) == 0:
            break
        elif row.startswith("base"): # NOT WORKING
            print("Setting base_url to", row)
            BASE.base_url = row
        else:
            url_list.append(row)
            n += 1
    f.close()
    print("Loaded", n, "rows from the file")
    url_list_len = n
    # print(url_list)
    return url_list, url_list_len

def start():
    print("Welcome to program")
    time.sleep(0.5)
    print("Starting with base URL of", "'"+ BASE.base_url + "'", "and datafile from:", BASE.datafile)
    return None

def pricescraper(url):
    try:
        page = urlopen(url)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")
    except Exception:
        print("Cannot access webpage or wrong url, exiting for now")
        sys.exit(0)
    # print(html) # Print to Terminal
    pattern = "\\bcontent=\"\d{2,4}.\d\d\""
    price = re.findall(pattern, html)
    pattern_fixed = "\d{2,4}.\d\d"
    price = price[0]
    price_fixed = re.findall(pattern_fixed,price)
    price_fixed = price_fixed[0]
    # print(price_fixed)
    return price_fixed, html

def namescraper(html):
    pattern = "<title data-rh=\"true\">[\s\S]*?Näytönohjaimet"
    name = re.findall(pattern, html)
    #print(name)
    name = name[0]
    name = name.replace("<title data-rh=\"true\">", "")
    new_pattern = "[\s\S]*?näytönohjain"
    name = re.findall(new_pattern, name)
    name = name[0]
    name = name.replace(" -näytönohjain", "")
    name = "'" + name + "'"
    return name

def avaibscraper(html):
    pattern = "out of stock|available for order"
    avail = re.findall(pattern, html)
    avail = avail[0]
    #print(avail)
    return avail

def printer(price_fixed, name, avail):
    print("Product:", name, "price:", price_fixed, "euro", "availability:", avail)

def run(url):
    try:
        price_fixed, html = pricescraper(url)
        name = namescraper(html)
        avail = avaibscraper(html)
    except Exception:
        print("Fatal error, exiting")
        sys.exit(0)
    return price_fixed, name, avail

def mainp():
    start()
    n = 0
    url_list,url_list_len = importer()
    while True:
        url = url_list[n]
        price_fixed, name, avail = run(url)
        printer(price_fixed, name, avail)
        n += 1
        if n == url_list_len:
            break
            
mainp()