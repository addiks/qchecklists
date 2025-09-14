
import sys, os, logging
from os.path import dirname, abspath

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from py.Application import Application

if __name__ == "__main__":
    logger = logging.getLogger('qchecklists')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(JournalHandler(SYSLOG_IDENTIFIER='qchecklists'))
    Log.registerLogger(logger)
        
    sys.exit(Application.main(sys.argv))