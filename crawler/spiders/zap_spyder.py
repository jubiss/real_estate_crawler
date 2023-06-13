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
class ZapSpider(scrapy.Spider):
    name='zap'
    tipo_venda = 'aluguel'
    estado = 'pe'
    cidade = 'recife'
    page = 1

    custom_settings = {
        'ROBOTSTXT_OBEY': False,    # Disable obeying robots.txt rules
        'DOWNLOAD_DELAY': 2,        # Set a delay of 2 seconds between requests
    }

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://www.example.com',
            }
        self.html_directory_path = self.set_html_directory()
        url = f"https://www.zapimoveis.com.br/aluguel/apartamentos/pe+recife/"
        yield SeleniumRequest(
            url=url,
            callback=self.parse,
            wait_time=1,
            headers=headers
        )
    def parse(self, response):
        driver = response.meta['driver']

        while self.page < 3:
            yield from self.scrap_page(response)
            next_button = driver.find_element(By.XPATH, '/html/body/main/section/div[1]/div[3]/div[2]/ul/li[7]/button')
            driver.execute_script("arguments[0].click();",next_button)

            self.wait_for_page_load(10)
            # Get the updated page source
            page_source = driver.page_source
            response = HtmlResponse(url=driver.current_url, body=page_source, encoding='utf-8')
            self.page += 1

    def scrap_page(self, response):
        self.save_html_in_folder(response)

        apartments = response.css('div.listings__container').css('div.card-listing.simple-card')  
        for apartment in apartments:
            
            # descricao
            description = apartment.css('span.simple-card__text.text-regular::text').get()
            description = str(description.replace('-', ' ').replace('\n', '')) if description else 'Vazio'
    
            # endereco
            address = apartment.css('h2.simple-card__address.color-dark.text-regular::text').get()
            if address:
                address = address.replace('\n', '').replace('  ', '')
            else:
                address = 'Não disponivel'

            # tamanho
            area = apartment.css('span[itemprop="floorSize"]::text').get()
            area = area.replace(' ', '').replace('\n', '').replace('m²', '') if area else '0'

            # quartos
            rooms = apartment.css('span[itemprop="numberOfRooms"]::text').get()
            rooms = rooms.replace(' ', '').replace('\n', '') if rooms else '0'

            # banheiros
            bathrooms = apartment.css('span[itemprop="numberOfBathroomsTotal"]::text').get()
            bathrooms = bathrooms.replace(' ', '').replace('\n', '') if bathrooms else '1'
    
            bathrooms = ' '.join(apartment.css('.property-card__detail-bathroom .js-property-card-value::text').getall()).strip()
            garages = ' '.join(apartment.css('.property-card__detail-garage .js-property-card-value::text').getall()).strip()

            # vagas
            garages = apartment.css('li.feature__item.text-small.js-parking-spaces::text').get()
            garages = (garages.replace(' ', '').replace('\n', '')) if garages else '0'

            # Valor
            rent = apartment.css('p.simple-card__price.js-price.color-darker.heading-regular.heading-regular__bolder.align-left::text').get()
            rent = rent.replace('R$', '').replace('\n', '').replace('.', '') if rent else '0'
    
            # condominio
            condominio = apartment.css('li.card-price__item.condominium.text-regular::text').get()
            condominio = condominio.replace('condomínioR$', '').replace(' ', '').replace('.', '') if condominio else '0'

            # Extract amenities
            amenities = 'Nulo' #apartment.css('.amenities__item::text').getall()
            
            # Extract property images
            images = apartment.css('.property-card__image::attr(src)').getall()
            
            # Extract ad link
            #link = 'www.vivareal.com.br' + apartment.css('a::attr(href)').get()
            link = 'unknown'
            # IPTU
            iptu = apartment.css('li.card-price__item.iptu.text-regular::text').get()
            iptu = iptu.replace('R$', '').replace('\n', '').replace('.', '').replace('IPTU', '').replace(' ', '') if iptu else '0'

            # tipo
            tipo = apartment.css('small::text').get()
            tipo = str(tipo) if tipo else 'Nenhuma'

            title = f'Apartamento com {str(rooms)} para alugar , 25m - {address}'

            # tipo
            tipo = apartment.css('small::text').get()
            tipo = str(tipo) if tipo else 'Nenhuma'

            # suite
            if re.search("suite|suíte|suites|suítes", description.lower()):
                suite = int(1)
            else:
                suite = int(0)

            # acabamento
            if re.search("porcelanato|ceramica|cerâmica|cerâmico|cerâmicos|gesso|antiderrapante|planejado", description.lower()):
                acabamento = int(1)
            else:
                acabamento = int(0)

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
                scraped_site='ZapImoveis'
            )
            yield item

    def wait_for_page_load(self, seconds):
        import time
        time.sleep(seconds)

    def set_html_directory(self):
        parent_dir = fr"{crawler_path}\spyder_html\zap_imoveis_html\{self.tipo_venda}\{self.estado}\{self.cidade}"
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


#//*[@id="app"]/section/div[1]/div[3]/div[2]/div/div[1]/div/div[1]/div[2]
#//*[@id="app"]/section/div[1]/div[3]/div[2]/div/div[2]/div/div[1]/div[2]