import dataclasses
import datetime
import typing


@dataclasses.dataclass
class Image:
    url: typing.Optional[str] = None
    title: typing.Optional[str] = None
    width: typing.Optional[int] = None
    height: typing.Optional[int] = None


@dataclasses.dataclass
class Comment:
    author: typing.Optional[str] = None
    text: typing.Optional[str] = None
    posted_at: typing.Optional[datetime.datetime] = None
    score: typing.Optional[int] = None
    likes: typing.Optional[int] = None
    dislikes: typing.Optional[int] = None


@dataclasses.dataclass
class Post:
    title: typing.Optional[str] = None
    author: typing.Optional[str] = None
    posted_at: typing.Optional[datetime.datetime] = None
    location: typing.Optional[str] = None
    description: typing.Optional[str] = None
    content: typing.Optional[str] = None
    comments: typing.Optional[typing.List[Comment]] = None
    images: typing.Optional[typing.List[Image]] = None
    video_url: typing.Optional[str] = None
