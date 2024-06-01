from abc import ABCMeta, abstractmethod
import os

class Actions(metaclass=ABCMeta):
    
    def __init__(self, client):
        self.client = client
        self.env = {
            'development': self.development,
            'test': self.test,
            'production': self.production,
        }

    @abstractmethod
    def development(self, ):
        raise NotImplementedError()

    @abstractmethod
    def test(self,):
        raise NotImplementedError()

    @abstractmethod
    def production(self, ):
        raise NotImplementedError()

    def exec(self, ):
        return self.env[os.environ['ENVIRONMENT']]


class Config(metaclass=ABCMeta):

    def __init__(self, env):
        self.env = env
        self.bot_token = os.environ['BOT_TOKEN']

    def get_token(self, ):
        return self.bot_token


class DataBase(metaclass=ABCMeta):
    
    def __init__(self, env, name):
        self.env = env
        self.name = name
    
    # def connect(self, ):
    #     connection = MySQLdb.connect(
    #         host=os.os.environ['MYSQL_HOST'],
    #         user=os.os.environ['MYSQL_USER'],
    #         passwd=os.os.environ['MYSQL_PASSWORD'],
    #         db=os.os.environ['MYSQL_DATABASE'],
    #     )
    #     return connection.cursor()
        
    @abstractmethod
    def define_columns(self, ):
        raise NotImplementedError()

    @abstractmethod
    def update(self,):
        raise NotImplementedError()

    @abstractmethod
    def commit(self, ):
        raise NotImplementedError()