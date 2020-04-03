from inputlinkextractor.google import IGoogle
from utils.logger import LogJ
from xls_generator import *
from time import sleep
from datetime import datetime
from random import randint
from inputlinkextractor.walgreens import IWalgreens
from inputlinkextractor.visiondirect import IVisionDirect
from inputlinkextractor.coastal import ICoastal
from inputlinkextractor.lensdiscounters import ILensdiscounters
from inputlinkextractor.lens import ILens
from inputlinkextractor.aclens import IAclens
from inputlinkextractor.walmart import IWalmart
from inputlinkextractor.discountcontactlenses import IDiscountContactLens
from inputlinkextractor.contactlensking import IContactLensKing
from inputlinkextractor.lensdirect import ILensDirect
from inputlinkextractor.getlens1800 import IGetLens1800
from inputlinkextractor.smartbuyglasses import ISmartBuyGlasses
from inputlinkextractor.framesdirect import IFramesDirect
from inputlinkextractor.webcontacts import IWebContacts
from inputlinkextractor.bestpricecontacts import IBestPriceContacts
import threading
from selenium import webdriver

TAG = "LinkExtractor"
PATH_INPUT = "../data/input/"


class LinkExtractor:
    driver = None
    last_thread = None
    total_links = 0
    total_exp = 0
    start_time = ''
    end_time = ''
    error_logger = LogJ(TAG, "ERROR", True)
    info_logger = LogJ(TAG, "INFO", True)
    websites = [ "www.webcontacts.com.au", "www.framesdirect.com",
                "www.smartbuyglasses.com", "www.1800getlens.com",
                "www.walgreens.com",
                "www.lensdiscounters.com",
                "www.visiondirect.co.uk",
                "www.google.com",
                "www.coastal.com",
                "www.lens.com",
                "www.aclens.com",
                "www.discountcontactlenses.com",
                "www.contactlensking.com",
                "www.lensdirect.com", "www.bestpricecontacts.com"
                ]
    websites = [
        "www.aclens.com",
        "www.discountcontactlenses.com",
        "www.contactlensking.com",
        "www.lensdirect.com", "www.bestpricecontacts.com"
    ]
    brands = ['Acuvue', 'Alcon', 'Bausch & Lomb', 'CooperVision']
    blacklisted_keys = ['systane', 'eye drop']

    def __init__(self, driver=None):
        self.driver = driver

    # Open headless chromedriver

    def start_driver(self):
        print('starting driver...')
        try:
            driver = webdriver.Chrome("../drivers/chromedriver.exe")
        except:
            try:
                driver = webdriver.Chrome("../drivers/chromedriver")
            except:
                print("No Driver")

        sleep(4)
        return driver


        # Close chromedriver\

    def close_driver(self, driver):
        print('closing driver...')
        driver.quit()
        print('closed!')

    def extract_data(self):

        start_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        self.driver = self.start_driver()

        for website in self.websites:
            excel = Excel(website, True)
            excel_dump = Excel("dumps/" + website + "_dump", True)
            wb = getattr(excel, "wb")
            excel.add_headers(excel.wb.active,
                              ["Product Link", "Product Name", "No. of Reviews"])
            excel_dump.add_headers(excel_dump.wb.active,
                                   ["Product Link", "Product Name", "No. of Reviews"])
            if website.__contains__("walgreens"):
                IWalgreens(website, self.brands, excel, excel_dump, self.driver, self.logging, self.match_product_name,
                           self.get_page, self.total_links)
            elif website.__contains__("getlens"):
                IGetLens1800(website, self.brands, excel, excel_dump, self.driver, self.logging,
                             self.match_product_name,
                             self.get_page, self.total_links)
            elif website.__contains__("google"):
                IGoogle(website, self.brands, excel, excel_dump, self.driver, self.logging, self.match_product_name,
                        self.get_page, self.total_links)
            elif website.__contains__("visiondirect"):
                IVisionDirect(website, self.brands, excel, excel_dump, self.driver, self.logging,
                              self.match_product_name,
                              self.get_page, self.total_links)
            elif website.__contains__("coastal"):
                ICoastal(website + "/contact-lenses", self.brands, excel, excel_dump, self.driver, self.logging,
                         self.match_product_name,
                         self.get_page, self.total_links)
            elif website.__contains__("aclens.com"):
                IAclens(website, self.brands, excel, excel_dump, self.driver, self.logging,
                        self.match_product_name,
                        self.get_page, self.total_links)
            elif website.__contains__("lens.com"):
                ILens(website, self.brands, excel, excel_dump, self.driver, self.logging,
                      self.match_product_name,
                      self.get_page, self.total_links)
            elif website.__contains__("walmart"):
                IWalmart(website, self.brands, excel, excel_dump, self.driver, self.logging,
                         self.match_product_name,
                         self.get_page, self.total_links)
            elif website.__contains__("lensdiscounters.com"):
                ILensdiscounters(website, self.brands, excel, excel_dump, self.driver, self.logging,
                                 self.match_product_name,
                                 self.get_page, self.total_links)
            elif website.__contains__("discountcontactlenses"):
                IDiscountContactLens(website, self.brands, excel, excel_dump, self.driver, self.logging,
                                     self.match_product_name,
                                     self.get_page, self.total_links)
            elif website.__contains__("www.contactlensking.com"):
                IContactLensKing(website, self.brands, excel, excel_dump, self.driver, self.logging,
                                 self.match_product_name,
                                 self.get_page, self.total_links)
            elif website.__contains__("lensdirect"):
                ILensDirect(website, self.brands, excel, excel_dump, self.driver, self.logging,
                            self.match_product_name,
                            self.get_page, self.total_links)
            elif website.__contains__("smartbuyglasses"):
                ISmartBuyGlasses(website, self.brands, excel, excel_dump, self.driver, self.logging,
                                 self.match_product_name,
                                 self.get_page, self.total_links)
            elif website.__contains__("framesdirect"):
                IFramesDirect(website, self.brands, excel, excel_dump, self.driver, self.logging,
                              self.match_product_name,
                              self.get_page, self.total_links)
            elif website.__contains__("webcontacts"):
                IWebContacts(website, self.brands, excel, excel_dump, self.driver, self.logging,
                             self.match_product_name,
                             self.get_page, self.total_links)
            elif website.__contains__("bestpricecontacts"):
                IBestPriceContacts(website, self.brands, excel, excel_dump, self.driver, self.logging,
                                   self.match_product_name,
                                   self.get_page, self.total_links)
            threading.Thread(target=self.save_excels, args=(excel, excel_dump)).start()
        print("Input Link Generation Start Time : " + start_time)
        print("Input Link Generation End Time : " + datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
        self.close_driver(self.driver)

    # Tell the browser to get a page
    def get_page(self, url):
        print('getting page...')
        start_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        print("Start Time" + start_time)
        self.driver.get(url)
        sleep(randint(2, 3))

    def logging(self, curr_links, log, last_thread):
        self.last_thread = last_thread
        while last_thread and last_thread.isAlive():
            pass
        log.append(self.total_links - curr_links)
        self.info_logger.log(log)

    def match_product_name(self, product_name):
        product_name = str(product_name).lower()
        wb = load_workbook(filename=PATH_INPUT + 'parameters.xlsx', read_only=True)
        ws = wb["Products"]

        for row in ws.rows:
            for cell in row:
                if str(type(cell)).__eq__("<class 'openpyxl.cell.read_only.ReadOnlyCell'>") and cell.row != 1:
                    if cell.column == 1:
                        name = str(cell.value).lower()
                        if product_name.__contains__(name):
                            for blacklist_key in self.blacklisted_keys:
                                if product_name.__contains__(blacklist_key):
                                    return False
                            return True
        return False

    def save_excels(self, excel, excel_dump):
        while self.last_thread and self.last_thread.isAlive():
            pass
        while True:
            try:
                excel.save_xls(excel.wb)
                excel_dump.save_xls(excel_dump.wb)
                break
            except Exception as e:
                print(e)
                pass


link_extractor = LinkExtractor()
link_extractor.extract_data()
