"""
SQLALCHEMY_DATABASE_URI = location of the app's db
"""

import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir,'.env')) # app을 시작할때 .env파일을 실행

class Config(object):
	ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-nerver-guess'
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	MAIL_SERVER = os.environ.get('MAIL_SERVER')
	MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
	MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')
	ADMINS = ['your-email@example.com'] # 오류보고서를 수신할 이메일 주소 목록
	POSTS_PER_PAGE = 25
	LANGUAGES = 'ko'
