from __future__ import unicode_literals
import time
from reporter import *


def timeit(method):
    def timed(*args, **kw):
        ts = datetime.utcnow()
        result = method(*args, **kw)
        te = datetime.utcnow()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = (te - ts) * 1000
        else:
            Reporter().addReport(method.__name__, (te - ts).microseconds / 100)
            # print '%r  %2.2f ms' % \
            #       (method.__name__, (te - ts) * 1000)
        return result
    return timed
