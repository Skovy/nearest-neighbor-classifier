import psycopg2
import os
import urlparse

class TrackData:
    def __init__(self):
        self.conn = None
        self.cur = None
        self.connect()

    def connect(self):
        try:
            urlparse.uses_netloc.append("postgres")
            url = urlparse.urlparse(os.environ["DATABASE_URL"])

            self.conn = psycopg2.connect(
                database=url.path[1:],
                user=url.username,
                password=url.password,
                host=url.hostname,
                port=url.port
            )
            self.cur = self.conn.cursor()
        except:
            print "Unable to connect to the database."

    # retrieve the data from the database
    def retrieve_data(self, limit_total):
        sql = """SELECT name,
            spotify_uri,
            id,
            round(danceability::numeric, 8),
            round(loudness::numeric, 8),
            round(energy::numeric, 8),
            round(speechiness::numeric, 8),
            round(liveness::numeric, 8),
            round(acousticness::numeric, 8),
            round(instrumentalness::numeric, 8) FROM tracks
            ORDER BY id ASC LIMIT %s;"""
        self.cur.execute(sql, [limit_total])

        data = []
        for index, row in enumerate(self.cur.fetchall()):
            data.append([])
            for col in row:
                data[index].append(col)
        return data

    def close(self):
        self.cur.close()
        self.conn.close()
