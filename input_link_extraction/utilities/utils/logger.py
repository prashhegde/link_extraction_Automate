import datetime
from input_link_extraction.utilities.xls_generator import *


class LogJ:
    log_file_name = ''
    wg = ''
    wb = ''
    PATH_OUTPUT = "C:/Users/Prash/Desktop/Work/scrapj-new/scrapj/data/output/log/"

    def __init__(self, website, log_type, path=None):
        if path:
            self.PATH_OUTPUT = "C:/Users/Prash/Desktop/Work/scrapj-new/scrapj/data/output/log/"
        self.log_file_name = log_type + "_" + str(
            datetime.datetime.utcnow().strftime('%Y-%m-%d-%H;%M;%S.%f')[:-3]) + "_" + website
        self.wg = Excel(self.log_file_name, path=self.PATH_OUTPUT)
        self.wb = getattr(self.wg, "wb")
        self.wg.add_headers(self.wb.active, ["NAME", "URL", "No Of Reviews Scrapped"])

    def log(self, text_list):
        self.wg.insert_row(self.wb, text_list)

        while True:
            try:
                self.wg.save_xls(self.wb)
                break
            except Exception as e:
                print(e)
