
import csv
import requests
from bs4 import BeautifulSoup
import urllib.parse
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
    for link in links:
        href = link.get('href')
        if href:
            for domain in social_domains:
                if domain in href:
                    output_links.append(urllib.parse.urljoin(url, href))
                    break

# select output folder
output_folder_path = filedialog.askdirectory(title="Select Output Folder")

# write output links to a CSV file
output_file_path = output_folder_path + '/output_links.csv'
with open(output_file_path, 'w', newline='') as output_file:
    writer = csv.writer(output_file)
    for link in output_links:
        writer.writerow([link])
