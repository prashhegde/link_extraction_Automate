from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import threading
import traceback
from time import sleep
from datetime import datetime


class IGoogle:
    def __init__(self, website, brands, excel, excel_dump, driver, logging, match_product_name, get_page, total_links):
        get_page("http://" + website + "/search?q=acuvue&tbm=shop")
        self.logging = logging
        self.match_product_name = match_product_name
        self.brands = brands
        self.driver = driver
        self.total_links = total_links
        self.total_exp = 0
        
        for brand in self.brands:
            self.pages=0
            search_input = self.driver.find_element_by_xpath(
                '//*[@id="lst-ib"]')
            search_input.clear()
            search_input.send_keys(brand)
            search_input.send_keys(Keys.ENTER)
            sleep(2)

            print('grabbing reviews......')
            print(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
            curr_links = self.total_links
            last_thread = None
            log = [brand]

            while True:

                try:
                    elements = self.driver.find_elements_by_xpath(
                        '//*[@class="sh-dlr__list-result"]')
                except Exception as e:
                    continue
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
                try:
                    if self.pages<=9:
                        next_button = self.driver.find_element_by_xpath(
                            '//*[@id="pnnext"]')
                        self.pages+=1
                        sleep(3)
                        self.driver.execute_script("arguments[0].click();", next_button)

                    else:
                        break

                except:
                    break
                continue

    def get_data(self, div, excel, excel_dump):
        soup = BeautifulSoup(div, 'lxml')
        attributes = []

        try:
            content = soup.select_one(".eIuuYe > a")
            if content is not None:
                attributes.append("https://www.google.com" + str(content.get("href")))
                if not str(content.get("href")).__contains__("shopping"):
                    return
                attributes.append(content.getText())
                print(content.getText())
            else:
                attributes.append("NA")
        except:
            traceback.print_exc()
            attributes.append("NA")
            pass
        try:
            content = soup.select_one(".eWxN4b")
            if content is not None:
                print(content.getText().strip())
                attributes.append(content.getText().strip())
            else:
                attributes.append("NA")
        except:
            attributes.append("NA")
            pass
        self.total_links = self.total_links + 1
        print("Total Number of reviews : " + str(self.total_links))
        # print("Total Number of exp : " + str(self.total_exp))
        row = attributes
        if row and not self.match_product_name(row[1]):
            excel_dump.insert_row(getattr(excel_dump, "wb"), row)
        else:
            excel.insert_row(getattr(excel, "wb"), row)
