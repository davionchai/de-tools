import psycopg2

conn = psycopg2.connect(
    dbname="randomizer",
    user="admin",
    host="localhost",
    password="password",
    port="5433",
)

cursor = conn.cursor()
cursor.execute("select * from hydaelyn.eorzea_population;")
rows = cursor.fetchall()
for table in rows:
    print(table)
conn.close()
