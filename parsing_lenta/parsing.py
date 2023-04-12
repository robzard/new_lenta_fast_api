import re
import aiohttp
from aiohttp import ClientSession
from bs4 import BeautifulSoup
import asyncio
import numpy as np

user_agent = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 OPR/72.0.3815.465 (Edition Yx GX)',
}
conn = aiohttp.TCPConnector(limit_per_host=3)


class ParsingLenta:
    def __init__(self):
        self.URL_SITE = 'https://lenta.ru'

    @staticmethod
    async def request(url: str) -> str:
        print(f'get page html - {url}')
        async with aiohttp.ClientSession(trust_env=True, headers=user_agent) as session:
            async with session.get(url) as response:
                return await response.text()

    async def get_page_html(self, url) -> str:
        return await self.request(url)

    async def get_all_links(self, html: str) -> list:
        soup = await self.get_page_soup(html)
        links = soup.find_all('a', class_=re.compile('card-mini|card-full-news'))
        links_list = [self.URL_SITE + link['href'] for link in links]
        print(len(links_list))
        return links_list

    async def download_pages(self, urls: list) -> list:
        result = []
        tasks = []
        for url in urls[:10]:
            task = asyncio.create_task(self.request(url))
            tasks.append(task)
            if len(tasks) == 3:
                task_result = await asyncio.gather(*tasks)
                result.append(task_result)
                tasks = []
                await asyncio.sleep(1)
        return list(np.concatenate(result))

    async def get_titles(self, html_list: list) -> list:
        titles_list = []
        for html in html_list:
            soup = await self.get_page_soup(html)
            title = soup.find('h1', class_=re.compile('title')).text
            titles_list.append(title)
        return titles_list

    def get_url_for_start_page(self, year: str = None, month: str = None, day: str = None) -> str:
        if year and month and day:
            return f'{self.URL_SITE}/news/{year}/{month}/{day}'
        return self.URL_SITE

    @staticmethod
    async def get_page_soup(html: str) -> BeautifulSoup:
        soup = BeautifulSoup(html, 'html.parser')
        return soup
