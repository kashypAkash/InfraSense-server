import pymysql, os

from peewee import *

DATABASE = MySQLDatabase('infraSense-dev', user='root', passwd='root', host='127.0.0.1', port=3306)


class User(Model):
    """A base model that will use our MySQL database"""
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=40)
    is_admin = BooleanField(default=False)

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User],safe=True)

