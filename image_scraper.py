from typing import IO
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import io
from PIL import Image
import time

PATH = "chromedriver.exe"

wd = webdriver.Chrome(PATH)

def get_images(wd, delay, query, max_images):
    
    def scroll_down(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)

    url = f"https://www.google.com/search?q={query}&rlz=1C1YTUH_en-GBGB978GB978&sxsrf=AOaemvJ4ZeX0ulddZG9laXYL7SGVdJl_Cw:1635876732942&source=lnms&tbm=isch&sa=X&ved=2ahUKEwi-sMDco_rzAhWGqqQKHZrvBXgQ_AUoAXoECAEQAw&biw=1920&bih=961&dpr=1"
    wd.get(url)

    image_urls = set()
    skips = 0

    while len(image_urls) + skips < max_images:
        scroll_down(wd)

        thumbnails = wd.find_elements(By.CLASS_NAME, 'Q4LuWd')
        for img in thumbnails[len(image_urls) + skips: max_images]:
            try:
                img.click()
                time.sleep(delay)
            except:
                continue

            images = wd.find_elements(By.CLASS_NAME, 'n3VNCb')
            for image in images:
                if image.get_attribute('src') in image_urls:
                    max_images += 1
                    skips += 1
                    break
                if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                    image_urls.add(image.get_attribute('src'))
                    print("Found Image")

    return image_urls


def download_image(download_path, url, file_name):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = download_path + file_name

        with open(file_name, 'wb') as f:
            image.save(f, 'JPEG')
    except Exception as e:
        print('FAILED - ', e)

urls = get_images(wd, 2, 'cars', 5)
for i, url in enumerate(urls):
    download_image("images/", url, str(i) + '.jpg')

wd.quit()