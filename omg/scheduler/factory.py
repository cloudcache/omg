from omg.factory import Factory
from omg.config import Config

class Scheduler(Factory):
    configsource = Config()
    configname = 'scheduler_type'

