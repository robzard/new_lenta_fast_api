import uvicorn
from fastapi import FastAPI, Query
from parsing_lenta import ParsingLenta

app = FastAPI()


@app.get('/get_links')
@app.get('/get_links/{year}/{month}/{day}')
async def get_links(year: str = None, month: str = None, day: str = None):
    pl = ParsingLenta(year, month, day)
    page_html = await pl.get_page_html()
    links_list = await pl.get_all_links(page_html)
    return links_list


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
