import os
import typing
from pydantic_settings import BaseSettings

BASE_DIR = os.path.dirname(__file__)


class Config(BaseSettings):
    driver_remote_url: str
    userName: str
    accessKey: str
    timeout: float = 10.0
    android_app_url: str
    ios_app_url: str

    android_platformVersion: typing.Literal['11.0', '12.0', '13.0'] = '11.0'
    android_deviceName: typing.Literal[
        'Samsung Galaxy S22 Ultra',
        'Google Pixel 7 Pro',
        'OnePlus 9',
    ] = 'OnePlus 9'

    ios_platformVersion: typing.Literal['16', '15', '14'] = '15'
    ios_deviceName: typing.Literal[
        'iPhone 14 Pro Max', 'iPhone XS', 'iPhone 11'
    ] = 'iPhone 11'


config = Config(_env_file=os.path.join(BASE_DIR, '.env'))

