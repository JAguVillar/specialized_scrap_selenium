from selenium import webdriver
from selenium.webdriver.common.by import By

import pandas as pd

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach', True)

driver = webdriver.Chrome(options=chrome_options)

li_tags = driver.find_elements(By.TAG_NAME, value='article')

num_scrolls = 5
scroll_height = 500
data = []

driver.get('https://www.specialized.com/ar/es/c/bikes?page=1')
main_div = driver.find_element(By.ID, value='PlpWrapper')
pagination = main_div.find_element(By.XPATH, value='following-sibling::section')
number_of_pages = pagination.find_element(By.TAG_NAME, value='ul')
pages = number_of_pages.find_elements(By.TAG_NAME, value='li')
print(pages)

total_pages = len(pages)
print(total_pages)

page = 1
while page <= 3:
    for i in li_tags:
        # Scroll down by the specified height
        driver.execute_script(f"window.scrollBy(0, {scroll_height});")

        # Wait for a brief moment to allow lazy loading to occur
        driver.implicitly_wait(2)

        producto = i.find_element(By.TAG_NAME, value='h3')

        precio = i.find_element(By.XPATH, value='//*[@id="PlpWrapper"]/section[3]/ul/li[1]/article/div/div[2]/span')

        img_tags = i.find_elements(By.TAG_NAME, value='img')
        article_url = i.find_element(By.XPATH, value='//*[@id="PlpWrapper"]/section[3]/ul/li[1]/article/div/a[1]')
        url = article_url.get_attribute('href')
        print(url)

        data.append({'Producto': producto.text, 'Precio': precio.text, 'Enlace': url})
        print(data)
    page =page +1
    driver.get('https://www.specialized.com/ar/es/c/bikes?page='+str(page))
    driver.implicitly_wait(5)

# Create a DataFrame from the scraped data
df = pd.DataFrame(data)

# # Export the DataFrame to an Excel file
excel_filename = "scraped_data.xlsx"
df.to_excel(excel_filename, index=False)
driver.quit()

