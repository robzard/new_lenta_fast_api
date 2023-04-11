import re
import aiohttp
from aiohttp import ClientSession
from bs4 import BeautifulSoup
import asyncio


class ParsingLenta():
    def __init__(self, year: str = None, month: str = None, day: str = None):
        self.URL_SITE = 'https://lenta.ru'
        self.year = year
        self.month = month
        self.day = day
        self.url = self.get_url()
        print(f"parsing url - {self.url}")

    def get_url(self) -> str:
        if self.year and self.month and self.day:
            return f'{self.URL_SITE}/news/{self.year}/{self.month}/{self.day}'
        return self.URL_SITE

    async def get_page_html(self) -> str:
        async with aiohttp.ClientSession() as session:
            return await self.request(session, self.url)

    async def get_all_links(self, html: str) -> list:
        links_list = []
        soup = await self.get_page_soup(html)
        links = soup.find_all('a', class_=re.compile('card-mini|card-full-news'))
        for link in links:
            href = self.URL_SITE + link.get('href')
            links_list.append(href)
        print(len(links_list))
        return links_list

    @staticmethod
    async def get_page_soup(html: str) -> BeautifulSoup:
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    @staticmethod
    async def request(session: ClientSession, url: str):
        async with session.get(url) as response:
            return await response.text()
