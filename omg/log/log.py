from omg.factory import Factory
from omg.config import Config

class Log(Factory):
    configname = 'log_type'
    configsource = Config()
