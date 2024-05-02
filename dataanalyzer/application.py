import psycopg2
import psycopg2.extensions
import select
import threading


def listen_for_notifications():
    params = {
        "dbname": "postgres",
        "user": "postgres",
        "password": "_XZUt-7U.QZCCV6c",
        "host": "datastore.cnwc620s2iep.us-east-1.rds.amazonaws.com",
        "port": "5432"
    }
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="_XZUt-7U.QZCCV6c", host="datastore.cnwc620s2iep.us-east-1.rds.amazonaws.com")
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    curs = conn.cursor()
    curs.execute("LISTEN my_notification;")

    print("Listening for notifications on channel 'my_notification'")
    while True:
        if select.select([conn], [], [], 5) == ([], [], []):
            print("Timeout, no messages")
        else:
            conn.poll()
            while conn.notifies:
                notify = conn.notifies.pop(0)
                print("Received NOTIFY:", notify.pid, notify.channel, notify.payload)
                # Here you can trigger any specific function or handle the notification
                handle_database_update(notify.payload)


def handle_database_update(data):
    print("Handle logic for updated data:", data)


def start_listener_thread():
    thread = threading.Thread(target=listen_for_notifications, daemon=True)
    thread.start()
