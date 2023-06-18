import xlsxwriter
import  pandas as pd
import bs4
import  requests
from bs4 import BeautifulSoup
from xlsxwriter import worksheet

titles = []
prices = []




page = requests.get(f"https://gamerall.com/module/hpp/ajax?p={1}&tab_id=16")
soup = BeautifulSoup(page.content, 'html.parser')
price = soup.find_all(class_="content_price price_container")
title  = soup.find_all(class_="name-product")

for tcounter in  title:
    span = tcounter.find('span')
    titles.append(span.string)


for prcounter in  price:
    pspan = prcounter.find('span')
    prices.append(pspan.string)

df = pd.DataFrame({'Items': titles,
                   'Price': prices,
                   })

writer = pd.ExcelWriter("data.xlsx", engine='xlsxwriter')


df.to_excel(writer, sheet_name='Sheet1', startrow=1, header=False, index=False)

workbook = writer.book
worksheet = writer.sheets['Sheet1']

(max_row, max_col) = df.shape

column_settings = []
for header in df.columns:
    column_settings.append({'header': header})

worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings})

# Make the columns wider for clarity.
worksheet.set_column(0, max_col - 1, 40)

writer._save()