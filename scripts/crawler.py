import requests
import json
import aiofiles
import asyncio
import os


def get_access_token():
    headers = {
        'accept': '*/*',
        'content-type': 'application/x-www-form-urlencoded; charset=utf-8',
        'authorization': 'Basic aW1tb3dlbHRfbW9iaWxlX2FwcF9pb3NfMjo5UXVHa20xM1k0WEZPZHFzZW05eGh4RVVKejR2UWdEWA==',
        'accept-encoding': 'br;q=1.0, gzip;q=0.9, deflate;q=0.8',
        'user-agent': 'immowelt/7.8.1 (de.immowelt.immoweltapp; build:271; iOS 14.7.1) Alamofire/5.5.0',
        'accept-language': 'en-RS;q=1.0, sr-RS;q=0.9, sr-Latn-RS;q=0.8, de-RS;q=0.7'
    }

    response = requests.post(url="https://api.immowelt.com/auth/oauth/token",
                             data={"grant_type": "client_credentials"},
                             headers=headers)

    try:
        access_token = response.json()['access_token']
    except (KeyError, AttributeError, TypeError):
        return None
    else:
        return access_token


def get_listings():

    access_token = get_access_token()

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "accept-language": "en-RS;q=1.0, sr-RS;q=0.9, sr-Latn-RS;q=0.8, de-RS;q=0.7",
        "accept-encoding": "br;q=1.0, gzip;q=0.9, deflate;q=0.8",
        "content-length": "224",
        "user-agent": "immowelt/7.8.1 (de.immowelt.immoweltapp; build:271; iOS 14.7.1) Alamofire/5.5.0",
        "authorization": f"Bearer {access_token}"
    }

    params = {
        "construction": {},
        "general": {
            "category": [],
            "distributionType": "ZUR_MIETE",
            "equipment": [],
            "estateType": ["WOHNUNG", "LAND_FORSTWIRTSCHAFT", "WOHNGEMEINSCHAFT", "GARAGE_STELLPLATZ",
                           "GASTRONOMIE_HOTEL", "HALLEN_INDUSTRIEFLAECHE", "HAUS", "BUERO_PRAXISFLAECHE",
                           "GRUNDSTUECK", "SONSTIGES", "LADENFLAECHE", "WOHNEN_AUF_ZEIT",
                           "GEWERBE_GRUNDSTUECK", "RENDITEOBJEKT"]
        },
        "location": {
            "geo": {
                "locationId": [516424, 518004, 518044, 517940]
            }
        },
        "offset": "0",
        "pagesize": "5000",
        "pricing": {},
        "sort": "SortByCreateDate"
    }

    response = requests.post(url="https://api.immowelt.com/estatesearch/EstateSearch/v1/Search",
                             data=json.dumps(params),
                             headers=headers)

    try:
        listings = response.json()['items']
    except (KeyError, AttributeError, TypeError):
        return []
    else:
        return listings


async def save_to_file(listing, index):

    async with aiofiles.open(f'files/listing_{index}.json', 'w') as f:
        await f.write(json.dumps(listing))


async def main():

    listings = get_listings()
    tasks = []

    for index, listing in enumerate(listings):
        task = asyncio.create_task(save_to_file(listing, index))
        tasks.append(task)

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    path = os.getcwd() + '/files'
    os.makedirs(path, exist_ok=True)
    asyncio.run(main())
    print("DONE CRAWLER")
