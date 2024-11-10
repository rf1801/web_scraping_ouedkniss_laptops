from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd

def scroll_to_end(mydriver):
    scroll_pause_time = 1  # Wait time after each scroll
    max_scrolls = 12  # Limit the number of scrolls in case it never fully loads
    previous_count = 0
    scroll_count = 0
    time.sleep(5)
    while scroll_count < max_scrolls:
        # Scroll down a small amount and then wait
        mydriver.execute_script("window.scrollBy(0, 1000);")  # Scroll down in smaller steps
        time.sleep(scroll_pause_time)
        scroll_count += 1

    time.sleep(2)

def extract_save_links(my_divs,save_csv):
    hrefs = []
    # Iterate over each div in the list
    for index, div in enumerate(my_divs):
        link_tag = div.find("a", href=True)
        if link_tag:
            hrefs.append(link_tag["href"])
        else:
            continue

    print(f"Total hrefs found: {len(hrefs)}")
    hrefs_df = pd.DataFrame(hrefs, columns=["URL"])
    hrefs_df.to_csv(save_csv, mode="a", index=False, header=False)
    print("Data appended to hrefs.csv")

url = "https://www.ouedkniss.com/informatique-ordinateur-portable/1?origin=STORE&hasPrice=true&priceRangeMin=10000"
csv_file="scraped_links.csv"
pages=60


def collect(source):
    driver = webdriver.Chrome()
    driver.get(source)
    scroll_to_end(driver)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    div_element = soup.find_all("div", class_="v-col-sm-6 v-col-md-4 v-col-lg-3 v-col-12")
    print(len(div_element))
    extract_save_links(div_element, csv_file)
    driver.quit()


for i in range(1,pages+1):
    url = f"https://www.ouedkniss.com/informatique-ordinateur-portable-laptop/{str(i)}?origin=STORE&hasPrice=true&priceRangeMin=10000"
    collect(url)
    print("page ",i, " done")


