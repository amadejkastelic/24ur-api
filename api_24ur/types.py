import dataclasses
import typing


@dataclasses.dataclass
class Image:
    caption: typing.Optional[str] = None
    src: typing.Optional[str] = None
    height: typing.Optional[int] = None
    width: typing.Optional[int] = None


@dataclasses.dataclass
class Video:
    title: typing.Optional[str] = None


@dataclasses.dataclass
class Article:
    title: typing.Optional[str] = None
    summary: typing.Optional[str] = None
    place: typing.Optional[str] = None
    num_views: typing.Optional[int] = None
    num_comments: typing.Optional[int] = None
    images: typing.Optional[typing.List[Image]] = None
    videos: typing.Optional[typing.List[Video]] = None
