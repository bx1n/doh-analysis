from time import sleep, time
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
#from clear_cache import clear_firefox_cache
from get_url import get_top_urls
#from get_dns_cache import get_dns
from get_config_networking import get_urls_from_dnscache
import json, subprocess, os
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

os.system("export SSLKEYLOGFILE=" + os.getcwd() + "/sslkey.log")

binary = FirefoxBinary('/home/firefox/firefox')

resolver = [["8.8.8.8","https://dns.google/dns-query"], \
            ["1.1.1.1","https://cloudflare-dns.com/dns-query"], \
            ["176.103.130.130","https://dns.adguard.com/dns-query"],\
            ["9.9.9.9","https://dns.quad9.net/dns-query"],
            ["104.236.178.232","https://dns.dnsoverhttps.net/dns-query"]]

res = 0 


#fp.set_preference("network.dnsCacheExpiration", 60)
#fp.set_preference("network.dnsCacheExpirationGracePeriod", 10)
#fp.set_preference("network.dns.get-ttl", False)

rank_from = 0
rank_to = 10
url = get_top_urls(rank_from,rank_to);

#test case
#url = ["https://google.com/","http://nfpa.tmit.bme.hu/"]
#url = ["https://yahoo.com"]

print(url)
result = {}

for i in range(0,len(url)): 
    
    tdump_stat = 0
    #starting tcpdump for each file - and storing in seperate files
    try:
        process = subprocess.Popen(['tcpdump', '-vvvnni', 'eth0','-w', 'trace' + str(rank_from+i) + ".pcap", 'port', '443', 'or', 'port', '80', 'or', 'port', '54'], shell=False, cwd=os.getcwd()+"/data/traces/", stdout=subprocess.PIPE)
        tdump_stat = 1
    except:
        tdump_stat = 0

    cap = DesiredCapabilities().FIREFOX
    #cap["marionette"] = False
	    
    fp = webdriver.FirefoxProfile()

    fp.set_preference("network.trr.mode", 3)
    fp.set_preference("network.trr.bootstrapAddress", resolver[res][0])
    fp.set_preference("network.trr.uri", resolver[res][1])
    
    # fp.set_preference("browser.safebrowsing.features.trackingProtection.update", False)
    # fp.set_preference("browser.safebrowsing.features.flashBlock.update", False)
    # fp.set_preference("browser.safebrowsing.features.fingerprinting.annotate.update", False)
    # fp.set_preference("browser.safebrowsing.features.fingerprinting.update", False)
    # fp.set_preference("browser.safebrowsing.features.cryptomining.annotate.update", False)
    # fp.set_preference("browser.safebrowsing.features.cryptomining.update", False)
    # fp.set_preference("browser.safebrowsing.features.socialtracking.annotate.update", False)
    # fp.set_preference("browser.safebrowsing.features.socialtracking.update", False)
    # fp.set_preference("browser.safebrowsing.features.trackingAnnotation.update", False)

    # fp.set_preference("browser.newtabpage.activity-stream.feeds.snippets", False)
    #fp.set_preference("browser.search.geoip.url", "")

    #fp.set_preference("network.dnsCacheEntries", 20)

    options = Options()
    options.headless = True

    query_status = 1
    driver = webdriver.Firefox(capabilities=cap, options=options, firefox_profile=fp, firefox_binary=binary)
    

    driver.set_page_load_timeout(40)
    sleep(1)
    
    try: 
        #driver.get("http://nfpa.tmit.bme.hu/")
        tstamp = time()
        driver.get(url[i])
        if rank_from+i == 7638: 
	        try:
	            WebDriverWait(driver, 1).until(EC.alert_is_present())
	            alert = driver.switch_to.alert
	            alert.accept()
	            print("accepted")
	        except: 
	            print("No alert found")

    except:
        print("unable to query result")
        query_status = 0

    #sleep(1)

    result = get_urls_from_dnscache(driver)
    result['query-stime'] = tstamp 
    result['query-status'] = query_status
    result['query-url'] = url[i]
    result['tdump-stat'] = tdump_stat
    #print(json.dumps(net_res, indent=2))
    #print(result)

    #sleep(1)
    cmd = "sudo kill " + str(process.pid) 
    os.system(cmd)
    
    #sleep(1)
    result['query-etime'] = time()
    json.dump(result, open(os.getcwd() + '/data/urls/url' + str(rank_from+i) + '.json', 'w'))

    driver.quit()

    if result['query-status'] == 1:
        print(url[i]+" is successful!!!!")

    #exit(-1)


