# About
Scrapes Form 4 data from the SEC site and creates an Excel file with the data for easy viewing.

Run time varies with total # of companies and # of folders. 

Takes approx 4 minutes to run given current company list.

Line 58 can be modified to scrape every single report ever filed on record

Max # of threads is kept at 4 to avoid rate limit of 10 requests/second.

# How to use 
- Clone Repo
- Install dependencies using "pip install  -r requirements.txt"
- Run "python Scrape.py"
- Wait approx 4 min for scraping to complete
- Open Insider_Transactions.xls which will appear in the same directory