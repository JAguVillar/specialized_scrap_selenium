from selenium import webdriver
from selenium.webdriver.common.by import By

import pandas as pd

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach', True)

driver = webdriver.Chrome(options=chrome_options)
driver.get('https://www.specialized.com/ar/es/c/bikes')

li_tags = driver.find_elements(By.TAG_NAME, value='article')

num_scrolls = 5
scroll_height = 500
data = []

for i in li_tags:
    imagenes = []

    # Scroll down by the specified height
    driver.execute_script(f"window.scrollBy(0, {scroll_height});")

    # Wait for a brief moment to allow lazy loading to occur
    driver.implicitly_wait(2)

    producto = i.find_element(By.TAG_NAME, value='h3')
    print(producto.text)
    precio = i.find_element(By.XPATH, value='//*[@id="PlpWrapper"]/section[3]/ul/li[1]/article/div/div[2]/span')
    print(precio.text)
    img_tags = i.find_elements(By.TAG_NAME, value='img')
    for img in img_tags:
        url = img.get_attribute('src')
        imagenes.append(url)
        print(imagenes)
    data.append({'Producto': producto.text, 'Precio': precio.text, 'Imagenes': '\n'.join(imagenes)})


# Create a DataFrame from the scraped data
df = pd.DataFrame(data)

# # Export the DataFrame to an Excel file
excel_filename = "scraped_data.xlsx"
df.to_excel(excel_filename, index=False)
driver.quit()

