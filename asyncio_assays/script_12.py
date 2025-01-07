# A Full Program: Asynchronous Requests
# 
# You’ve made it this far, and now it’s time for the fun and painless part. In this section, you’ll build a web-scraping URL collector, areq.py, using aiohttp, a blazingly fast async HTTP client/server framework. (We just need the client part.) Such a tool could be used to map connections between a cluster of sites, with the links forming a directed graph.
# 
# Note: You may be wondering why Python’s requests package isn’t compatible with async IO. requests is built on top of urllib3, which in turn uses Python’s http and socket modules.
# 
# By default, socket operations are blocking. This means that Python won’t like await requests.get(url) because .get() is not awaitable. In contrast, almost everything in aiohttp is an awaitable coroutine, such as session.request() and response.text(). It’s a great package otherwise, but you’re doing yourself a disservice by using requests in asynchronous code.
# 
# The high-level program structure will look like this:
# 
#     Read a sequence of URLs from a local file, urls.txt.
# 
#     Send GET requests for the URLs and decode the resulting content. If this fails, stop there for a URL.
# 
#     Search for the URLs within href tags in the HTML of the responses.
# 
#     Write the results to foundurls.txt.
# 
#     Do all of the above as asynchronously and concurrently as possible. (Use aiohttp for the requests, and aiofiles for the file-appends. These are two primary examples of IO that are well-suited for the async IO model.)
# 
# Here are the contents of urls.txt. It’s not huge, and contains mostly highly trafficked sites:
# 
# $ cat urls.txt
# https://regex101.com/
# https://docs.python.org/3/this-url-will-404.html
# https://www.nytimes.com/guides/
# https://www.mediamatters.org/
# https://1.1.1.1/
# https://www.politico.com/tipsheets/morning-money
# https://www.bloomberg.com/markets/economics
# https://www.ietf.org/rfc/rfc2616.txt
# 
# The second URL in the list should return a 404 response, which you’ll need to handle gracefully. If you’re running an expanded version of this program, you’ll probably need to deal with much hairier problems than this, such a server disconnections and endless redirects.
# 
# The requests themselves should be made using a single session, to take advantage of reusage of the session’s internal connection pool.
# 
# Let’s take a look at the full program. We’ll walk through things step-by-step after:

#!/usr/bin/env python3
# areq.py

"""Asynchronously get links embedded in multiple pages' HMTL."""

import asyncio
import logging
import re
import sys
from typing import IO
import urllib.error
import urllib.parse

import aiofiles
import aiohttp
from aiohttp import ClientSession

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)
logger = logging.getLogger("areq")
logging.getLogger("chardet.charsetprober").disabled = True

HREF_RE = re.compile(r'href="(.*?)"')

async def fetch_html(url: str, session: ClientSession, **kwargs) -> str:
    """GET request wrapper to fetch page HTML.

    kwargs are passed to `session.request()`.
    """

    resp = await session.request(method="GET", url=url, **kwargs)
    resp.raise_for_status()
    logger.info("Got response [%s] for URL: %s", resp.status, url)
    html = await resp.text()
    return html

async def parse(url: str, session: ClientSession, **kwargs) -> set:
    """Find HREFs in the HTML of `url`."""
    found = set()
    try:
        html = await fetch_html(url=url, session=session, **kwargs)
    except (
        aiohttp.ClientError,
        aiohttp.http_exceptions.HttpProcessingError,
    ) as e:
        logger.error(
            "aiohttp exception for %s [%s]: %s",
            url,
            getattr(e, "status", None),
            getattr(e, "message", None),
        )
        return found
    except Exception as e:
        logger.exception(
            "Non-aiohttp exception occured:  %s", getattr(e, "__dict__", {})
        )
        return found
    else:
        for link in HREF_RE.findall(html):
            try:
                abslink = urllib.parse.urljoin(url, link)
            except (urllib.error.URLError, ValueError):
                logger.exception("Error parsing URL: %s", link)
                pass
            else:
                found.add(abslink)
        logger.info("Found %d links for %s", len(found), url)
        return found

async def write_one(file: IO, url: str, **kwargs) -> None:
    """Write the found HREFs from `url` to `file`."""
    res = await parse(url=url, **kwargs)
    if not res:
        return None
    async with aiofiles.open(file, "a") as f:
        for p in res:
            await f.write(f"{url}\t{p}\n")
        logger.info("Wrote results for source URL: %s", url)

async def bulk_crawl_and_write(file: IO, urls: set, **kwargs) -> None:
    """Crawl & write concurrently to `file` for multiple `urls`."""
    async with ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(
                write_one(file=file, url=url, session=session, **kwargs)
            )
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    import pathlib
    import sys

    assert sys.version_info >= (3, 7), "Script requires Python 3.7+."
    here = pathlib.Path(__file__).parent

    with open(here.joinpath("urls.txt")) as infile:
        urls = set(map(str.strip, infile))

    outpath = here.joinpath("foundurls.txt")
    with open(outpath, "w") as outfile:
        outfile.write("source_url\tparsed_url\n")

    asyncio.run(bulk_crawl_and_write(file=outpath, urls=urls))
