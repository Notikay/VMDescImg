from dataclasses import dataclass


@dataclass
class Response:
    msg: str
    code: int


@dataclass
class GetDescriptResponse(Response):
    desc: str


@dataclass
class UploadImgResponse(Response):
    uuid: str


@dataclass
class ErrorResponse(Response):
    error: str
