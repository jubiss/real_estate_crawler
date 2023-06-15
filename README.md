README - Real Estate Websites Scraper

[![pt-br](https://img.shields.io/badge/lang-pt--br-green.svg)](https://github.com/jubiss/real_estate_crawler/blob/master/READMEpt-br.md)
[![Em progresso](https://img.shields.io/badge/status-in%20progress-yellow.svg)](README_pt-br.md)

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [System Requirements](#system-requirements)
- [Project Structure](#project-structure)

## Installation

1. Create a virtual environment for the project:

```shell
python -m venv my_virtual_environment
```

2. Activate the virtual environment:

- On Linux/macOS:

```shell
source my_virtual_environment/bin/activate
```

- On Windows (PowerShell):

```shell
my_virtual_environment\Scripts\Activate.ps1
```

3. Install the project dependencies from the `requirements.txt` file:

```shell
pip install -r requirements.txt
```

## Usage

To perform the scrape, follow the steps below:

1. Navigate to the `crawler` folder:

```shell
cd crawler
```

2. Run the default Scrapy command to start scraping a specific website:

```shell
scrapy crawl [spider_name] -O [output_filename.format]
```

- Example:

```shell
scrapy crawl viva_real -O data.json
```

3. Alternatively, you can use the `fast_crawl.sh` bash script to automate the process:

```shell
bash fast_crawl.sh
```

This script assumes you have a virtual environment named `real_estate`.

## System Requirements

Make sure the following requirements are met:

- itemadapter==0.3.0
- pandas==2.0.1
- Scrapy==2.8.0
- scrapy_selenium==0.0.7
- python==3.8.16

## Project Structure

The project follows the standard Scrapy file structure with the following additions:

- `spider_html` file: Stores the HTML files obtained during the scraping process.
- `saved_json` folder: Stores the generated JSON files during the scraping process.

The project structure is as follows:

```
project_scraper/
  |-- crawler/
        |-- scrapy.cfg
        |-- project_scraper/
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
