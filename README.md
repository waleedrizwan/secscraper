## About
Extracts insider trading data from the Securities and Exchange Commission (SEC) website for a set of pre-defined companies, and saves it in an Excel file.

**`scrape.py`** uses the requests library to make HTTP requests and the BeautifulSoup library to parse the response HTML content. It also employs the concurrent.futures module to process multiple HTTP requests concurrently using threads, and the pandas library to create and write a pandas DataFrame to an Excel file.

**`visualize.py`** plots the historical stock prices and insider transactions for a list of stocks using the yfinance, pandas, and matplotlib libraries. 

## Companies
- To add or remove companies modify the **`companies`** dictionary to include ticker symbol and CIK

## Rate Limit 
- **`scrape.py`** uses multithreading to reduce runtime
- The global variable **`max_threads`** defines the number of threads to be used
- Fluctuations in network speed can lead to exceeding the rate limit of 10 requests/second
- In this case wait 10 minutes before running again and try reducing **`max_threads`** by 1
- Each additional request before the 10 minute cooldown is finished increases it by another 10 minutes
- Mulithreading can be eliminated by calling **`scrape_all_filing_folders()`** in **`scrape_data_for_company()`**

## Folder Count Command Line Argument
- Each company has a folders page which contains all files relating to every SEC filing made 
- This script allows you to choose the number of folders you would like to scrape as a command line argument
- **100** folders goes back approx 1 year
- It is possible to scrape every SEC filing for each company but this will drastically increase runtime 
- To scrape all filings on record, call **`scrape_all_filing_folders()`** on the full folders list

## How To Use 
1. Clone Repo
2. Install dependencies using **`pip install  -r requirements.txt`**
3. Run **`python scrape.py n`**, where **`n`** is the number of folders that will be scraped per company (100 for test)
4. Wait until the script has finished executing
5. All data scraped will be visible in **`Insider_Transactions.xlsx`** which will appear in the same directory

## How To Visualize Data
1. Run **`python visualize.py`** 
2. Graphs will pop up in a seperate window
