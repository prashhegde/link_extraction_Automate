from random import randint
from time import sleep
from openpyxl import load_workbook
from datetime import datetime
import _thread
from bs4 import BeautifulSoup
from datetime import datetime

from datetime import datetime

from selenium import webdriver
from review_extraction.coastal import *
from pathlib import Path
import os



from selenium import webdriver

from review_extraction.utilities.xls_generator import Excel

TAG = "www.coastal.com"
PATH_INPUT = "C:/Users/Prash/Desktop/Work/scrapj-new/scrapj/data/input/"


class Coastal():
    driver = None
    total_reviews = 0
    total_exp = 0
    start_time = ''
    end_time = ''
    params = ()

    def __init__(self, driver, params):
        self.driver = driver
        self.params = params

    def extract_data(self, excel):
        wb = load_workbook(filename=PATH_INPUT + 'www.coastal.com.xlsx', read_only=True)
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
        #print(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
        # global prev_div
        # prev_div = ''
        # while True:
        #     elements = self.driver.find_elements_by_xpath('//*[@class="_dpc"]')
        #     print(len(elements))
        #     if len(elements) == 0:
        #         return
        #     for div in elements:
        #         cur_div = div.get_attribute("innerHTML")
        #         if prev_div.__eq__(cur_div):
        #             return
        #         try:
        #             _thread.start_new_thread(self.thread_process,
        #                                      (cur_div, product_name, product_url, excel))
        #         except:
        #             self.total_exp += 1
        #             print("Error: unable to start thread")
        #     prev_div = elements[0].get_attribute("innerHTML")
        #     next_button = self.driver.find_element_by_xpath('//*[@id="reviews-next-btn"]')
        #     print(next_button.get_attribute("innerHTML"))
        #     self.driver.execute_script("arguments[0].click();", next_button)
        #     sleep(1)
        #title
        try:
            product_name = self.driver.find_element_by_xpath('//*[@class="title-header-wrapper-red"]')
            product_name = str(product_name.get_attribute("innerHTML")).strip()
           #print(product_name)
        except:
            print("Error getting product name")
            pass
        pagecount=0
        while pagecount<10:
            try:
                sleep(randint(2, 4))
                elements = self.driver.find_elements_by_xpath('//*[@class="pr-review"]')
            except:
                print("No Reviews")
                return

            #print(len(elements))
            if len(elements) == 0:
                return
            for div in elements:
                #print(div.get_attribute("innerHTML"))
                cur_div = div.get_attribute("innerHTML")
                try:
                    _thread.start_new_thread(self.thread_process,
                                             (cur_div, product_name, product_url, excel))
                except:
                    self.total_exp += 1
                    print("Error: unable to start thread")
            try:
                next_button = self.driver.find_element_by_xpath('//*[@aria-label="Next"]')
            except:
                return
            try:
                a = next_button #.find_element_by_tag_name("a")
                #print(a)
                self.driver.execute_script("arguments[0].click();", a)
                #print("Click")
                sleep(1)
            except:
                print("No more reviews")
                return
            pagecount+=1

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

        # Title
        try:
            content = soup.select_one(".pr-rd-review-headline")
            if content is not None:
                #print(content.getText())
                attributes.append(content.getText())
            else:
                attributes.append("NA1")
        except:
            attributes.append("NA1")
            pass
        # Comments
        try:
            content = soup.select_one(".pr-rd-description-text")
            if content is not None:
                #print(content.getText())
                attributes.append(content.getText())
            else:
                attributes.append("NA2")
        except:
            attributes.append("NA2")
            pass
        # Ratings
        try:
            content = soup.select_one(".pr-snippet-rating-decimal")
            if content is not None:
                star = content.getText()[:1] + " out of 5"
                #print(star)
                attributes.append(star)
            else:
                attributes.append("NA3")
        except:
            attributes.append("NA3")
            pass
        attributes.append("NA3")
        attributes.append("NA3")
        attributes.append("NA3")

        # Author
        try:
            content = soup.select_one("p.pr-rd-details.pr-rd-author-location > span > span:nth-child(2)")
            if content is not None:
                #print(content.getText())
                attributes.append(str(content.getText()))
            else:
                attributes.append("NA4")
        except Exception as e:
            print(e)
            attributes.append("NA4")
            pass
        # Date
        try:
            content = soup.select_one("time")
            attributes_dictionary = content.attrs
            timeval=attributes_dictionary['datetime']
            timeval=timeval.split('T')
            timeval=timeval[0]
            # print(timeval)
            if timeval is not None:
                # date = str(content.getText()).strip().split(" ")
                # date = str(strptime(str(date[0]), '%B').tm_mon) + "/" + date[1][:-1] + "/" + str(date[2])
                date = datetime.strptime(timeval, '%Y-%m-%d').strftime('%Y/%m/%d')
                print(date)
                attributes.append(date)
            else:
                attributes.append("NA5")
        except:
            attributes.append("NA5")
            pass
        # # pros
        try:
            tags=str(soup.select_one(".pr-rd-content-block > dl:nth-of-type(1) > dt").getText())
            if tags == "Best for" :
                content = soup.select_one(".pr-rd-content-block > dl:nth-of-type(2)").find_all("dd")
            else:
                content = soup.select_one(".pr-rd-content-block > dl:nth-of-type(1)").find_all("dd")
            if content:
                pros_text = ''
                for pros in content:
                    if pros_text=="":
                        pros_text += ','
                    pros_text += str(pros.getText())
                attributes.append(pros_text)
            else:
                attributes.append("NA6")
        except:
            attributes.append("NA6")
            pass
        # # cons
        try:
            tags=str(soup.select_one(".pr-rd-content-block > dl:nth-of-type(1) > dt").getText())
            if tags == "Best for" :
                content = soup.select_one(".pr-rd-content-block > dl:nth-of-type(3)").find_all("dd")
            else :
                content = soup.select_one(".pr-rd-content-block > dl:nth-of-type(2)").find_all("dd")
            if content:
                cons_text = ''
                for cons in content:
                    if cons_text=="":
                        cons_text += ','
                    cons_text += str(cons.getText())
                attributes.append(cons_text)
            else:
                attributes.append("NA7")
        except:
            attributes.append("NA7")
            pass
        # # OriginalSource
        try:
            content = soup.select_one(".pr-review-attribution-img").find("a")
            if content is not None:
                website = content.get("href")
                print("Original WebSite: " + website[7:-1])
                attributes.append(website[7:-1])
            else:
                attributes.append(TAG)
        except Exception as e:
            print(e)
            attributes.append(TAG)
            pass

        # Reply from Acuvue
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


wg = Excel("www.coastal.com")  #to be corrected
wb = getattr(wg, "wb")
coastal = Coastal(driver, None)
coastal.extract_data(wg)
while True:
    try:
        wg.save_xls(wb)
        Path("../status/" + "www.coastal.com" + ".txt").touch()
        break
    except:
        pass