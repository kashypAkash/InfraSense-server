import pymysql, os

from peewee import *

DATABASE = MySQLDatabase('infraSense-dev', user='root', passwd='root', host='127.0.0.1', port=3306)

class Admin(Model):
    UserName = CharField(unique=True)
    EmailId = CharField(unique=True)
    Password = CharField(max_length=40)

    class Meta:
        database = DATABASE

class User(Model):
    """A base model that will use our MySQL database"""
    UserName = CharField(unique=True)
    Password = CharField(max_length=40)
    EmailId = CharField(unique=True)

    class Meta:
        database = DATABASE

class SensorDetails(Model):
    SensorType = CharField(max_length=20)
    Region = CharField(max_length=20)
    ChargePerHour = IntegerField(default=0)

    class Meta:
        database = DATABASE

class SensorCluster(Model):
    SensorHubName = CharField(max_length=40)
    UserName = CharField(max_length=40)
    Status = CharField(max_length=40)

    class Meta:
        database = DATABASE

class Sensor(Model):
    UserName = CharField(max_length=40)
    SensorHubName = CharField(max_length=40)
    SensorId = CharField(unique=True)
    SensorType = CharField(max_length=40)
    Status = CharField(max_length=40)

    class Meta:
        database = DATABASE

class UserSensorHubDetails(Model):
    """A base model that will use our MySQL database"""
    username = CharField(max_length=40)
    SensorHubName = CharField(max_length=40)
    SensorId = CharField(unique=True)
    SensorType = CharField(max_length=40)
    Status = CharField(max_length=40)

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Admin, User, SensorDetails, SensorCluster, Sensor, UserSensorHubDetails ],safe=True)

