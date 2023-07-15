import argparse
import urllib.request
import html.parser
from datetime import datetime
from html import parser

class mParser(html.parser.HTMLParser):
    urls = []
    now = datetime.now()
    tms = datetime.timestamp(now)

    def handle_starttag(self, tag, attrs):
        f = open("links.txt", "a")
        if(tag == "a"):
            for a in attrs:
                if(a[0] == 'href'):
                    if(a[0] == 'href' and str(a[1]).startswith('http')):
                        print(a[1])
                        self.urls.append(a[1])
                        f.write("{\n\"url\":\"" + a[1]+"\"\n},\n")
                        f.close()

def spidering(target, output):
    with urllib.request.urlopen(args.target) as response:
        handle = response.read().decode('latin-1')
        parser = mParser()
        parser.feed(handle)
        links = mParser.urls
        f = open(f"{args.output}", "a")
        f.write("]")
        f.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target")
    parser.add_argument("-o", "--output", default="links.txt")
    args = parser.parse_args()
    try:
        spidering(args.target, args.output)
    except Exception as err: print(err)

  