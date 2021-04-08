# TODO: Get author
# TODO: Download images and search-replace new paths

from urllib.request import urlopen
from bs4 import BeautifulSoup, Doctype

ISSUE = 'current' # make this an argument
HOME_URL = 'http://clarkesworldmagazine.com'

if ISSUE != 'current':
    HOME_URL += f'/issue_{ISSUE}'

# read main page and get issue info and story urls
with urlopen(HOME_URL) as url:
    page = BeautifulSoup(url, features="html.parser")
content = page.select('.home_body_2')[0]
p_entries = content.find_all('p')

# get issue title
p_title = p_entries[0]
if 'issue' not in p_title.attrs['class']:
    exit("Error: HTML has unexpected format: first paragraph doesn't have issue info")
issue_title = p_title.text

if p_entries[1].text != 'FICTION':
    exit("Error: HTML has unexpected format: 'FICTION' header not in expected location")

# iterate to get story titles and urls
stories = []
for p in p_entries[2:]:
    text = p.text
    attrs = p.attrs

    # only get fiction
    if 'section2' in attrs['class']:
        break

    # grab issue title
    if 'story' in attrs['class']:
        story = {'title': text, 'url': p.a['href']}
        stories.append(story)

# initiate doc
doc = BeautifulSoup()
doc.append(Doctype('html'))
html = doc.new_tag('html', lang='en-US')
doc.append(html)
head = doc.new_tag('head')
html.append(head)
meta = doc.new_tag('meta', charset='utf-8')
head.append(meta)
title = doc.new_tag('title')
title.string = issue_title
head.append(title)
body = doc.new_tag('body')
html.append(body)

for story in stories:
    header = doc.new_tag('h1')
    header.string = story['title']
    body.append(header)

    with urlopen(HOME_URL+story['url']) as url:
        page = BeautifulSoup(url, features="html.parser")
    content = page.select('.story-text')[0]
    body.append(content)

# print(str(doc))

doc = BeautifulSoup(str(doc).replace('../images/storycom.jpg',
                                     '/Users/msteinpreis/Desktop/clarkesworld_ebook/data/issues/imgs/storycom.jpeg'),
                    features='html.parser')

print(doc.prettify())
