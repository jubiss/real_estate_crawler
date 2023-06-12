from pathlib import Path
import re
import os
import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from crawler.items import PropertyItem
from scrapy.http import HtmlResponse

crawler_path = r'C:\Users\jubi\Desktop\Projetos\Projetos_pessoais\real_estate\crawler\crawler'
class VivaSpider(scrapy.Spider):
    name='viva'
    tipo_venda = 'aluguel'
    estado = 'pernambuco'
    cidade = 'recife'
    page = 1

    def start_requests(self):
        self.html_directory_path = self.set_html_directory()
        url = f"https://www.vivareal.com.br/{self.tipo_venda}/{self.estado}/{self.cidade}/apartamento_residencial"
        yield SeleniumRequest(
            url=url,
            callback=self.parse,
            wait_time=1
        )
    def parse(self, response):
        driver = response.meta['driver']

        while self.page < 90:
            yield from self.scrap_page(response)
            next_button = driver.find_element(By.XPATH, '//*[@id="js-site-main"]/div[2]/div[1]/section/div[2]/div[2]/div/ul/li[9]/button')
            driver.execute_script("arguments[0].click();",next_button)

            self.wait_for_page_load(10)
            # Get the updated page source
            page_source = driver.page_source
            response = HtmlResponse(url=driver.current_url, body=page_source, encoding='utf-8')
            self.page += 1

    def scrap_page(self, response):
        self.save_html_in_folder(response)
        apartments = response.css('article.property-card__container.js-property-card')
        for apartment in apartments:
            title = ' '.join(apartment.css('.property-card__title::text').getall()).strip()
            address = ' '.join(apartment.css('.property-card__address::text').getall()).strip()
            area = ' '.join(apartment.css('.property-card__detail-area::text').getall()).strip()
            rooms = ' '.join(apartment.css('.property-card__detail-room .js-property-card-value::text').getall()).strip()
            bathrooms = ' '.join(apartment.css('.property-card__detail-bathroom .js-property-card-value::text').getall()).strip()
            garages = ' '.join(apartment.css('.property-card__detail-garage .js-property-card-value::text').getall()).strip()
            rent_html = apartment.css('.property-card__price').getall()[0].replace('.','')
            rent = re.search(r'R\$ (\d+)', rent_html).group(1) if rent_html else None
            condominio = apartment.css('.js-condo-price::text').getall()  
            # Extract amenities
            amenities = apartment.css('.amenities__item::text').getall()
            
            # Extract property images
            images = apartment.css('.property-card__image::attr(src)').getall()
            
            # Extract ad link
            link = 'www.vivareal.com.br' + apartment.css('a::attr(href)').get()

            item = PropertyItem(
                title=title,
                address=address,
                area=area,
                rooms=rooms,
                bathrooms=bathrooms,
                garages=garages,
                rent=rent,
                amenities=amenities,
                images=images,
                condominio=condominio,
                link=link,
                scraping_date=datetime.now().strftime('%Y-%m-%d'),
                scraped_site='VivaReal'
            )
            yield item

    def wait_for_page_load(self, seconds):
        import time
        time.sleep(seconds)

    def set_html_directory(self):
        parent_dir = fr"{crawler_path}\spyder_html\viva_real_html\{self.tipo_venda}\{self.estado}\{self.cidade}"
        directory = f'date_{datetime.now().strftime("%Y-%m-%d")}'
        path = os.path.join(parent_dir, directory)
        try:
            os.mkdir(path)
        except:
            pass
        return path

    def save_html_in_folder(self, response):
        filename = fr"{self.html_directory_path}\page_{self.page}_date_{datetime.now().strftime('%Y-%m-%d')}.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file: {filename}")