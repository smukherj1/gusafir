import webbrowser
import subprocess
import time
import os
import urllib2
import uuid
import atexit
import logging

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
SERVER_SCRIPT = os.path.join(SCRIPT_DIR, 'gusafir_server.py')
HOST = '0.0.0.0'
PORT = 8080
TEST_PAGE = str(uuid.uuid1())
_log = logging.getLogger(__name__)
logging.basicConfig(format='[%(asctime)s][%(levelname)s]   %(message)s', level=logging.INFO)

if __name__ == '__main__':
    _log.info('Welcome to Gusafir 2.0')
    _log.info('Attemping to start the Gusafir Server. We will attempt 10 different ports before giving up.')
    p = None

    def cleanup():
        if p:
            try:
                p.kill()
            except OSError:
                pass
        return

    atexit.register(cleanup)
    success = False
    for iport in range(PORT, PORT + 1001, 100):
        addr = 'http://%s:%d'%(HOST, iport)
        _log.info('Attemping to start the Gusafir Server on %s'%addr)
        p = subprocess.Popen(['python' , SERVER_SCRIPT, HOST, str(iport), TEST_PAGE])
        while p.poll() == None:
            time.sleep(1)
            try:
                resp = urllib2.urlopen(addr + '/' + TEST_PAGE)
                success = True
                _log.info('Gusafir is alive at %s'%addr)
                webbrowser.open(addr, autoraise=True)
                break
            except urllib2.URLError:
                pass
        if success:
            break
        else:
            try:
                p.kill()
            except OSError:
                pass
    if not success:
        _log.error('Gusafir 2.0 failed to start :(')
        exit(-1)
    elif p:
        try:
            p.wait()
        except OSError:
            pass
