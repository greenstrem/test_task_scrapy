import requests

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'origin': 'https://fix-price.com',
    'priority': 'u=1, i',
    'referer': 'https://fix-price.com/',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'x-city': '3',
    'x-delivery-type': 'store',
    'x-key': 'bc84fec1c1b76b827965943d6dc04f1b',
    'x-language': 'ru',
    'x-pfm': '5528',
}

response = requests.get('https://api.fix-price.com/buyer/v1/category/menu', headers=headers)
print(response.text)


