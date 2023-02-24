# About
Scrapes Form 4 data from the SEC site. Creates an Excel file containing summarized data for easy viewing. Run time varies with total # of companies and # of folders.

Sample output folder contains a previously generated file.

Max # of threads is kept at 4 to avoid rate limit of 10 requests/second.

A slower connection may be able to higher # of threads.

Tested and working at 4 threads.

# How to use 
- Clone Repo
- Install dependencies
- Run Scrape.py
- Open Insider_Transactions.xls in the same directory





