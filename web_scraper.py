import re
import requests
from bs4 import BeautifulSoup
import mysql.connector
import csv
import pandas as pd

# Database configuration
db_config = {
    'user': 'root',
    'password': 'password',
    'host': 'localhost',
    'database': 'web_scraping'
}

# Function to read URLs from an Excel file
def read_urls_from_excel(file_path):
    df = pd.read_excel(file_path)
    return df['URL'].tolist()

# Function to read URLs from a text file
def read_urls_from_text_file(file_path):
    with open(file_path, 'r') as file:
        urls = file.read().splitlines()
    return urls

# Connect to the MySQL database
db_connection = mysql.connector.connect(**db_config)
cursor = db_connection.cursor()

# Regex patterns for extracting email and phone numbers
email_pattern = re.compile(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})')
phone_pattern = re.compile(r'(\+?\d{1,3}[\s.-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}|\d{3}[\s.-]?\d{4}[\s.-]?\d{4}')

# Function to extract information from a website
def extract_info(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract email
        email = None
        email_match = email_pattern.search(soup.text)
        if email_match:
            email = email_match.group(0)
        
        # Extract phone number
        phone = None
        phone_match = phone_pattern.search(soup.text)
        if phone_match:
            phone = phone_match.group(0)
        
        # Extract address
        address = None
        address_tag = soup.find('address')
        if address_tag:
            address = address_tag.get_text(strip=True)
        else:
            # Search for address in <p>, <div>, or <span> tags with address-related keywords
            possible_address_tags = soup.find_all(['p', 'div', 'span'], string=re.compile(r'address|location|contact', re.I))
            for tag in possible_address_tags:
                text = tag.get_text(strip=True)
                # Assuming addresses are longer than 10 characters and contain specific keywords
                if len(text) > 10 and re.search(r'\d{1,5}\s\w+.*', text):
                    address = text
                    break
        
        # Extract language
        language = soup.find('html').get('lang', None)
        
        # Extract CMS/MVC (Based on meta generator tag or common keywords)
        cms_mvc = None
        generator_meta = soup.find('meta', attrs={'name': 'generator'})
        if generator_meta:
            cms_mvc = generator_meta.get('content')
        if not cms_mvc:
            if 'wp-content' in response.text:
                cms_mvc = 'WordPress'
            elif 'Drupal' in response.text:
                cms_mvc = 'Drupal'
            # Add more CMS/MVC detection as needed
        
        # Categorize website (Based on certain keywords in meta tags or content)
        category = None
        if 'blog' in response.text:
            category = 'Blog'
        elif 'ecommerce' in response.text or 'shop' in response.text:
            category = 'E-commerce'
        # Add more category detection as needed
        
        # Insert data into MySQL database
        insert_query = """
            INSERT INTO website_info (url, contact_email, contact_address, contact_number, language, cms_mvc, category)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (url, email, address, phone, language, cms_mvc, category))
        db_connection.commit()
    
    except Exception as e:
        print(f"Error scraping {url}: {e}")

# Main function
def main():
    def ensure_https(urls):
        return ["https://" + url if not url.startswith("http://") and not url.startswith("https://") else url for url in urls]

    file_type = int(input("Enter the file type\n1. Excel file\n2. Text file\n3. List of URLs: "))
        
    if file_type == 1:
        file_path = input("Enter the file path: ").strip()
        websites = read_urls_from_excel(file_path)
        websites = ensure_https(websites)
    elif file_type == 2:
        file_path = input("Enter the file path: ").strip()
        websites = read_urls_from_text_file(file_path)
        websites = ensure_https(websites)
    elif file_type == 3:
        url_num = int(input("Enter the number of URLs you want to enter: "))
        urls = []
        for i in range(url_num):
            url = input(f"Enter the {i+1} URL: ").strip()
            urls.append(url)
        print("These are the URLs you have given,\n", urls)
        websites = ensure_https(urls)
    else:
        print("Invalid file type. Please enter either 'Excel file', 'Text file' or 'List of URLs'.")
        return
    
    # Scrape each website
    for website in websites:
        extract_info(website)
    
    # Export results to CSV
    cursor.execute("SELECT * FROM website_info")
    rows = cursor.fetchall()
    with open('website_info.csv', 'w', newline='') as csvfile:
        fieldnames = ['id', 'url', 'contact_email', 'contact_address', 'contact_number', 'language', 'cms_mvc', 'category']
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)
        writer.writerows(rows)
    
    # Close the database connection
    cursor.close()
    db_connection.close()

if __name__ == "__main__":
    main()