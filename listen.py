import eventlet
from eventlet import wsgi
from eventlet import websocket

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from eventlet.hubs import trampoline

def dblisten(q):
    """
    Open a db connection and add notifications to *q*.
    """
    cnn = psycopg2.connect(dsn)
    cnn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = cnn.cursor()
    cur.execute("LISTEN data;")
    while 1:
        trampoline(cnn, read=True)
        cnn.poll()
        while cnn.notifies:
            n = cnn.notifies.pop()
            q.put(n)

@websocket.WebSocketWSGI
def handle(ws):
	q = eventlet.Queue()
    eventlet.spawn(dblisten, q)
    while 1:
        n = q.get()
        print n
        ws.send(n.payload)