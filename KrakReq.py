from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import re
from urllib.parse import urlparse
from urlmatch import urlmatch


def checkBrowserClosed(driver):
    try:
        driver.current_url
        return False
    except:
        return True
    
def getRequests(target,manaulDiscover):
    domain = urlparse(target).netloc
    reDomain = '.'.join(domain.split('.')[-2:])
    domain = 'https://*.'+reDomain+'/*'
    
    requests = []
    tempUrls = []
    #driver = webdriver.Firefox()
    driver = webdriver.Chrome(ChromeDriverManager().install())

    driver.get(target)


    
    if manaulDiscover == 1:
        while True:
            if checkBrowserClosed(driver):
                break
            for req in driver.requests:
                if req.response:
                    if urlmatch(domain,req.url):
                        if req.url not in tempUrls:
                            print(req.url)
                            tempUrls.append(req.url)
                            requests.append(req)

    else:
        for request in driver.requests:
            if request.response:
                if urlmatch(domain,request.url):
                    if request.url not in tempUrls:
                        requests.append(request)
                        tempUrls.append(request)
                        print(request.url)
        driver.quit()
    
    print('Matching Findings With Target Domain')
    return requests


