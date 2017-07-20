"""
health check for f5
"""

#!/usr/bin/python3


import elasticsearch
from elasticsearch import Transport
import socket
import threading
import urllib3
import time


def client_thread(conn):
    try:
        #Sending message to connected client
        conn.send(bytearray("F5 HealthCheck\t\n Press Any Key to Disconnect", "utf-8"))

        #infinite loop so that function do not terminate and thread do not end.
        while True:

            #Receiving from client
            data = conn.recv(1024)
            if data:
                conn.close()
                break
    except ConnectionAbortedError:
        conn.close()


    #came out of loop
    conn.close()

def accept_thread(sock):
    try:
        conn = sock.accept()
        thread = threading.Thread(target=client_thread, args=(conn[0],))
        thread.start()
    except SystemExit:
        sock.close()
    except OSError:
        sock.close()
    except ConnectionAbortedError:
        sock.close()
    except TimeoutError:
        sock.close()

def main():

    s = socket.socket()
    while True:
        client = elasticsearch.Elasticsearch(transport_class=Transport,
                                             hosts=,
                                             http_auth=)
        try:
            if client.ping():
                if client.cat.health(format='json')[0]['status'] == 'red':
                    print('server is down')
                    s.close()
                    try:
                        msg = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        msg.connect(('localhost', 10000))
                        msg.send(bytearray('a', 'utf-8'))
                        msg.close()
                    except ConnectionAbortedError:
                        pass
                    except ConnectionRefusedError:
                        pass
                    time.sleep(5)
                else:
                    print('server is up')
                    try:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.settimeout(10)
                        s.bind(("", 10000))
                        s.listen(1)

                    except OSError:
                        pass
                    thread = threading.Thread(target=accept_thread, args=(s,))
                    thread.start()
                    time.sleep(5)

        except ConnectionRefusedError:
            s.close()
            try:
                msg = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                msg.connect(('localhost', 10000))
                msg.send(bytearray('a', 'utf-8'))
                msg.close()
            except ConnectionAbortedError:
                pass
            time.sleep(5)
        except urllib3.exceptions.NewConnectionError:
            s.close()
            try:
                msg = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                msg.connect(('localhost', 10000))
                msg.send(bytearray('a', 'utf-8'))
                msg.close()
            except ConnectionAbortedError:
                msg.close()
            time.sleep(5)
        except elasticsearch.exceptions.ConnectionError:
            s.close()
            try:
                msg = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                msg.connect(('localhost', 10000))
                msg.send(bytearray('a', 'utf-8'))
                msg.close()
            except ConnectionAbortedError:
                msg.close()
            time.sleep(5)
        except Exception:
            s.close()
            try:
                msg = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                msg.settimeout(10)
                msg.connect(('localhost', 10000))
                msg.send(bytearray('a', 'utf-8'))
                msg.close()
            except ConnectionAbortedError:
                msg.close()
            except TimeoutError:
                msg.close()
            time.sleep(5)

    s.close()

if __name__ == "__main__":
    main()
