from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import threading
import traceback
from time import sleep
from datetime import datetime


class IDiscountContactLens:
    def __init__(self, website, brands, excel, excel_dump, driver, logging, match_product_name, get_page, total_links):
        get_page("http://" + website)
        self.logging = logging
        self.match_product_name = match_product_name
        self.brands = brands
        self.driver = driver
        self.total_links = total_links
        self.total_exp = 0

        for brand in self.brands:
            get_page("http://" + website)
            search_input = self.driver.find_element_by_xpath(
                '//*[contains(@class,"search-input")]')
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
                    elements = self.driver.find_elements_by_xpath(
                        '//*[contains(@class,"product-list list")]/div')
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
                try:
                    next_button = self.driver.find_element_by_xpath(
                        '//*[@class="icon-circle-right"]')
                    # print(load_more_button.get_attribute("innerHTML"))
                    self.driver.execute_script("arguments[0].click();", next_button)
                    sleep(1)
                except:
                    break
                continue

    def get_data(self, div, excel, excel_dump):
        soup = BeautifulSoup(div, 'lxml')
        attributes = []

        try:
            content = soup.select_one("a")
            if content is not None:
                attributes.append("https://www.discountcontactlenses.com" + str(content.get("href")))
            else:
                attributes.append("NA")
        except:
            traceback.print_exc()
            attributes.append("NA")
            pass
        try:
            content = soup.select_one(".shelf__panel--name")
            if content is not None:
                print(content.getText().strip())
                attributes.append(content.getText().strip())
            else:
                attributes.append("NA")
        except:
            attributes.append("NA")
            pass
        try:
            content = soup.select_one(".text-m")
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
