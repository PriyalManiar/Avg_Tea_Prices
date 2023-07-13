import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the Tea Board of India from where data is to be scraped
url_base = "https://www.teaboard.gov.in/WEEKLYPRICES/"

# function definition
def scrape_data():
    # creating an empty list to store the scraped data
    data = []

    # creating a loop from 2008 to 2023, where year values get appended to base url to retrieve data for all years 
    for year in range(2008, 2024):
        url_all = url_base + str(year)
        resp = requests.get(url_all)
        soup = BeautifulSoup(resp.content, 'html.parser')

        # finding the required table by its id  
        req_table = soup.find('table', {'id': 'contn_GridView2'})

        # checking if the table is found or not
        if req_table is not None:
            # extracting the header column from the table on the website
            row_header = req_table.find('tr')
            # skipping the week ending/date column; only extracting the column headers with location names
            headers = [header.text.strip() for header in row_header.find_all('th')][1:] 

            # extracting all table rows, skipping the header row
            rows = req_table.find_all('tr')[1:] 
            for row in rows:
                columns = row.find_all('td')
                date = columns[0].text.strip()

                # extracting the location and average price for each location
                for i, header in enumerate(headers):
                    location = header
                    avg_price = columns[i+1].text.strip()

                    # appending extracted columns to list
                    data.append([date, location, avg_price])

            print(f"Data is scraped data for {year}")
        else:
            print(f"No table found for {year}")

    # converting the list to a dataframe
    df = pd.DataFrame(data, columns=['date', 'location', 'avg_price'])

    # writing the dataframe into a csv
    df.to_csv('tea_avg_price.csv', index=False)
    print("Data written to tea_avg_price.csv successfully.")

# function call
scrape_data()
