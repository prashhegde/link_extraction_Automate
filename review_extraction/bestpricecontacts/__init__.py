from random import randint
from time import sleep
from openpyxl import load_workbook
from datetime import datetime
from bs4 import BeautifulSoup
from review_extraction.utilities.utils.logger import LogJ
from review_extraction.utilities.xls_generator import *
from review_extraction.bestpricecontacts import *
import threading
from selenium import webdriver
from time import strptime
from pathlib import Path

TAG = "www.bestpricecontacts.com"
PATH_INPUT = "C:/Users/Prash/Desktop/Work/scrapj-new/scrapj/data/input/"


class BestPriceContacts():
    driver = None
    total_reviews = 0
    total_exp = 0
    start_time = ''
    end_time = ''
    params = ()
    error_logger = LogJ(TAG, "ERROR")
    info_logger = LogJ(TAG, "INFO")

    def __init__(self, driver, params):
        self.driver = driver
        self.params = params

    def extract_data(self, excel):
        wb = load_workbook(filename=PATH_INPUT + 'www.bestpricecontacts.com.xlsx', read_only=True)
        ws = wb[wb.get_sheet_names()[0]]
        excel.add_headers(excel.wb.active,
                          ["Title", "Comments", "Overall", "Comfort", "Vision", "Value for Money", "Author", "Date",
                           "Pros", "Cons", "Original Source",
                           "Reply from Acuvue", "Product Name", "Product Link", "Website"])
        for row in ws.rows:
            for cell in row:
                if str(type(cell)).__eq__("<class 'openpyxl.cell.read_only.ReadOnlyCell'>") and cell.row != 1:
                    if cell.column == 1:
                        print(cell.row)
                        print(cell.value)
                        try:
                            excel.save_xls(excel.wb)
                        except Exception as e:
                            print(e)
                            self.total_exp += 1
                        # url_to_crawl = "http://www.visiondirect.co.uk/brand/acuvue-contact-lenses/1-day-acuvue-moist"
                        # self.get_page(url_to_crawl)
                        if cell.value is not None and not "":
                            self.get_page(cell.value)
                            self.grab_reviews(excel, row[1].value, cell.value)

    # Tell the browser to get a page
    def get_page(self, url):
        print('getting page...')
        start_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        print("Start Time" + start_time)
        self.driver.get(url)
        sleep(randint(2, 3))

    def grab_reviews(self, excel, product_name, product_url):
        print('grabbing reviews......')
        print(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
        print(len(
            self.driver.find_elements_by_xpath('//*[@id="tabContent"]/div[3]/div[2]/div[contains(@style,"float")]')))
        log = [product_name, product_url]
        curr_reviews = self.total_reviews
        last_thread = None
        elements = []
        try:
            product_name = self.driver.find_element_by_xpath(
                '//*[contains(@class,"contentPadding")]//table[contains(@width,"100%")]//*[contains(@valign,"top")]/h1')
            product_name = str(product_name.get_attribute("innerHTML")).strip()
        except:
            print("Error getting product name")
            pass
        i = 1
        for div in self.driver.find_elements_by_xpath(
                '//*[@id="tabContent"]/div[3]/div[2]/div[contains(@style,"float")]'):
            if i % 2 != 0:
                part1 = str(div.get_attribute("innerHTML"))
            else:
                part1 = part1 + str(div.get_attribute("innerHTML"))
                elements.append(part1)
            i += 1
        for element in elements:
            try:
                last_thread = threading.Thread(target=self.thread_process, args=
                (element, product_name, product_url, excel))
                last_thread.start()
            except Exception as e:
                print(e)
                self.total_exp += 1
                print("Error: unable to start thread")
        # threading.Thread(target=self.logging, args=(curr_reviews, log, last_thread)).start()

    # def logging(self, curr_reviews, log, last_thread):
    #     while last_thread and last_thread.isAlive():
    #         pass
    #     log.append(self.total_reviews - curr_reviews)
    #     self.info_logger.log(log)

    def thread_process(self, div, product_name, product_url, excel):
        # row = self.process_elements(div)
        row = self.process_soup(div)
        if row:
            row.append(product_name)
            row.append(product_url)
            row.append(TAG)
            excel.insert_row(getattr(excel, "wb"), row)

    def process_soup(self, div):
        soup = BeautifulSoup(div, 'lxml')
        attributes = []

        try:
            content = soup.select_one(".BlackH5")
            if content is not None:
                print(content.getText())
                attributes.append(content.getText())
            else:
                attributes.append("NA1")
        except:
            attributes.append("NA1")
            pass
        try:
            content = soup.select(".BlackH6")[1]
            if content is not None:
                print(content.getText())
                attributes.append(content.getText())
            else:
                attributes.append("NA2")
        except:
            attributes.append("NA2")
            pass
        try:
            content = str(soup.select(".BlackH6")[0].getText()).split(":")
            if content is not None:
                star = str(content[5]).strip() + " out of 5"
                print(star)
                attributes.append(star)
                star = str(content[3]).strip().split("Vision")[0][:2].strip() + " out of 5"
                print(star)
                attributes.append(star)
                star = str(content[4]).strip().split("Overall")[0][:2].strip() + " out of 5"
                print(star)
                attributes.append(star)
            else:
                attributes.append("NA3")
        except:
            attributes.append("NA3")
            pass

        attributes.append("NA3")
        try:
            # content = soup.select_one("strong > span")
            if content is not None:
                author = str(content[2]).strip().split("Comfort")[0].strip()
                print(author)
                attributes.append(author)
            else:
                attributes.append("NA4")
        except:
            attributes.append("NA4")
            pass

        try:
            # content = soup.select_one("time")
            if content is not None:
                date = str(content[1]).split("Reviewer")[0].strip()
                print(date)
                date = datetime.strptime(date, '%m/%d/%Y').strftime('%Y/%m/%d')
                attributes.append(date)
            else:
                attributes.append("")
        except:
            attributes.append("")
            pass

        attributes.append("NA6")
        attributes.append("NA7")
        attributes.append(TAG)
        attributes.append("NA9")

        self.total_reviews = self.total_reviews + 1
        print("Total Number of reviews : " + str(self.total_reviews))
        print("Total Number of exp : " + str(self.total_exp))
        return attributes


# Open headless chromedriver
def start_driver():
    print('starting driver...')
    try:
        driver = webdriver.Chrome("C:/Users/Prash/Desktop/Work/scrapj-Thread-Implementation/scrapj/input_link_extraction/utilities/drivers/chromedriver.exe")
    except:
        try:
            driver = webdriver.Chrome("C:/Users/Prash/Desktop/Work/scrapj-Thread-Implementation/scrapj/input_link_extraction/utilities/drivers/chromedriver")
        except:
            print("No Driver")

    sleep(4)
    return driver


# Close chromedriver\
def close_driver(driver):
    print('closing driver...')
    driver.quit()
    print('closed!')


start_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
driver = start_driver()

wg = Excel("www.bestpricecontacts.com") #correct
wb = getattr(wg, "wb")
lens = BestPriceContacts(driver, None)
lens.extract_data(wg)
while True:
    try:
        wg.save_xls(wb)
        Path("../status/" + "www.bestpricecontacts.com" + ".txt").touch()
        break
    except:
        pass