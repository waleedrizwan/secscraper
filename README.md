# About
This script extracts insider trading data from the Securities and Exchange Commission (SEC) website for a set of pre-defined companies, and saves it in an Excel file.

The script uses the requests library to make HTTP requests and the BeautifulSoup library to parse the response HTML content. It also employs the concurrent.futures module to process multiple HTTP requests concurrently using threads, and the pandas library to create and write a pandas DataFrame to an Excel file.

The main steps of the script include:

1. Defining a dictionary of company CIK codes and the base URL and headers for making HTTP requests.

2. Defining functions to scrape data for each company, to scrape the list of filing folders for a company, and to process the content of each filing folder.

3. Looping through the companies, and calling the function to scrape data for each company.

4. Writing the extracted data to an Excel file.


# How to use 
1. Clone Repo
2. Install dependencies using "pip install  -r requirements.txt"
3. Run "python Scrape.py"
4. Wait approx 4 min for scraping to complete
5. Open Insider_Transactions.xls which will appear in the same directory