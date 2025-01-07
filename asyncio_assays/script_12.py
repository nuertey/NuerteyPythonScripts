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

# This script is longer than our initial toy programs, so let’s break it down.
# 
# The constant HREF_RE is a regular expression to extract what we’re ultimately searching for, href tags within HTML:
# 
# >>> HREF_RE.search('Go to <a href="https://realpython.com/">Real Python</a>')
# <re.Match object; span=(15, 45), match='href="https://realpython.com/"'>
# 
# The coroutine fetch_html() is a wrapper around a GET request to make the request and decode the resulting page HTML. It makes the request, awaits the response, and raises right away in the case of a non-200 status:
# 
# resp = await session.request(method="GET", url=url, **kwargs)
# resp.raise_for_status()
# 
# If the status is okay, fetch_html() returns the page HTML (a str). Notably, there is no exception handling done in this function. The logic is to propagate that exception to the caller and let it be handled there:
# 
# html = await resp.text()
# 
# We await session.request() and resp.text() because they’re awaitable coroutines. The request/response cycle would otherwise be the long-tailed, time-hogging portion of the application, but with async IO, fetch_html() lets the event loop work on other readily available jobs such as parsing and writing URLs that have already been fetched.
# 
# Next in the chain of coroutines comes parse(), which waits on fetch_html() for a given URL, and then extracts all of the href tags from that page’s HTML, making sure that each is valid and formatting it as an absolute path.
# 
# Admittedly, the second portion of parse() is blocking, but it consists of a quick regex match and ensuring that the links discovered are made into absolute paths.
# 
# In this specific case, this synchronous code should be quick and inconspicuous. But just remember that any line within a given coroutine will block other coroutines unless that line uses yield, await, or return. If the parsing was a more intensive process, you might want to consider running this portion in its own process with loop.run_in_executor().
# 
# Next, the coroutine write() takes a file object and a single URL, and waits on parse() to return a set of the parsed URLs, writing each to the file asynchronously along with its source URL through use of aiofiles, a package for async file IO.
# 
# Lastly, bulk_crawl_and_write() serves as the main entry point into the script’s chain of coroutines. It uses a single session, and a task is created for each URL that is ultimately read from urls.txt.
# 
# Here are a few additional points that deserve mention:
# 
#     The default ClientSession has an adapter with a maximum of 100 open connections. To change that, pass an instance of asyncio.connector.TCPConnector to ClientSession. You can also specify limits on a per-host basis.
# 
#     You can specify max timeouts for both the session as a whole and for individual requests.
# 
#     This script also uses async with, which works with an asynchronous context manager. I haven’t devoted a whole section to this concept because the transition from synchronous to asynchronous context managers is fairly straightforward. The latter has to define .__aenter__() and .__aexit__() rather than .__exit__() and .__enter__(). As you might expect, async with can only be used inside a coroutine function declared with async def.
# 
# If you’d like to explore a bit more, the companion files for this tutorial up at GitHub have comments and docstrings attached as well.
