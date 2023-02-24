import requests                  # Import the requests library for making HTTP requests
from bs4 import BeautifulSoup    # Import BeautifulSoup for parsing HTML content
import time                      # Import the time library for timing the script
import pandas as pd              # Import pandas library for creating a DataFrame and writing to Excel
import concurrent.futures        # Import the concurrent.futures module for multi-threading

# Set the maximum number of threads to use for multi-threading
max_threads = 4

# Define the company CIK codes
companies = {
    'TSLA': '0001318605',
    'AAPL': '0000320193',
    'AMZN': '0001018724',
    'MSFT': '0000789019',
    'GOOGL': '0001652044',
    'CSCO': '0000858877',
    'PYPL': '0001633917',
    'NFLX': '0001065280',
    'INTC': '0000050863',
    'AMD': '0000002488',
    
}

# Define the base URL and headers
base_url = "https://www.sec.gov/Archives/edgar/data/"
headers = {
    "Connection": "close",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
}

form_data = [] # Initialize an empty list to hold extracted data from SEC filings

def scrape_all_company_data(companies):
    # Loop through the companies
    for company, cik in companies.items():
        scrape_data_for_company(company, cik)
        
def scrape_data_for_company(company, cik):      
    print(f"Scraping company {company} with CIK {cik}")
    # Construct the URL for the company
    url = base_url + cik + "/"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error accessing company {company} at URL {url}: {e}")
        return
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find all the folders on the page and keep the first 100 for simplicity
    folders = soup.find("table").find_all("a", {"href": True, "id": False})[:100]
   
    # We can use a with statement to ensure threads are cleaned up promptly
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        # Submit a thread for each folder to scrape data from each folder concurrently
        future_to_folders = {executor.submit(scrape_all_filing_folders, company, url, folder): folder for folder in folders}
        # Process the futures as they complete
        for future in concurrent.futures.as_completed(future_to_folders):
            # Get the folder associated with the completed future
            folder = future_to_folders[future]
            try:
                future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (folder.get_text(), exc))
                   
def scrape_all_filing_folders(company, url, folder):                            
    # Get the text for the folder
    folder_text = folder.get_text()
    
    # each filing folder is numerical 
    try:
        # Construct the URL for the folder
        folder_url = url + folder_text
        
        # Access the folder URL and get its content
        response = requests.get(folder_url, headers=headers)
        response.raise_for_status()
        folder_content = BeautifulSoup(response.text, "html.parser")
        
    except requests.exceptions.RequestException as e:
        print(f"Error accessing folder {folder_url} for company {company}: {e}")
        return
    
    for link in folder_content.find("table").find_all("a", href=True):
            process_folder_content_link(company, folder_url, link)

def process_folder_content_link(company, folder_url, link):
    if "index.html" not in link.get_text():
        return 
                   
    # contains link to folder containing form 4
    filing_detail_folder = folder_url + "/"  + link.get_text()               
    response = requests.get(filing_detail_folder, headers=headers)
    response.raise_for_status()
    filing_detail_content = BeautifulSoup(response.text, "html.parser")

    for link in filing_detail_content.find_all("a", href=True):
        process_filing_detail(company, folder_url, link)


def process_filing_detail(company, folder_url, link):
    link_title = link.get_text() 
    should_process = ".xml" in link_title and ("doc4" in link_title or "form4" in link_title)
    if not should_process:
        return
                                                                                                
    form4_url = folder_url + "/" + link.get_text()
    
    try:
        response = requests.get(form4_url, headers=headers)
        response.raise_for_status()
        form_4_content = BeautifulSoup(response.text, "xml")
        non_derivative_table = form_4_content.find('nonDerivativeTable')
        non_derivative_transactions = non_derivative_table.find_all('nonDerivativeTransaction')
        current_transaction = {}

        for transaction in non_derivative_transactions:
            transaction_amounts = transaction.find('transactionAmounts') 
            security_title = transaction.find('securityTitle').find('value').get_text()
            transaction_date = transaction.find('transactionDate').find('value').get_text()            
            transaction_code = transaction.find('transactionCoding').find('transactionCode').get_text()
            transaction_shares = transaction_amounts.find('transactionShares').find('value').get_text()            
            transaction_price_per_share = transaction_amounts.find("transactionPricePerShare").find("value")

            if transaction_price_per_share is not None:
                transaction_price_per_share = transaction_price_per_share.get_text()

            else:
                transaction_price_per_share = ""

            if form_4_content.find("officerTitle") is not None:
                current_transaction["insiderTitle"] = form_4_content.find("officerTitle").get_text()
                
            else:
                current_transaction["insiderTitle"] = ""

            current_transaction["ticker"] = company 
            current_transaction["insiderName"] = form_4_content.find("rptOwnerName").get_text()                            
            current_transaction["securityType"] = security_title
            current_transaction["purchaseDate"] = transaction_date
            current_transaction["transactionCode"] = transaction_code
            current_transaction["numShares"] = transaction_shares
            current_transaction["pricePerShare"] = transaction_price_per_share
            current_transaction["formURL"] = form4_url

            if len(current_transaction) > 2:
                form_data.append(current_transaction) 
    except:  
        pass

def print_to_excel(data):
    # Create a pandas DataFrame from the extracted data
    df = pd.DataFrame(data)

    df = df[['purchaseDate', 'ticker', 'insiderName', 'insiderTitle', 'securityType', 'transactionCode', 'numShares', 'pricePerShare', "formURL"]]

    # Create an Excel writer object
    writer = pd.ExcelWriter('insider_transactions.xlsx')

    # Write the DataFrame to the excel file
    df.to_excel(writer, sheet_name='Insider Transactions', index=False)

    # Format the sheet to make it more readable
    workbook = writer.book
    worksheet = writer.sheets['Insider Transactions']
    header_format = workbook.add_format({'bold': True, 'border': 1, 'align': 'center', 'valign': 'vcenter'})
    cell_format = workbook.add_format({'border': 1, 'align': 'center', 'valign': 'vcenter'})
    worksheet.set_column('A:A', 25)
    worksheet.set_column('B:B', 15)
    worksheet.set_column('C:C', 25)
    worksheet.set_column('D:D', 15)
    worksheet.set_column('E:E', 20)
    worksheet.set_column('F:F', 10)
    worksheet.set_column('G:G', 15)
    worksheet.set_column('H:H', 15)
    worksheet.set_column('I:I', 100)
    worksheet.set_row(0, None, header_format)
    for row in range(1, len(df)+1):
        worksheet.set_row(row, None, cell_format)

    # Save the Excel file
    writer.save()

if __name__ == "__main__":
    start = time.time()
    scrape_all_company_data(companies)
    print_to_excel(form_data)
    end = time.time()
    #Subtract Start Time from The End Time
    total_time = end - start
    print("\n Total Runtime"+ str(total_time//60), " Minutes")