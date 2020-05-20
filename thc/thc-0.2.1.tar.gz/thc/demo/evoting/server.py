import threading
import http.server
import sqlite3
from functools import partial

from ._votingserver import VotingServer

def init_db (db_file):
    try:
        db = sqlite3.connect('file:' + db_file + '?mode=rw', uri=True)
        db.close()
    except:
        from pkgutil import get_data
        print('> Initializing database in ' + db_file + '… ', end='')
        try:
            sql = get_data(__package__, 'init-db.sql').decode('utf-8')
            db = sqlite3.connect('file:' + db_file + '?mode=rwc', uri=True)
            db.executescript(sql)
            db.close()
            print('done!')
        except:
            print('failure!')
            sys.exit(1)

def web_server (host, port, db_file):
    httpd = http.server.ThreadingHTTPServer((host, port),
                                            partial(VotingServer, db_file))
    print('> Voting server starting…')
    web = threading.Thread(target=lambda: httpd.serve_forever())
    try:
        web.start()
        print('> Voting server listing on ' + host + ':' + str(port))
        web.join()
    except KeyboardInterrupt:
        print('> Voting server exiting…')
        httpd.shutdown()
    web.join()

def main ():
    import argparse
    ap = argparse.ArgumentParser(description='THC demo e-voting server.')
    ap.add_argument('-H', '--host', default='127.0.0.1', type=str,
                    help=('hostname to bind the HTTP server to '
                          '(default is "127.0.0.1")'))
    ap.add_argument('-p', '--port', default=9380, type=int,
                    help=('port to bind the HTTP server to '
                          '(default is 9380)'))
    ap.add_argument('-d', '--db', default='votes.db', type=str,
                    help=('SQLite database file name '
                          '(default is "votes.db")'))
    args = ap.parse_args()
    init_db(args.db)
    web_server(args.host, args.port, args.db)

if __name__ == '__main__':
    main()
