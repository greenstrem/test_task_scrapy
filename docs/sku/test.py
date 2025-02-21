import requests

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-type': 'application/json',
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
    'x-key': 'bc84fec1c1b76b827965943d6dc04f1b',
    'x-language': 'ru',
}

params = {
    'page': '1',
    'limit': '24',
    'sort': 'sold',
}

json_data = {
    'category': 'sad-i-ogorod',
    'brand': [],
    'price': [],
    'isDividedPrice': False,
    'isNew': False,
    'isHit': False,
    'isSpecialPrice': False,
}

response = requests.post(
    'https://api.fix-price.com/buyer/v1/product/in/sad-i-ogorod',
    params=params,
    headers=headers,
    json=json_data,
)
print(response.text)

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"category":"sad-i-ogorod","brand":[],"price":[],"isDividedPrice":false,"isNew":false,"isHit":false,"isSpecialPrice":false}'
#response = requests.post('https://api.fix-price.com/buyer/v1/product/in/sad-i-ogorod', params=params, headers=headers, data=data)