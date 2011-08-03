from omg.defaults import Defaults
from omg.log.file import FileLog
from omg.log.levels import *
import omg.log as _log

def setup(service=None):
    d = Defaults()
    try:
        path = d['log_path'] if d.has_key('log_path') else None
        _log.hose = _log.hoses[d['log_type']](service, path)
        debug("Logging setup")
    except KeyError:
        print "Unknown logging type"

def log(msg, level=None):
    if not level:
        level = INFO
    try:
        _log.hose.drip(msg, level)
    except Exception:
        print "Exception while attempting to spew log data"
        import traceback
        traceback.print_exc()

def debug(msg):
    log(msg, DEBUG)

def info(msg):
    log(msg, INFO)

def warn(msg):
    log(msg, WARN)

def error(msg):
    log(msg, ERROR)

def crit(msg):
    log(msg, CRIT)

def fatal(msg):
    log(msg, FATAL)

def open_files():
    return _log.hose.open_files()

