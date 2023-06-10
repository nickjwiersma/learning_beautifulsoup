import requests
from bs4 import BeautifulSoup
import csv

# Requesting the website
res = requests.get('https://news.ycombinator.com/')
res2 = requests.get('https://news.ycombinator.com/?p=2')

soup = BeautifulSoup(res.text, 'html.parser')
soup2 = BeautifulSoup(res2.text, 'html.parser')
links = soup.select('.titleline')
links2 = soup2.select('.titleline')
subtext = soup.select('.subtext')
subtext2 = soup2.select('.subtext')

combined_links = links + links2
combined_subtext = subtext + subtext2

def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k: k['vote'], reverse=True)

def create_custom_hn(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        title = links[idx].getText()
        href = links[idx].find('a')['href'] if links[idx].find('a') else None
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99:
                hn.append({'title': title, 'link': href, 'vote': points})
    return sort_stories_by_votes(hn)

custom_hn = create_custom_hn(combined_links, combined_subtext)

# Define the CSV file path
csv_file = 'hacker_news.csv'

# Write the data to the CSV file
with open(csv_file, 'w', newline='') as file:
    fieldnames = ['Title', 'Link', 'Vote']
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    for item in custom_hn:
        writer.writerow({'Title': item['title'], 'Link': item['link'], 'Vote': item['vote']})

print(f'Scraped data has been saved to {csv_file}.')
