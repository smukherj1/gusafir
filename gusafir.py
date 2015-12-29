import webbrowser
import subprocess
import time
import os
import urllib2
import uuid
import atexit


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
SERVER_SCRIPT = os.path.join(SCRIPT_DIR, 'gusafir_server.py')
HOST = '0.0.0.0'
PORT = 8080
TEST_PAGE = str(uuid.uuid1())

if __name__ == '__main__':
    print 'Info: Welcome to Gusafir 2.0'
    print 'Info: Attemping to start the Gusafir Server. We will attempt 10 different ports before giving up.'
    p = None

    def cleanup():
        if p:
            p.kill()
    atexit.register(cleanup)
    for iport in range(PORT, PORT + 10):
        addr = 'http://%s:%d'%(HOST, iport)
        print 'Info: Attemping to start the Gusafir Server on %s'%addr
        p = subprocess.Popen(['python' , SERVER_SCRIPT, HOST, str(iport), TEST_PAGE])
        time.sleep(5)
        try:
            resp = urllib2.urlopen(addr + '/%s'%TEST_PAGE)
            print 'Info: Gusafir is alive at %s'%addr
            print 'Info: A new tab has been opened in your default webbrowser pointing to Gusafir. Happy Gusifying!'
            webbrowser.open(addr, autoraise=True)
            break
        except urllib2.URLError:
            p.kill()
            continue
    if p:
        p.wait()
