import csv
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import pandas as pd

class Crawler:
    
    def get_linkedin_urls(self, company_names_file, linkedin_urls_file):
        # Read the company names from the CSV file
        company_names = pd.read_csv(company_names_file)['Company Name']

        # Initialize the output CSV file
        output_data = [['Company Name', 'LinkedIn URL']]

        # Launch the Playwright browser
        with sync_playwright() as p:
            browser = p.chromium.launch()

            # Create a new page
            page = browser.new_page()

            for company_name in company_names:
                # Search for the company on LinkedIn
                query = f'site:linkedin.com {company_name}'
                search_url = f'https://www.google.com/search?q={query}'

                page.goto(search_url)
                search_results = page.content()

                # Parse the HTML of the search results page
                soup = BeautifulSoup(search_results, 'html.parser')

                # Find the first LinkedIn URL in the search results
                linkedin_url = None
                link_tags = soup.find_all('a')
                for link in link_tags:
                    if 'linkedin.com/company' in link.get('href', ''):
                        linkedin_url = link.get('href')
                        break

                output_data.append([company_name, linkedin_url])

            # Save the LinkedIn URLs to the output CSV file
            with open(linkedin_urls_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(output_data)

            self.update_employee_count(company_names_file, linkedin_urls_file, browser)
            # Close the browser
            browser.close()

    def get_employee_count(self, linkedin_url, browser):
        
       
        page =  browser.new_page()
        page.goto(linkedin_url)
        employee_text =  page.inner_text('.self-center.link-no-visited-state')
        
        employee_text = employee_text.split(' ')
        for word in employee_text:
            try:
                employee_count = int(word)
            except:
                pass
        return employee_count

    def update_employee_count(self, company_names_file, linkedin_urls_file, browser):
        # Read the LinkedIn URLs from the CSV file
        df = pd.read_csv(linkedin_urls_file)

        # Add a new column for the employee count
        df['Employee Count'] = ''

        # Launch the Playwright browser
        
           
        for index, row in df.iterrows():
            linkedin_url = row['LinkedIn URL']

            # Skip rows without LinkedIn URLs
            if pd.isnull(linkedin_url):
                continue

            # Extract the employee count from LinkedIn
            employee_count = self.get_employee_count(linkedin_url, browser)
            df.at[index, 'Employee Count'] = employee_count
            

        df = df.drop(columns=['LinkedIn URL'])
        # Save the updated data to the output file
        df.to_csv(company_names_file.name, index=False)
            
           
