import sys
from urllib.request import urlopen # To open URL provided
import urllib.request # To make the request
import re # For regex operations
import time # For time.sleep()


class BASE():
    base_url = "NA"
    datafile = "D:\Acci\code\Gpu_Scraper\data.txt"

class LENGHTS():
    total_url_list_len = 0
    vk_n = 0
    g_n = 0

def importer(): # Loading URL from a file specified
    filename = BASE.datafile
    vk_url_list = []
    g_url_list = []
    LENGHTS.vk_n = 0
    LENGHTS.g_n = 0
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
        elif row.startswith("https://www.gigantti.fi"):
            g_url_list.append(row)
            LENGHTS.g_n += 1
        elif row.startswith("https://www.verkkokauppa.com"):
            vk_url_list.append(row)
            LENGHTS.vk_n += 1
        else:
            print("Not supported line")
            sys.exit(0)
    f.close()
    LENGHTS.total_url_list_len = LENGHTS.vk_n + LENGHTS.g_n
    print("Successfully loaded total of", LENGHTS.total_url_list_len, "rows from the file")
    # print(vk_url_list)
    print(g_url_list)
    return vk_url_list, g_url_list

def start():
    print("Welcome to program")
    time.sleep(0.2)
    print("Starting with base datafile from:", BASE.datafile)
    return None

def get_html(url):
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' # Use what user agent you want
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','User-Agent': user_agent}
    req = urllib.request.Request(url,None, headers)
    try:
        page = urlopen(req)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")
    except Exception:
        print("Cannot access webpage, exiting for now")
        sys.exit(0)
    # print(page) # Print status to Terminal
    return html

def vk_pricescraper(html):
    pattern = "\\bcontent=\"\d{2,4}.\d\d\""
    price = re.findall(pattern, html)
    pattern_fixed = "\d{2,4}.\d\d"
    price = price[0]
    price_fixed = re.findall(pattern_fixed,price)
    price_fixed = price_fixed[0]
    # print(price_fixed)
    return price_fixed

def g_pricescraper(html):
    pattern = "<meta itemprop=\"price\" content=\"d{2,4},\d\d\">"
    price = re.findall(pattern, html)
    print(price)
    
    price_fixed = 0
    return price_fixed

def g_namescraper(html):
    name = "NAN"
    return name

def g_avaibscraper(html):
    avail = "NAN"
    return avail

def vk_namescraper(html):
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

def vk_avaibscraper(html):
    pattern = "out of stock|available for order"
    avail = re.findall(pattern, html)
    avail = avail[0]
    #print(avail)
    return avail

def printer(price_fixed, name, avail):
    print("Product:", name, "price:", price_fixed, "euro", "availability:", avail)


def mainp():
    start()
    vk_url_list, g_url_list = importer()
    vk_n = 0 # List item counter
    g_n = 0
    while True:
        url = vk_url_list[vk_n]
        html = get_html(url)
        price_fixed = vk_pricescraper(html)
        name = vk_namescraper(html)
        avail = vk_avaibscraper(html)
        printer(price_fixed, name, avail)
        vk_n += 1

        if vk_n == LENGHTS.vk_n:
            print("Moving to Gigantti list") # WORK IN PROGRESS
            try:
                url = g_url_list[g_n]
                html = get_html(url)
                price_fixed = g_pricescraper(html)
                name = g_namescraper(html)
                avail = g_avaibscraper(html)
                printer(price_fixed, name, avail)
                g_n += 1
            except Exception:
                print("Gigantti links not found, stopping.")
                break
            if g_n == LENGHTS.g_n:
                break

mainp()