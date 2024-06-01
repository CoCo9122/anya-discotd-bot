from interfaces import Config

class Development(Config):
    
    def __init__(self, ):
        super().__init__('development')

class Test(Config):

    def __init__(self, ):
        super().__init__('test')

class Production(Config):

    def __init__(self, ):
        super().__init__('production')