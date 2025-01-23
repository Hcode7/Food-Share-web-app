import os
import requests
from bs4 import BeautifulSoup

# Specify the URL of the website
url = 'https://tasty.co/'

# Send a GET request to the website
response = requests.get(url)

# Parse the HTML content of the page
soup = BeautifulSoup(response.text, 'html.parser')

# Find all image tags
img_tags = soup.find_all('img')

# Create a directory to save the images
os.makedirs('images', exist_ok=True)

# Loop through all image tags
for img_tag in img_tags:
    # Get the image source URL
    img_url = img_tag.get('src')
    
    # Ensure the URL is complete
    if not img_url.startswith(('http://', 'https://')):
        img_url = url + img_url  # Combine with base URL if relative
    
    # Get the image name from the URL
    img_name = img_url.split('/')[-1]
    
    # Download the image and save it
    try:
        img_data = requests.get(img_url).content
        with open(f'images/{img_name}', 'wb') as f:
            f.write(img_data)
        print(f"Downloaded {img_name}")
    except Exception as e:
        print(f"Failed to download {img_url}: {e}")
