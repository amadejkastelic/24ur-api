import datetime

import bs4

from api_24ur import types

DATE_TIME_FORMAT = '%d. %m. %Y %H.%M'


class Scraper:
    def __init__(self, html: str) -> None:
        self.soup = bs4.BeautifulSoup(html, 'html.parser')

    def scrape(self) -> types.Post:
        article = self.soup.find_all('article')[0]

        title = article.h1.text
        location, posted_at_str = article.p.text.split(', ')
        posted_at_str = posted_at_str.split('|')[0].strip()
        description = article.find('div', class_='md:px-article-summary').text

        content = ''
        for p in article.find_all('p'):
            if p.strong is not None and p.text.startswith(p.strong.text):
                content += f'{p.strong.text}\n{p.text[len(p.strong.text):]}\n'
            else:
                content += f'{p.text}\n'
        content_start_sep = ' min\n'
        content_end_sep = '\nOpozorilo:\n'
        content = content[content.find(content_start_sep)+len(content_start_sep):content.find(content_end_sep)]

        comments = []
        for comment in article.find_all('div', _class='comment'):
            comments.append(
                types.Comment(
                    author=comment.find('a', _class='comment__author').text,
                    posted_at=datetime.datetime.strptime(comment.find('div', _class='comment__time').text, DATE_TIME_FORMAT),
                    score=int(comment.find('div', _class='comment--positive')),
                    text=comment.find('div', _class='comment__content--body').text,
                    likes=int(comment.find('span', _class='comment-likes-positive')),
                    dislikes=int(comment.find('span', _class='comment-likes-negative')),
                )
            )

        gallery = article.find('div', _class='gallery')
        image_section = gallery.find('section')
        gallery_id = image_section.id
        images = []
        for image in image_section.find('ul', _id=f'{gallery_id}-list').find_all('li'):
            img = image.find('img')
            images.append(
                types.Image(
                    url=img.src,
                    width=int(img.width) if img.width else None,
                    height=int(img.height) if img.height else None,
                    title=image['data-title'],
                )
            )

        return types.Post(
            title=title,
            location=location,
            posted_at=datetime.datetime.strptime(posted_at_str, DATE_TIME_FORMAT),
            description=description,
            content=content,
            comments=comments,
            images=images,
        )
