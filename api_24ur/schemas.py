import dataclasses
import datetime
import typing


@dataclasses.dataclass
class VideoHls:
    url: typing.Optional[str] = None
    info: typing.Optional[str] = None
    info_code: typing.Optional[int] = None

    @classmethod
    def from_dict(cls, data: typing.Dict) -> 'VideoHls':
        return cls(info_code=data.pop('infoCode'), **data)


@dataclasses.dataclass
class Owner:
    id: typing.Optional[int] = None
    nickname: typing.Optional[str] = None
    avatar_url: typing.Optional[str] = None

    @classmethod
    def from_dict(cls, data: typing.Dict) -> 'Owner':
        cls(
            avatar_url=data.pop('avatarUrl'),
            **data,
        )


@dataclasses.dataclass
class Likes:
    sum: typing.Optional[int] = None
    negative: typing.Optional[int] = None
    positive: typing.Optional[int] = None

    @classmethod
    def from_dict(cls, data: typing.Dict) -> 'Likes':
        return cls(**data)


@dataclasses.dataclass
class Comment:
    id: typing.Optional[str] = None
    created_on: typing.Optional[int] = None
    body: typing.Optional[str] = None
    owner: typing.Optional[Owner] = None
    likes: typing.Optional[Likes] = None
    replies: typing.Optional[typing.List['Comment']] = None

    @classmethod
    def from_dict(cls, data: typing.Dict) -> 'Comment':
        return cls(
            created_on=data.pop('createdOn'),
            replies=[Comment.from_dict(reply) for reply in data.pop('replies', [])],
            owner=Owner.from_dict(data.pop('owner', {})),
            likes=Likes.from_dict(data.pop('likes', {})),
            **data,
        )


@dataclasses.dataclass
class BodyItems:
    type: typing.Optional[str] = None
    body: typing.Optional[str] = None
    id: typing.Optional[int] = None
    index: typing.Optional[int] = None
    data: typing.Optional[str] = None

    @classmethod
    def from_dict(cls, data: typing.Dict) -> 'BodyItems':
        return cls(**data)


@dataclasses.dataclass
class Site:
    id: typing.Optional[int] = None
    name: typing.Optional[str] = None

    @classmethod
    def from_dict(cls, data: typing.Dict) -> 'Site':
        return cls(**data)


@dataclasses.dataclass
class Section:
    id: typing.Optional[int] = None
    title: typing.Optional[str] = None
    site_id: typing.Optional[int] = None
    meta_keywords: typing.Optional[str] = None
    meta_description: typing.Optional[str] = None
    window_title: typing.Optional[str] = None
    gemius_code: typing.Optional[datetime.datetime] = None
    path: typing.Optional[str] = None
    root_section_id: typing.Optional[int] = None
    grid_section_id: typing.Optional[int] = None

    @classmethod
    def from_dict(cls, data: typing.Dict) -> 'Section':
        return cls(
            id=data.get('id'),
            title=data.get('title'),
            site_id=data.get('siteId'),
            meta_keywords=data.get('metaKeywords'),
            meta_description=data.get('metaDescription'),
            window_title=data.get('windowTitle'),
            gemius_code=data.get('gemiusCode'),
            path=data.get('path'),
            root_section_id=data.get('rootSectionId'),
            grid_section_id=data.get('gridSectionId'),
        )


@dataclasses.dataclass
class FrontImage:
    id: typing.Optional[int] = None
    src: typing.Optional[str] = None
    caption: typing.Optional[str] = None
    source: typing.Optional[str] = None
    type: typing.Optional[str] = None
    order: typing.Optional[int] = None

    @classmethod
    def from_dict(cls, data: typing.Dict) -> 'FrontImage':
        return cls(**data)


@dataclasses.dataclass
class Images:
    caption: typing.Optional[str] = None
    show_caption: typing.Optional[bool] = None
    source: typing.Optional[str] = None
    src: typing.Optional[str] = None
    type: typing.Optional[str] = None
    link: typing.Optional[str] = None
    id: typing.Optional[int] = None
    height: typing.Optional[int] = None
    width: typing.Optional[int] = None

    @classmethod
    def from_dict(cls, data: typing.Dict) -> 'Images':
        return cls(
            show_caption=data.pop('showCaption'),
            **data,
        )


@dataclasses.dataclass
class Image:
    src: typing.Optional[str] = None

    @classmethod
    def from_dict(cls, data: typing.Dict) -> 'Image':
        return cls(**data)


@dataclasses.dataclass
class Videos:
    id: typing.Optional[int] = None
    object_type: typing.Optional[str] = None
    title: typing.Optional[str] = None
    subtype: typing.Optional[str] = None
    date: typing.Optional[int] = None
    order: typing.Optional[int] = None
    length: typing.Optional[int] = None
    style: typing.Optional[str] = None
    preroll: typing.Optional[bool] = None
    postroll: typing.Optional[bool] = None
    vtt: typing.Optional[str] = None
    image: typing.Optional[Image] = None

    @classmethod
    def from_dict(cls, data: typing.Dict) -> 'Videos':
        return cls(
            image=Image.from_dict(data.pop('image', {})),
            object_type=data.pop('objectType'),
            **data,
        )


@dataclasses.dataclass
class Galleries:
    id: typing.Optional[int] = None
    title: typing.Optional[str] = None
    summary: typing.Optional[str] = None
    type: typing.Optional[str] = None
    subtype: typing.Optional[str] = None
    images: typing.Optional[typing.List[Images]] = None

    @classmethod
    def from_dict(cls, data: typing.Dict) -> 'Galleries':
        return cls(images=[Images.from_dict(image) for image in data.pop('images', [])], **data)


