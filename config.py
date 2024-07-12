class Config:
    SECRET_KEY = '3c8ff256d2a34811bb0a2c11ea1e124d2f8c9d5d7a3e4b6f'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'dbmusica'
    
class DevelopmentConfig(Config):
    DEBUG = True


config = {
    'development': DevelopmentConfig
}