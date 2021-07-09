__author__ = "Shane Drabing"
__license__ = "MIT"
__version__ = "0.0.0"
__email__ = "shane.drabing@gmail.com"


# IMPORTS


import concurrent.futures
import functools
import re

import bs4
import requests


# CONSTANTS


PATTERN_INFOBOX = re.compile(r"^infobox")
STRAIN_HEAD = bs4.SoupStrainer("head")
STRAIN_INFOBOX = bs4.SoupStrainer("table", {"class": PATTERN_INFOBOX})
URL_WIKI_SEARCH = "https://en.wikipedia.org/w/index.php?search="


# ENUMS


class Symbols:
    DAGGER = "†"
    CROSS = "×"
    LINK = "⛓"
    EYE = "👁"
    FLAT = "─"
    VERT = "│"
    RTEE = "├"
    TURN = "└"


# CLASSES


class Node:
    def __init__(self, data):
        self.key = data["url"]
        if "name" in data:
            self.name = data["name"]
        else:
            self.name = data["url"].split("/")[-1]
        self.thumb = data["thumb"] if "thumb" in data else None

        self.parents = dict()
        self.children = dict()

    def __str__(self):
        return self.name

    def sort_metric(self, ischild):
        return (-self.count(ischild), self.key)

    def count(self, ischild):
        n = len(self.children)
        if ischild:
            return n + sum(x.count(ischild) for x in self.children.values())
        return n + sum(x.count(ischild) for x in self.parents.values())

    def pretty(self, ischild=True, first="", second="", length=2):
        string = f"{first}{self}\n"
        ordinal = (self.children if ischild else self.parents).values()
        ordinal = sorted(ordinal, key=lambda x: -x.count(ischild))

        for x in ordinal[:-1]:
            string += x.pretty(
                ischild,
                second + f"{Symbols.RTEE}{Symbols.FLAT * length} ",
                second + f"{Symbols.VERT}{' ' * length} ",
                length
            )
        if ordinal:
            string += ordinal[-1].pretty(
                ischild,
                second + f"{Symbols.TURN}{Symbols.FLAT * length} ",
                second + f" {' ' * length} ",
                length
            )

        return string


# FUNCTIONS


def get_resp(url):
    return requests.get(url)


def is_wiki_href(url):
    return url.startswith("/wiki/") and not ":" in url


def make_wiki_url(href):
    return "https://en.wikipedia.org" + href


def parse_infobox(resp, pre, post, extra):
    dct = {
        "url": resp.url,
        "canonical": str(),
        "name": str(),
        "thumb": str(),
        "relation": {"pre": set(), "post": set(), "extra": set()}
    }
    
    if resp.status_code != 200:
        return dct

    html = resp.content
    head = bs4.BeautifulSoup(html, "lxml", parse_only=STRAIN_HEAD)
    box = bs4.BeautifulSoup(html, "lxml", parse_only=STRAIN_INFOBOX)

    link = head.select_one("link[rel='canonical']")
    if link:
        dct["canonical"] = link["href"]
    if not box:
        return dct

    th = box.select_one("th")
    if th:
        dct["name"] = th.text
    img = box.select_one("img")
    if img:
        dct["thumb"] = img["src"]

    headers = box.select("th.infobox-label")
    for th in headers:
        if pre and pre.match(th.text):
            rel = "pre"
        elif post and post.match(th.text):
            rel = "post"
        elif extra and extra.match(th.text):
            rel = "extra"
        else:
            continue

        row = th.parent
        links = row.select("td a")
        for link in links:
            href = link["href"]
            if not is_wiki_href(href):
                continue

            url = make_wiki_url(href)
            dct["relation"][rel].add(url)

    return dct


def walk_relations(term, pre, post, extra, steps):
    url = get_resp(URL_WIKI_SEARCH + term).url
    urls = {url}

    seen = set()
    data = tuple()

    new = urls - seen
    if not steps:
        steps = float("inf")

    while new and (steps > 0):
        steps -= 1
        seen |= urls
        
        print(f"Checking {len(new)} links...".ljust(30), end="\r")
        with concurrent.futures.ThreadPoolExecutor() as exe:
            resps = tuple(exe.map(get_resp, new))

        n = len(resps)
        tup = tuple(map(
            parse_infobox, resps,
            n * (pre,), n * (post,), n * (extra,)
        ))

        data += tup
        for dct in tup:
            urls |= functools.reduce(set.union, dct["relation"].values())
        new = urls - seen

    print(f"Done checking {len(urls)} links.".ljust(30), end="\n\n")
    return (url, data)


def main(args):
    for attr in ("pre", "post", "extra"):
        x = getattr(args, attr)
        if x:
            setattr(args, attr, re.compile(x))

    root, data = walk_relations(
        args.term, args.pre, args.post, args.extra, args.steps
    )

    canon = dict()
    for dct in data:
        canon[dct["url"]] = dct["canonical"]
        canon[dct["canonical"]] = dct["canonical"]
    root = canon[root]

    keys = set()
    for dct in data:
        dct["url"] = canon[dct["url"]]
        dct["relation"] = {
            k: {canon[x] if x in canon else x for x in v}
            for k, v in dct["relation"].items()
        }
        keys.add(dct["url"])
        keys |= functools.reduce(set.union, dct["relation"].values())

    lookup = {
        k: Node({"url": k})
        for k in keys
    }
    for dct in data:
        lookup[dct["url"]] = Node(dct)

    for dct in data:
        me = dct["url"]

        for parent in dct["relation"]["pre"]:
            if lookup[me] is lookup[parent]:
                continue
            lookup[parent].children[me] = lookup[me]
            lookup[me].parents[parent] = lookup[parent]

        for child in dct["relation"]["post"]:
            if lookup[me] is lookup[child]:
                continue
            lookup[me].children[child] = lookup[child]
            lookup[child].parents[me] = lookup[me]

    print("ANCESTORS of ", end=str())
    print(lookup[root].pretty(ischild=False))
    
    print("DESCENDANTS of ", end=str())
    print(lookup[root].pretty())


# SCRIPT


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("term", type=str)
    parser.add_argument("pre", nargs="?", type=str)
    parser.add_argument("post", nargs="?", type=str)
    parser.add_argument("-e", "--extra", nargs="?", type=str)
    parser.add_argument("-n", "--steps", nargs="?", type=int)
    args = parser.parse_args()

    main(args)
