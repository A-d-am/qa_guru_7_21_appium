import os
from typing import Literal
from pydantic_settings import BaseSettings

BASE_DIR = os.path.dirname(__file__)


class Config(BaseSettings):
    driver_remote_url: str
    bstack_userName: str
    bstack_accessKey: str
    timeout: float = 10.0
    android_app_url: str
    ios_app_url: str

    android_platformVersion: Literal['11.0', '12.0', '13.0'] = '11.0'
    android_deviceName: Literal[
        'Samsung Galaxy S22 Ultra',
        'Google Pixel 7 Pro',
        'OnePlus 9',
    ] = 'Samsung Galaxy S22 Ultra'
    ios_platformVersion: Literal['14', '15', '16'] = '14'
    ios_deviceName: Literal[
        'iPhone 14 Pro Max',
        'iPhone XS',
        'iPhone 11',
    ] = 'iPhone 14 Pro Max'


config = Config(_env_file=os.path.join(BASE_DIR, '.env'))

