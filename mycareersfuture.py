#!/usr/bin/python
# -*- coding: <encoding name> -*-

"""mycareersfuture.py: Crawler program to analyse job openings on mycareersfuture website"""

from bs4 import BeautifulSoup
import sys
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

__author__ = "Fan Lang"
__email__ = "a0099409@u.nus.edu"

class Downloader(object):

    def __init__(self):
        self.server = 'https://www.mycareersfuture.gov.sg'
        self.target = 'https://www.mycareersfuture.gov.sg/search?search=Java&salary=5500&sortBy=new_posting_date&page='
        self.num = 0
        self.company = []
        self.url = []

    def get_download_url(self):

        for x in range(0, 3):  # auto-open 100 webpages to exact job openings' info
            driver = webdriver.Chrome()  # launch chromedriver
            url = self.target + str(x)
            driver.get(url)
            timeout = 50
            try:
                element_present = EC.presence_of_element_located((By.ID, 'job-card-0'))
                WebDriverWait(driver, timeout).until(element_present)
            except TimeoutException:
                print("Timed out waiting for page to load")
            content = BeautifulSoup(driver.page_source, "html.parser")
            driver.quit()

            a = content.find_all("div", "card relative")

            for each in a[:]:
                link = self.server + each.a.get('href')  # parse each job opening's weblink
                #print("link = " + link)
                self.url.append(link)
                company_name = each.a.p.string  # parse each job opening's company name
                #print("Company name = " + company_name)
                self.company.append(company_name)

            for i in range(self.num, len(dl.url[:])):
                dl.writer('joblisting_5500_0831.txt', dl.url[i], dl.company[i])
                sys.stdout.flush()

            print("Done written index " + str(self.num) + " to " + str(len(dl.url[:]) - 1))  # System output successful message upon processing of each webpages are done
            self.num = len(dl.url[:])

    def writer(self, path, url, company):
        write_flag = True
        with open(path, 'a', encoding='utf-8') as f:
            f.writelines(company + ";" + url)
            f.write('\n')

if __name__ == "__main__":
    dl = Downloader()
    dl.get_download_url()
