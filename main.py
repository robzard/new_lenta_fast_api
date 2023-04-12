import uvicorn
from fastapi import FastAPI, Query
from parsing_lenta import ParsingLenta

app = FastAPI()
pl = ParsingLenta()


@app.get('/get_links')
@app.get('/get_links/{year}/{month}/{day}')
async def get_links(year: str = None, month: str = None, day: str = None) -> list:
    url = pl.get_url_for_start_page(year, month, day)
    page_html = await pl.get_page_html(url)
    links_list = await pl.get_all_links(page_html)
    return links_list


@app.post('/download_titles')
async def download_links_title(urls_list: list) -> dict[str, int | list]:
    result = await pl.download_pages(urls_list)
    titles = await pl.get_titles(result)
    return {'count': len(titles), 'titles': titles}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
