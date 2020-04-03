from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import threading
import traceback
from time import sleep
from datetime import datetime


class ILens:
    def __init__(self, website, brands, excel, excel_dump, driver, logging, match_product_name, get_page, total_links):
        get_page("http://" + website)
        self.logging = logging
        self.match_product_name = match_product_name
        self.brands = brands
        self.driver = driver
        self.total_links = total_links
        self.total_exp = 0

        for brand in self.brands:
            search_input = self.driver.find_element_by_xpath(
                '//*[@id="s"]')
            search_input.clear()
            search_input.send_keys(brand)
            search_input.send_keys(Keys.ENTER)
            sleep(1)

            print('grabbing reviews......')
            print(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
            curr_links = self.total_links
            last_thread = None
            log = [brand]

            while True:
                try:
                    elements = self.driver.find_elements_by_xpath('//*/div[@class="results"]//ul//li')
                    print("ganesh")
                    print(len(elements))
                    if len(elements) < 1:
                        elements = self.driver.find_elements_by_xpath('//*/table[1]/tbody[1]/tr/td/div')
                        print("ganesh2")
                        print(len(elements))
                except Exception as e:
                    self.logging(curr_links, log, None)
                    break
                if len(elements) < 1:
                    self.logging(curr_links, log, None)
                    break
                for div in elements:
                    try:
                        last_thread = threading.Thread(target=self.get_data,
                                                       args=(div.get_attribute("innerHTML"), excel, excel_dump))
                        last_thread.start()
                    except:
                        self.total_exp += 1
                        print("Error: unable to start thread")
                threading.Thread(target=self.logging, args=(curr_links, log, last_thread)).start()
                # next_button = self.driver.find_element_by_xpath(
                #     '//*[@id="omni-next-click"]')
                # # print(load_more_button.get_attribute("innerHTML"))
                # if str(next_button.get_attribute("title")).__eq__("Click or press enter for next page"):
                #     self.driver.execute_script("arguments[0].click();", next_button)
                #     sleep(1)
                # else:
                #     break
                break
                continue
    def get_data(self, div, excel, excel_dump):
        soup = BeautifulSoup(div, 'lxml')
        attributes = []

        try:
            content = soup.select_one(".productName")
            if content is not None:
                attributes.append(str(content.get("href")))
                print(content.getText().strip())
                attributes.append(content.getText().strip())
            else:
                attributes.append("NA")
        except:
            traceback.print_exc()
            attributes.append("NA")
            pass
        attributes.append("NA")
        self.total_links = self.total_links + 1
        print("Total Number of reviews : " + str(self.total_links))
        # print("Total Number of exp : " + str(self.total_exp))
        row = attributes
        if row and not self.match_product_name(row[1]):
            excel_dump.insert_row(getattr(excel_dump, "wb"), row)
        else:
            excel.insert_row(getattr(excel, "wb"), row)