import serial
import psycopg2
import time
from configparser import ConfigParser

# x = str(serial.readline().strip())[2:-1]
# if x:
#     x = x.split(",")
#     num = x[0]
#     speed = x[1]
#     altitude = x[2]
#     print(x)
#     print()


def connect():
    """Connect to the PostgreSQL database server"""
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print("Connecting to the PostgreSQL database...")
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement

        print("PostgreSQL database version:")
        cur.execute("SELECT version()")

        # display the PostgreSQL database server version
        # db_version = cur.fetchone()
        # print(db_version)

        # # close the communication with the PostgreSQL
        # cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    # finally:
    #     if conn is not None:
    #         conn.close()
    #         print("Database connection closed.")
    return conn


def config(filename="database.ini", section="postgresql"):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            "Section {0} not found in the {1} file".format(section, filename)
        )

    return db


if __name__ == "__main__":
    conn = connect()
    cur = conn.cursor()
    serial = serial.Serial("COM3", 9600, timeout=1)
    if not serial.isOpen():
        serial.open()
    print("com3 is open", serial.isOpen())
    i = 0
    # conn = psycopg2.connect("dbname=sensores user=postgres password=postgres")
    while True:
        if i > 5:
            break
        x = str(serial.readline().strip())[2:-1]
        x = x.split(",")
        print(x)
        command1 = "insert into sensordata (id, value, time) values (%s, %s, %s)" % (
            int(i),
            int(x[1]),
            int(x[0]),
        )
        cur.execute(command1)

        # execute query
        cur.execute("select id, value from sensordata")

        rows = cur.fetchall()

        for r in rows:
            print(f"id {r[0]} value {r[1]}")

        # commit the transcation
        conn.commit()
        i += 1
        # close the cursor
    cur.close()

    # close the connection
    conn.close()
#     # num = x[0]
#     # speed = x[1]
#     # altitude = x[2]
#     print(x)
#     print()
