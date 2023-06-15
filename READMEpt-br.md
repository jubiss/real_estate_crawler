README - Projeto Scraper de Sites Imobiliários


[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/jubiss/real_estate_crawler/blob/master/README.md)
![Em progresso](https://img.shields.io/badge/status-em%20progresso-yellow.svg)

## Índice

- [Instalação](#instalação)
- [Uso](#uso)
- [Requisitos do Sistema](#requisitos-do-sistema)
- [Estrutura do Projeto](#estrutura-do-projeto)

## Instalação

1. Crie um ambiente virtual para o projeto:

```shell
python -m venv real_estate
```

2. Ative o ambiente virtual:

- No Linux/macOS:

```shell
source real_estate/bin/activate
```

- No Windows (PowerShell):

```shell
real_estate\Scripts\Activate.ps1
```

3. Instale as dependências do projeto a partir do arquivo `requirements.txt`:

```shell
pip install -r requirements.txt
```

## Uso

Para realizar o scrape, siga as etapas abaixo:

1. Navegue até a pasta `crawler`:

```shell
cd crawler
```

2. Execute o comando padrão do Scrapy para iniciar o scrape de um site específico:

```shell
scrapy crawl [nome_do_scraper] -O [nome_do_arquivo_para_guardar_as_informacoes.formato]
```

- Exemplo:

```shell
scrapy crawl viva_real -O data.json
```

3. Alternativamente, você pode usar o script bash `fast_crawl.sh` para automatizar o processo:

```shell
bash fast_crawl.sh
```

Este script assume que você possui um ambiente virtual chamado `real_estate`.

## Requisitos do Sistema

Certifique-se de que os seguintes requisitos estejam atendidos:

- itemadapter==0.3.0
- pandas==2.0.1
- Scrapy==2.8.0
- scrapy_selenium==0.0.7
- python==3.8.16

## Estrutura do Projeto

O projeto segue a estrutura padrão de arquivos do Scrapy, com as seguintes adições:

- Arquivo `spider_html`: Guarda os arquivos HTML obtidos durante o scraping.
- Pasta `saved_json`: Armazena os arquivos JSON gerados durante o processo de scraping.

A estrutura do projeto é a seguinte:

```
projeto_scraper/
  |-- crawler/
        |-- scrapy.cfg
        |-- crawler/
              |-- __init__.py
              |-- items.py
              |-- middlewares.py
              |-- pipelines.py
              |-- settings.py
              |-- spiders/
                    |-- __init__.py
                    |-- viva_real.py
              |-- spider_html/
              |-- saved_json/
```
