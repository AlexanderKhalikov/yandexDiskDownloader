import asyncio
import json
import logging
import urllib
import requests
from urllib.parse import urlencode
import yaml
import aiohttp
from rich.progress import Progress


with open('config/configTest.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

targetUrl = config['targetUrl']
destination_folder = config['destination_folder']
number_of_files = config['number_of_files']

folder_url = 'https://yadi.sk/d' + targetUrl[targetUrl.rfind('/'):]
publicUrl = 'https://cloud-api.yandex.net/v1/disk/public/resources'


class YandexDiskDownloader:

    @staticmethod
    async def download_file(session, url, file_name):
        async with session.get(url, ssl=False) as response:
            with open(destination_folder + '/' + file_name, 'wb') as fd:
                async for chunk in response.content.iter_chunked(10):
                    fd.write(chunk)

    @staticmethod
    def download(download_urls: list, file_names: list):
        for url, file_name in zip(download_urls, file_names):
            response = requests.get(url)

            if response.status_code == 200:
                with open(destination_folder + '/' + file_name, 'wb') as file:
                    file.write(response.content)
            else:
                logging.info(f'Download failed with URL - {url}, file name - {file_name}')
                print(f'Download failed with URL - {url}, file name - {file_name}')

    @staticmethod
    def get_urls_and_names():
        response = requests.get(
            url=publicUrl + '?public_key='
            + urllib.parse.quote(folder_url)
            + '&limit=' + str(number_of_files)
        )

        if response.status_code == 200:
            public_folder = json.loads(response.text)['_embedded']['items']
            file_names = list(x['name'] for x in public_folder)

            prefix = publicUrl \
                + '/download?public_key=' \
                + urllib.parse.quote(folder_url) + '&path=/'

            urls = list(prefix + urllib.parse.quote(file_name) for file_name in file_names)

            # This probably can be done asynchronously
            download_urls = list(json.loads(requests.get(url).text)['href'] for url in urls)

            return download_urls, file_names
        else:
            print(response.status_code)
            return


async def main(urls, file_names):
    # Add Progress Bar to be fancy
    async with aiohttp.ClientSession() as session:
        tasks = [
            YandexDiskDownloader.download_file(session, url, file_name)
            for url, file_name in zip(urls, file_names)
        ]

        with Progress() as bar:
            bar_task = bar.add_task('Downloading files...', total=len(tasks))
            for task in asyncio.as_completed(tasks):
                await task
                bar.update(bar_task, advance=1)

    # async with aiohttp.ClientSession() as session:
    #     tasks = [
    #         asyncio.ensure_future(
    #             YandexDiskDownloader.download_file(session, url, file_name)
    #         )
    #         for url, file_name in zip(urls, file_names)
    #     ]
    #
    #     await asyncio.gather(*tasks)


if __name__ == '__main__':

    logging.info('Gathering filenames')
    print('Gathering filenames')
    URLs, names = YandexDiskDownloader.get_urls_and_names()

    logging.info('Download has started')
    print('Download has started')

    asyncio.run(main(URLs, names))

    logging.info('Download has finished')
    print('Download has finished')
