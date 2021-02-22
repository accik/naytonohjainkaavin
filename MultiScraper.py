import sys
from urllib.request import urlopen # To open URL provided
import urllib.request # To make the request
from bs4 import BeautifulSoup # To properly manage html tags later
import re # For regex operations
import time # For time.sleep()


class BASE():
    base_url = "NA"
    datafile = "D:\Acci\code\Gpu_Scraper\data.txt"

class LENGHTS():
    total_url_list_len = 0
    vk_n = 0
    j_n = 0

def importer(): # Loading URL from a file specified
    filename = BASE.datafile
    vk_url_list = []
    j_url_list = []
    # LENGHTS.vk_n = 0
    # LENGHTS.j_n = 0
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
        elif row.startswith("https://www.jimms.fi/"):
            j_url_list.append(row)
            LENGHTS.j_n += 1
        elif row.startswith("https://www.verkkokauppa.com"):
            vk_url_list.append(row)
            LENGHTS.vk_n += 1
        else:
            print("Not supported line/URL")
            # continue
    f.close()
    LENGHTS.total_url_list_len = LENGHTS.vk_n + LENGHTS.j_n
    print("Successfully loaded total of", LENGHTS.total_url_list_len, "rows from the file")
    # print(vk_url_list)
    # print(j_url_list)
    return vk_url_list, j_url_list

def start():
    print("Welcome to program")
    time.sleep(0.2)
    print("Starting with base datafile from:", BASE.datafile)
    return None

def get_html(url):
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' # Use what user agent you want
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','User-Agent': user_agent} # header from Google :P
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
    mydivs = soup.find_all("div", {"class": "whrow"})
    mydivs = mydivs[1]
    mydivs = str(mydivs)
    avail = mydivs.replace("<div class=\"whrow\"><div class=\"whname\"><b>Web-myynti:</b></div><div class=\"whqty\">", "")
    avail = avail.replace("</div></div>", "")
    avail = avail + " web"
    # print(name,price,avail)
    return name, price_fixed, avail

def vk_pricescraper(html):
    pattern = "\\bcontent=\"\d{2,4}.\d\d\""
    price = re.findall(pattern, html)
    pattern_fixed = "\d{2,4}.\d\d"
    price = price[0]
    price_fixed = re.findall(pattern_fixed,price)
    price_fixed = price_fixed[0]
    # print(price_fixed)
    return price_fixed

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
    vk_url_list, j_url_list = importer()
    print("Checking for Verkkokauppa.com URLs")
    vk_n = 0 # List item counter
    vk_t0 = time.time()
    while True: # Verkkokauppa.com
        url = vk_url_list[vk_n]
        html = get_html(url)
        price_fixed = vk_pricescraper(html)
        name = vk_namescraper(html)
        avail = vk_avaibscraper(html)
        printer(price_fixed, name, avail)
        vk_n += 1
        if vk_n == LENGHTS.vk_n:
            break
    vk_t1 = time.time()
    vk_timer = vk_t1-vk_t0 # Verkkokauppa timer
    print("That took", '{:.2f}'.format(vk_timer), "seconds", LENGHTS.vk_n, "item(s)") # Two decimals fine?
    j_t0 = time.time()
    print("Checking for Jimms URLs")
    j_n = 0
    while True:
        try:
            url = j_url_list[j_n]
            html = get_html(url)
            price_fixed, name, avail = j_scraper(html)
            printer(name,price_fixed, avail)
            j_n += 1
        except Exception:
            print("Jimms links not found, stopping.")
            break
        if j_n == LENGHTS.j_n:
            break
    j_t1 = time.time()
    j_timer = j_t1-j_t0 # Jimms timer
    print("That took", '{:.2f}'.format(j_timer), "seconds for", LENGHTS.j_n, "item(s)")
mainp()