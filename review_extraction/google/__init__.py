from random import randint
from time import sleep
from openpyxl import load_workbook
from datetime import datetime
import _thread
from bs4 import BeautifulSoup

TAG = "google"
PATH_INPUT = "../data/input/"


class Google():
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
        wb = load_workbook(filename=PATH_INPUT + 'www.google.com.xlsx', read_only=True)
        ws = wb[wb.get_sheet_names()[0]]
        excel.add_headers(excel.wb.active,
                          ["Title", "Comments", "Rating", "Comfort", "Vision", "Value for", "Author", "Date", "Pros", "Cons", "Original Source",
                           "Reply from Acuvue", "Product Name", "Product Link", "Website"])
        for row in ws.rows:
            for cell in row:
                if str(type(cell)).__eq__("<class 'openpyxl.cell.read_only.ReadOnlyCell'>") and cell.row != 1: #cell.row != 1:
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
                            # for a in self.driver.find_elements_by_xpath('//*[@class ="internal-link JKlKAe Ba4zEd"]'):
                            #     if str(a.get_attribute("innerHTML")).strip().lower().__contains__("review"):
                            #         # print(next_button.get_attribute("innerHTML"))
                            #         self.driver.execute_script("arguments[0].click();", a)
                            #         sleep(1)
                            #         break
                            self.grab_reviews(excel, row[1].value, self.driver.current_url)

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
        global prev_div
        prev_div = ''
        i = 0
        temp_product_url = product_url
        try:
            product_name = self.driver.find_element_by_xpath('//*[@class="sh-t__title sh-t__title-pdp translate-details-content"]')
            product_name = str(product_name.get_attribute("innerHTML")).strip()
            # while len(self.driver.find_elements_by_xpath('//*[@id="sh-fp__pagination-button-wrapper"]/button'))>0:
        except:
            print("Error getting product name")
            pass
        loopcount=0
        while loopcount<50:#50
            try:
                self.driver.find_elements_by_xpath('//*[@id="sh-fp__pagination-button-wrapper"]/button')[0].click()
                sleep(randint(1,3))
                loopcount+=1
            except Exception as e:
                print(e)
                break
            
            
        elements = self.driver.find_elements_by_xpath('//*[@id="sh-rol__reviews-cont"]/div')
        print("Number of elements found : " + str(len(elements)))
        for div in elements:
            # cur_div = div.get_attribute("innerHTML")
            # if prev_div.__eq__(cur_div):
            #     print("Prev = Curr")
            #     return
            # try:
            _thread.start_new_thread(self.thread_process,(div.get_attribute("innerHTML"), product_name, temp_product_url, excel))
            # except:
            #     self.total_exp += 1
            #     print("Error: unable to start thread")
        # prev_div = elements[0].get_attribute("innerHTML")
        # next_button = self.driver.find_element_by_xpath('//*[@id="reviews-next-btn"]')
        # print(next_button.get_attribute("innerHTML"))
        # self.driver.execute_script("arguments[0].click();", next_button)
        # sleep(1)
        # print("Page No: " + str(i))
        # temp_product_url = str(product_url).split('&sa=')[0] + ",rstart:" + str(i)
        # self.get_page(temp_product_url)

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
        titlecontent=None
        titlecontentval=None
        try:
            titlecontent = soup.select_one(".P3O8Ne.less-spaced")
            if titlecontent is not None:
                titlecontentval=titlecontent.getText()
        except Exception as e:
            print(e)
            pass
        try:
            titlecontent = soup.select_one("._-hE.less-spaced")
            if titlecontent is not None:
                titlecontentval=titlecontent.getText()
        except Exception as e:
            print(e)
            pass
        try:
            if titlecontentval is not None:
                print(titlecontentval)
                attributes.append(titlecontentval)
            else:
                attributes.append("NA1")
        except Exception as e:
            print(e)

            pass
        commentcontent=None
        commentcontentval=None
        try:
            commentcontent = soup.select_one(".g1lvWe>div")
            if commentcontent is not None:
                commentcontentval=commentcontent.getText()
        except Exception as e:
            print(e)
            pass
        try:
            commentcontent = soup.select_one("._-hD>div")
            if commentcontent is not None:
                commentcontentval=commentcontent.getText()
        except Exception as e:
            print(e)
            pass
        try:
            if commentcontentval is not None:
                print(commentcontentval)
                attributes.append(commentcontentval)
            else:
                attributes.append("NA2")
        except Exception as e:
            print(e)
            pass

        # Ratings
        ratingcontent=None
        ratingcontentval=None
        try:
            ratingcontent = soup.select_one(".UzThIf")
            if ratingcontent is not None:
                ratingcontentval=ratingcontent.get('aria-label')[:-6]
        except Exception as e:
            print(e)
            pass
        try:
            ratingcontent = soup.select_one("._-jt")
            if ratingcontent is not None:
                ratingcontentval=ratingcontent.get('aria-label')[:-6]
        except Exception as e:
            print(e)
            pass
        try:
            if ratingcontentval is not None:
                print(ratingcontentval)
                attributes.append(ratingcontentval)
            else:
                attributes.append("NA3")
        except Exception as e:
            print(e)
            pass

        try:
            attributes.append("NA4")
        except:
            attributes.append("NA4")
            pass
        try:
            attributes.append("NA5")
        except:
            attributes.append("NA5")
            pass
        try:
            attributes.append("NA6")
        except:
            attributes.append("NA6")
            pass
        # Author
        authorcontent=None
        authorcontentval=None
        try:
            authorcontent = soup.select_one(".sPPcBf")
            if authorcontent is not None:
                authorcontentval=authorcontent.get_text()
        except Exception as e:
            print(e)
            pass
        try:
            authorcontent = soup.select_one("._-hF")
            if authorcontent is not None:
                authorcontentval=authorcontent.get_text()
        except Exception as e:
            print(e)
            pass
        try:
            if authorcontentval is not None:
                print(authorcontentval)
                attributes.append(authorcontentval)
            else:
                attributes.append("NA7")
        except Exception as e:
            print(e)
            pass

        # Date
        datecontent=None
        datecontentval=None
        try:
            datecontent = soup.select_one(".ff3bE.nMkOOb")
            if datecontent is not None:
                text_list = datecontent.get_text()
                datecontentval = datetime.strptime(text_list, '%B %d, %Y').strftime('%Y/%m/%d')
        except Exception as e:
            print(e)
            pass
        try:
            datecontent = soup.select_one("._-hN._-hL")
            if datecontent is not None:
                text_list = datecontent.get_text()
                datecontentval = datetime.strptime(text_list, '%B %d, %Y').strftime('%Y/%m/%d')
        except Exception as e:
            print(e)
            pass
        try:
            if datecontentval is not None:
                print(datecontent)
                # text_list = datecontent.get_text()
                # date = datetime.strptime(text_list, '%B %d, %Y').strftime('%Y/%m/%d')
                attributes.append(datecontentval)
            else:
                attributes.append("")
        except Exception as e:
            print(e)
            pass
        # pros
        try:
            attributes.append("NA8")
        except:
            attributes.append("NA8")
            pass
        # cons
        try:
            attributes.append("NA9")
        except:
            attributes.append("NA9")
            pass

        # OriginalSource
        OriginalSource=None
        OriginalSourceval=None
        try:
            OriginalSource = soup.select_one(".sPPcBf>span:nth-child(2)")
            if OriginalSource is not None:
                OriginalSourceval = OriginalSource.get_text()

        except Exception as e:
            print(e)
            pass
        try:
            OriginalSource = soup.select_one("._-hF>span:nth-child(2)")
            if OriginalSource is not None:
                OriginalSourceval = OriginalSource.get_text()
        except Exception as e:
            print(e)
            pass
        try:
            if OriginalSourceval is not None:
                print(OriginalSourceval)
                attributes.append(OriginalSourceval)
            else:
                attributes.append("NA10")
        except Exception as e:
            print(e)
            pass

        # Reply from Acuvue
        attributes.append("NA11")

        self.total_reviews = self.total_reviews + 1
        print("Total Number of reviews : " + str(self.total_reviews))
        print("Total Number of exp : " + str(self.total_exp))
        return attributes
