import requests
from bs4 import BeautifulSoup

def get_description(url):

    response = requests.get(url)
    response.raise_for_status() 

    soup = BeautifulSoup(response.text, 'html.parser')

    descriptions = soup.select('.description')
    longest_description = max((desc.get_text(strip=True) for desc in descriptions), key=len, default=None)

    properties = {}
    for prop in soup.select('.property'):
        title = prop.select_one('.title')
        value = prop.select_one('.value')
        if title and value:
            properties[title.get_text(strip=True)] = value.get_text(strip=True)

    result = {
        'description': longest_description,
        'properties': properties
    }

    return result

if __name__ == "__main__":
    url = 'https://fix-price.com/catalog/dlya-doma/p-5079023-korobka-skladnaya-14-yacheek-32h32h9-sm'
    data = get_description(url)
    print(data)