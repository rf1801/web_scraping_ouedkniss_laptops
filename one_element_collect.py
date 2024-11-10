from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd

links_of_products_csv= "scraped_links.csv"

def collect_product_data(link):
    driver = webdriver.Chrome()
    driver.get(link)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    description_element = soup.find(class_="v-row v-row--dense")
    if description_element:
        description = description_element.get_text(strip=True)
        description = description[description.find("Référence") + len("Référence"):]
    else:
        description = None

    price_element = soup.find(class_="mr-1")
    if price_element:
        price = price_element.get_text(strip=True)
    else:
        price = None


    elements = soup.find_all("span", class_="me-1 mb-1")

    data = []
    data.append(price)
    if elements:
        for element in elements:
            data.append(element.get_text(strip=True))
    else:
        data.append(None)

    data.append(description)


    df = pd.DataFrame([data])

    # Append the row to the CSV file without headers or indexes
    df.to_csv("laptop_details.csv", mode='a', index=False, header=False)

    driver.quit()


df = pd.read_csv("scraped_links.csv", usecols=[0])
base_url="https://www.ouedkniss.com"
for i in range(1536,len(df)):
    url=base_url+df.iloc[i,0]
    collect_product_data(url)
    print("item ",i," is done")





