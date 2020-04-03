from random import randint
from time import sleep
from openpyxl import load_workbook
from datetime import datetime
import _thread
from bs4 import BeautifulSoup
text_list="January 22, 2019"
text_list2="January 1, 2019"
date = datetime.strptime(text_list, '%B %d, %Y').strftime('%Y/%m/%d')
date2 = datetime.strptime(text_list2, '%B %d, %Y').strftime('%Y/%m/%d')
print(date-date2)