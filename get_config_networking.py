from time import sleep
from selenium.webdriver.support.ui import WebDriverWait


s1 = '#dns_content > tr'
s2 = '#dns_content > tr:nth-child(5) > td:nth-child(1)'
ip_s = '#dns_content > tr:nth-child(1) > td:nth-child(4)'

def get_table_rows(driver, select):
    try:
        return driver.find_elements_by_css_selector(select)
    except:
        flag = 1

def get_element(driver, path):
    try:
        return driver.find_element_by_css_selector(path)
    except:
        flag = 1


def get_urls_from_dnscache(driver):
    
    driver.get("about:networking#dns")
    #sleep(2)
    #wait = WebDriverWait(driver, 20)
 
    #column_count = wait.until(driver.find_element_by_xpath("/html/body/div[3]/div[4]/table/tbody/tr[1]/td[1]"))
    
    #out = check_exists_by_css_selector(driver, )
    #print(column_count)
        
    cnt = len(get_table_rows(driver, s1)) + 1
        
    dns_res = {}

    for i in range(1,cnt):

        #get URL         
        url = driver.find_element_by_css_selector("#dns_content > tr:nth-child(" + str(i) + ") > td:nth-child(1)").get_attribute('innerHTML')

        #get IP addresses associated with each URL
        ip = driver.find_element_by_css_selector("#dns_content > tr:nth-child(" + str(i) + ") > td:nth-child(4)").get_attribute('innerHTML')

        ip = ip.split("<br xmlns=\"http://www.w3.org/1999/xhtml\" />")
        del ip[-1]

        #checking if the URL is present in the dic at the time of entry
        if url in dns_res.keys():
            dns_res[url] = dns_res[url] + ip
            dns_res[url] = list(dict.fromkeys(dns_res[url]))
        else:
            dns_res[url] = ip

    return dns_res
