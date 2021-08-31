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
        self.server = "https://www.mycareersfuture.gov.sg"
        self.keyword = "/search?search=Java"
        self.min_salary = "&salary=5500"
        self.target = "&sortBy=new_posting_date&page="
        self.num = 0
        self.company = []
        self.url = []
        self.title = []
        self.detail = []
        self.salary = []
        self.applicant = []

    def get_download_url(self):

        for x in range(0, 151):  # auto-open 151 webpages to exact job openings' info
            driver = webdriver.Chrome()  # launch chromedriver
            url = self.server + self.keyword + self.min_salary + self.target + str(x)
            driver.get(url)
            timeout = 3  # second
            try:
                element_present = EC.presence_of_element_located((By.CLASS_NAME, "mb1-ns mb0 tl tr-ns dib db-ns"))
                WebDriverWait(driver, timeout).until(element_present)
            except TimeoutException:
                print("Timed out waiting for page to load")
            content = BeautifulSoup(driver.page_source, "html.parser")
            driver.quit()

            a = content.find_all("div", "card relative")  # search for elements containing job opening's info

            for each in a[:]:
                link = self.server + each.a.get("href")  # parse each job opening's weblink
                self.url.append(link)

                company_name = each.a.p.string  # parse each job opening's company name
                self.company.append(company_name)

                job_title = each.find("span", class_="f4-5 fw6 mv0 brand-sec dib mr2 JobCard__jobtitle___3HqOw").get_text()  # parse each job opening's title
                self.title.append(job_title)

                job_detail = each.find("div", "w-100 db dn-ns order-1 pt2").get_text(";")  # parse each job opening's detail

                if each.find("p", "black-80 f6 fw4 mt0 mb1 dib pr3 ttc icon-bw-period") is None:  # fill the cell with None if num of years of experience is not specified
                    job_detail = job_detail + ";None"

                self.detail.append(job_detail)

                salary_range = each.find("div", "lh-solid").get_text(" ")  # parse each job opening's salary info

                self.salary.append(salary_range)

                application = each.find("div", "w-100 pt3 flex dn-l justify-between").get_text(";")  # parse each job opening's applicant number
                self.applicant.append(application)

            for i in range(self.num, len(dl.url[:])):  # write each job openings into a txt file
                dl.writer("joblisting_5500_0831v5.txt", dl.url[i], dl.company[i], dl.title[i], dl.detail[i], dl.salary[i], dl.applicant[i])
                sys.stdout.flush()

            print("Done written index " + str(self.num) + " to " + str(len(dl.url[:]) - 1))  # System output successful message upon processing of each webpages are done
            self.num = len(dl.url[:])

    def writer(self, path, url, company, title, detail, salary, application):
        write_flag = True
        with open(path, 'a', encoding='utf-8') as f:
            f.writelines(company + ";" + title + ";" + detail + ";" + salary + ";" + application + ";" + url)
            f.write('\n')

if __name__ == "__main__":
    dl = Downloader()
    dl.get_download_url()
