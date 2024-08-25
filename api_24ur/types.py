import dataclasses
import datetime
import typing


@dataclasses.dataclass
class Image:
    caption: typing.Optional[str] = None
    url: typing.Optional[str] = None
    height: typing.Optional[int] = None
    width: typing.Optional[int] = None


@dataclasses.dataclass
class Video:
    title: typing.Optional[str] = None
    url: typing.Optional[str] = None


@dataclasses.dataclass
class Comment:
    posted_at: typing.Optional[datetime.datetime] = None
    content: typing.Optional[str] = None
    author: typing.Optional[str] = None
    author_avatar_url: typing.Optional[str] = None
    likes: typing.Optional[int] = None
    dislikes: typing.Optional[int] = None
    score: typing.Optional[int] = None
    replies: typing.Optional[typing.List['Comment']] = None


@dataclasses.dataclass
class Article:
    id: typing.Optional[str] = None
    title: typing.Optional[str] = None
    summary: typing.Optional[str] = None
    content: typing.Optional[str] = None
    place: typing.Optional[str] = None
    num_views: typing.Optional[int] = None
    images: typing.Optional[typing.List[Image]] = None
    videos: typing.Optional[typing.List[Video]] = None
    posted_at: typing.Optional[datetime.datetime] = None
    comments: typing.Optional[typing.List[Comment]] = None
