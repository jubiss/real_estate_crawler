from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date
import time
from scrapy.http import HtmlResponse

chromedriver_path = fr'C:\Users\jubi\Desktop\Projetos\Projetos_pessoais\real_estate\crawler\chromedriver.exe'

chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')

driver = webdriver.Chrome(service=Service(chromedriver_path), options=chrome_options)

url = "https://www.vivareal.com.br/aluguel/pernambuco/recife/"

driver.get(url)

page_source = driver.page_source
response_page_1 = HtmlResponse(url=driver.current_url, body=page_source, encoding='utf-8') 
next_button = driver.find_element(By.XPATH, '//*[@id="js-site-main"]/div[2]/div[1]/section/div[2]/div[2]/div/ul/li[9]/button')
driver.execute_script("arguments[0].click();",next_button)
# Wait for a brief moment to ensure the button is in view
time.sleep(5)

# Get the updated page source
page_source = driver.page_source
response = HtmlResponse(url=driver.current_url, body=page_source, encoding='utf-8')
breakpoint()

# Click the "Next page" button


# Close the browser
driver.quit()