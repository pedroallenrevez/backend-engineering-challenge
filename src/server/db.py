from psycopg2 import connect


class PSQLConnector:
    UPSERT = (
        lambda ts, dur: f"""INSERT INTO metrics("date", average_delivery_time) VALUES('{ts}', {dur}) ON CONFLICT ("date") DO UPDATE SET average_delivery_time = {dur};"""
    )

    def __init__(self):
        self.conn = connect(
            dbname="postgres", user="postgres", host="localhost", password="test"
        )

    def exe(self, query: str):
        cur = self.conn.cursor()
        try:
            cur.execute(query)
        except Exception as e:
            print(e)

        self.conn.commit()
        cur.close()

    def create_db(self):
        self.exe(
            """CREATE TABLE metrics( "date" TIMESTAMP PRIMARY KEY, average_delivery_time FLOAT );"""
        )

    def clear(self):
        self.exe("DELETE FROM metrics;")

    def test_insert(self):
        self.exe(PSQLConnector.UPSERT("2000-01-03 00:00:00", 1.0))

    def insert(self, ts: str, dur: float):
        self.exe(PSQLConnector.UPSERT(ts, dur))


psql = PSQLConnector()
psql.create_db()
# psql.test_insert()
# psql.test_insert()
