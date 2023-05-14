# WaybackMachine Scraper for business Data

This is a Scrapy spider that allows you to scrape web pages from the Wayback Machine for a given set of URLs. The project includes HTML parsing, XPath parsing, and redirect handling .

## Installation

1. Clone the repository:

```shell
git clone https://github.com/yd2333/WaybackMachine-Scraper-For-Business-Data.git
```

2. Navigate to the project directory:

```shell
cd value spider
```

3. Install the required dependencies:

```shell
pip install scrapy
pip install bs4
pip install pandas
pip install pymongo
```

## Usage

1. Open the `settings.py` file and configure the spider's settings according to your requirements.

2. Create a text file `urls.txt` and add one URL per line that you want to scrape from the Wayback Machine.

3. Run the spider:
start and end specify the (url,year) pair in a csv file. Scrapy spider is a program with a lot of blocking, so running multiple spider concurrently can help reducing overall running time.

```shell
scrapy crawl spider -a start=0 -a end=10000 -s LOG_FILE=spider.log
```

The scraped data will be saved in `spider.json` file.

## Features

- **HTML Parsing:** The spider uses Scrapy's built-in HTML parser to extract relevant data from web pages.

- **XPath Parsing:** XPath expressions are utilized to navigate and extract specific elements from the HTML structure.

- **Redirect Handling:** The spider handles redirects encountered during the scraping process, ensuring accurate data extraction.

## Acknowledgements

- The developers of Scrapy for providing an excellent web scraping framework.

- The Wayback Machine for archiving web pages and making historical data accessible.