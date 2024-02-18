#!/usr/bin/python3
""" The new class for sqlAlchemy """
from os import getenv
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import (create_engine)
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """ creating tables in environmental"""
    __engine = None
    __session = None

    def __init__(self):
        user = getenv("HBNB_MYSQL_USER")
        passwd = getenv("HBNB_MYSQL_PWD")
        myDB = getenv("HBNB_MYSQL_DB")
        host = getenv("HBNB_MYSQL_HOST")
        myEnv = getenv("HBNB_ENV")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, passwd, host, myDB),
                                      pool_pre_ping=True)

        if myEnv == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returning a dictionary of __object"""
        myDic = {}
        if cls:
            if type(cls) is str:
                cls = eval(cls)
            myQuery = self.__session.query(cls)
            for myElem in myQuery:
                k = "{}.{}".format(type(myElem).__name__, myElem.id)
                myDic[k] = myElem
        else:
            myList = [State, City, User, Place, Review, Amenity]
            for c in myList:
                myQuery = self.__session.query(c)
                for myElem in myQuery:
                    k = "{}.{}".format(type(myElem).__name__, myElem.id)
                    myDic[k] = myElem
        return (myDic)

    def new(self, obj):
        """Adding a new elem in the table"""
        self.__session.add(obj)

    def save(self):
        """Saving changes"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deleting an elem in the table"""
        if obj:
            self.session.delete(obj)

    def reload(self):
        """The configuration"""
        Base.metadata.create_all(self.__engine)
        s = sessionmaker(bind=self.__engine, expire_on_commit=False)
        mySess = scoped_session(s)
        self.__session = mySess()

    def myClose(self):
        """ Calling remove() """
        self.__session.close()