@dataclasses.dataclass
class Quotes:
    order: typing.Optional[int] = None
    author: typing.Optional[str] = None
    body: typing.Optional[str] = None
    type: typing.Optional[int] = None
    url: typing.Optional[str] = None

    @classmethod
    def from_dict(cls, data: typing.Dict) -> 'Quotes':
        return cls(**data)


@dataclasses.dataclass
class Article:
    id: typing.Optional[int] = None
    title: typing.Optional[str] = None
    subtitle: typing.Optional[str] = None
    summary: typing.Optional[str] = None
    keywords: typing.Optional[str] = None
    categories: typing.Optional[str] = None
    place: typing.Optional[str] = None
    date: typing.Optional[int] = None
    url: typing.Optional[str] = None
    nb_views: typing.Optional[int] = None
    last_changed: typing.Optional[int] = None
    style: typing.Optional[str] = None
    desktop_url: typing.Optional[str] = None
    has_banners: typing.Optional[int] = None
    has_comments: typing.Optional[int] = None
    allow_new_comments: typing.Optional[int] = None
    has_votes: typing.Optional[str] = None
    is_slim: typing.Optional[bool] = None
    body_items: typing.Optional[typing.List[BodyItems]] = None
    has_videos: typing.Optional[int] = None
    has_galleries: typing.Optional[int] = None
    has_streams: typing.Optional[int] = None
    is_developing: typing.Optional[bool] = None
    has_audios: typing.Optional[int] = None
    has_documents: typing.Optional[int] = None
    nb_comments: typing.Optional[int] = None
    has_active_feed: typing.Optional[bool] = None
    substyle: typing.Optional[str] = None
    reading_time: typing.Optional[int] = None
    source: typing.Optional[str] = None
    feeds: typing.Optional[typing.List] = None
    front_image: typing.Optional[FrontImage] = None
    additional_front_images: typing.List[FrontImage] = None
    images: typing.Optional[typing.List[Images]] = None
    videos: typing.Optional[typing.List[Videos]] = None
    audios: typing.Optional[typing.List] = None
    streams: typing.Optional[typing.List] = None
    documents: typing.Optional[typing.List] = None
    galleries: typing.Optional[typing.List[Galleries]] = None
    section: typing.Optional[Section] = None
    quotes: typing.Optional[typing.List[Quotes]] = None
    embeds: typing.Optional[typing.List] = None
    polls: typing.Optional[typing.List] = None
    site: typing.Optional[Site] = None
    related_articles: typing.Optional[typing.List] = None
    related_recipes: typing.Optional[typing.List] = None

    @classmethod
    def from_dict(cls, data: typing.Dict) -> 'Article':
        return cls(
            id=data.get('id'),
            title=data.get('title'),
            subtitle=data.get('subtitle'),
            summary=data.get('summary'),
            keywords=data.get('keywords'),
            categories=data.get('categories'),
            place=data.get('place'),
            date=data.get('date'),
            url=data.get('url'),
            nb_views=data.get('nbViews'),
            last_changed=data.get('lastChanged'),
            style=data.get('style'),
            desktop_url=data.get('desktopUrl'),
            has_banners=data.get('hasBanners'),
            has_comments=data.get('hasComments'),
            allow_new_comments=data.get('allowNewComments'),
            has_votes=data.get('hasVotes'),
            is_slim=data.get('isSlim'),
            body_items=[BodyItems.from_dict(body_item) for body_item in data.get('bodyItems', [])],
            has_videos=data.get('hasVideos'),
            has_galleries=data.get('hasGalleries'),
            has_streams=data.get('hasStreams'),
            is_developing=data.get('isDeveloping'),
            has_audios=data.get('hasAudios'),
            has_documents=data.get('hasDocuments'),
            nb_comments=data.get('nbComments'),
            has_active_feed=data.get('hasActiveFeed'),
            substyle=data.get('substyle'),
            reading_time=data.get('readingTime'),
            source=data.get('source'),
            feeds=data.get('feeds'),
            front_image=FrontImage.from_dict(data.get('frontImage', {})),
            additional_front_images=[FrontImage(**image) for image in data.get('additionalFrontImages', [])],
            images=[Images.from_dict(image) for image in data.get('images', [])],
            videos=[Videos.from_dict(video) for video in data.get('videos', [])],
            audios=data.get('audios'),
            streams=data.get('streams'),
            documents=data.get('documents'),
            galleries=[Galleries.from_dict(gallery) for gallery in data.get('galleries', [])],
            section=Section.from_dict(data.get('section', {})),
            quotes=[Quotes.from_dict(quote) for quote in data.get('quotes', [])],
            embeds=data.get('embeds'),
            polls=data.get('polls'),
            site=Site.from_dict(data.get('site', {})),
            related_articles=data.get('relatedArticles'),
            related_recipes=data.get('relatedRecipes'),
        )


@dataclasses.dataclass
class Data:
    article: typing.Optional[Article] = None

    @classmethod
    def from_dict(cls, data: typing.Dict) -> 'Data':
        return cls(article=Article.from_dict(data.get('article', {})))


@dataclasses.dataclass
class Root:
    data: typing.Optional[Data] = None

    @classmethod
    def from_dict(cls, data: typing.Dict) -> 'Root':
        return cls(data=Data.from_dict(data.get('data', {})))
