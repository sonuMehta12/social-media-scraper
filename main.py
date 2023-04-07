
import csv
import requests
from bs4 import BeautifulSoup
import urllib.parse
import re
import phonenumbers
from phonenumbers import geocoder
import tkinter as tk
from tkinter import filedialog

# list of social media domains
social_domains = ['facebook.com', 'twitter.com', 'instagram.com', 'linkedin.com']

# select input CSV file
root = tk.Tk()
root.withdraw()
input_file_path = filedialog.askopenfilename(title="Select Input CSV File", filetypes=[("CSV Files", "*.csv")])

# read input links from CSV file
with open(input_file_path, 'r') as input_file:
    reader = csv.reader(input_file)
    input_links = [row[0] for row in reader]

# scrape social media links from each input link
output_links = []
for url in input_links:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all('a')
    output_link = {
        'domain name': '',
        'insta': '',
        'twitter': '',
        'facebook': '',
        'email': '',
        'linkedin': '',
        'phone number': ''
    }
    for link in links:
        href = link.get('href')
        if href:
            for domain in social_domains:
                if domain in href:
                    if 'facebook.com' in href:
                        output_link['facebook'] = href
                    elif 'twitter.com' in href:
                        output_link['twitter'] = href
                    elif 'instagram.com' in href:
                        output_link['insta'] = href
                    elif 'linkedin.com' in href:
                        output_link['linkedin'] = href
                    else:
                        continue

    email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    email = re.findall(email_pattern, soup.text)
    if email:
        output_link['email'] = email[0]

    phone_pattern = r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"
    phone_numbers = re.findall(phone_pattern, soup.text)
    if phone_numbers:
        phone_number = phonenumbers.parse(phone_numbers[0], "US")
        output_link['phone number'] = phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.NATIONAL)

    output_link['domain name'] = urllib.parse.urlparse(url).netloc
    output_links.append(output_link)

# select output folder
output_folder_path = filedialog.askdirectory(title="Select Output Folder")

# write output links to a CSV file in table format
output_file_path = output_folder_path + '/output_links.csv'
with open(output_file_path, 'w', newline='') as output_file:
    writer = csv.DictWriter(output_file, fieldnames=['domain name', 'insta', 'twitter', 'facebook', 'email', 'linkedin', 'phone number'])
    writer.writeheader()
    for link in output_links:
        writer.writerow(link)
