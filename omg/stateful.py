class Stateful(object):
    __state = {}

    def _state(self):
        if self.__class__.__state:
            self.__dict__ = self.__class__.__state
            return True
        else:
            self.__class__.__state = self.__dict__
            return False

