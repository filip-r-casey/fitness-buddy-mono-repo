import psycopg2
from psycopg2.extras import RealDictCursor
import psycopg2.extensions
import select
import threading
import json


def listen_for_notifications():
    params = {
        "dbname": "postgres",
        "user": "postgres",
        "password": "_XZUt-7U.QZCCV6c",
        "host": "datastore.cnwc620s2iep.us-east-1.rds.amazonaws.com",
        "port": "5432"
    }
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="_XZUt-7U.QZCCV6c",
                            host="datastore.cnwc620s2iep.us-east-1.rds.amazonaws.com")
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    curs = conn.cursor()
    curs.execute("LISTEN my_notification;")

    print("Listening for notifications on channel 'my_notification'")
    while True:
        if select.select([conn], [], [], 5) == ([], [], []):
            continue
        else:
            conn.poll()
            while conn.notifies:
                notify = conn.notifies.pop(0)
                print("Received NOTIFY:", notify.pid, notify.channel, notify.payload)
                # Here you can trigger any specific function or handle the notification
                handle_database_update(notify.payload)


def update_records(past, curs, weight, reps, sets, workout_name, username, date, conn):
    prev_record = next((d for d in past if d.get("record") == True), None)
    if prev_record:
        if prev_record["weight"]:
            prev_score = prev_record["weight"] * prev_record["reps"] * prev_record["sets"]
            new_score = weight * reps * sets
        else:
            prev_score = prev_record["reps"] * prev_record["sets"]
            new_score = reps * sets
        if new_score > prev_score:
            sql = ("UPDATE progress SET record=true "
                   "WHERE workout_name=%s AND username=%s AND date=%s ")
            curs.execute(sql, (workout_name, username, date))
            sql = ("UPDATE progress SET record=false "
                   "WHERE workout_name=%s AND username=%s AND date=%s ")
            curs.execute(sql, (prev_record["workout_name"], prev_record["username"], prev_record["date"]))
    else:
        sql = ("UPDATE progress SET record=true "
               "WHERE workout_name=%s AND username=%s AND date=%s ")
        curs.execute(sql, (workout_name, username, date))
    conn.commit()


def user_stats(past, curs, conn, username, workout_name):
    import pandas as pd
    import numpy as np

    data = pd.DataFrame(past)
    average_reps = np.average(data["reps"])
    average_sets = np.average(data["sets"])
    if data["weight"].notnull().all():
        average_weight = np.average(data["weight"])
        average_score = np.average(data["reps"] * data["sets"] * data["weight"])
        std_score = np.std(data["reps"] * data["sets"] * data["weight"])
    else:
        average_weight = None
        average_score = np.average(data["reps"] * data["sets"])
        std_score = np.std(data["reps"] * data["sets"])
    sql = (
        "INSERT INTO user_workout_stats (username, workout_name, average_reps, average_sets, average_weight, average_score, std_score) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s) "
        "ON CONFLICT (username, workout_name) DO UPDATE "
        "SET average_reps = excluded.average_reps, "
        "average_sets = excluded.average_sets, "
        "average_weight = excluded.average_weight, "
        "average_score = excluded.average_score, "
        "std_score = excluded.std_score")
    curs.execute(sql, (username, workout_name, average_reps, average_sets, average_weight, average_score, std_score))
    conn.commit()


def handle_database_update(data):
    print("Handle logic for updated data:", data)
    data = json.loads(data)
    username = data["username"]
    workout_name = data["workout_name"]
    reps = data["reps"]
    sets = data["sets"]
    weight = data["weight"]
    date = data["date"]
    params = {
        "dbname": "postgres",
        "user": "postgres",
        "password": "_XZUt-7U.QZCCV6c",
        "host": "datastore.cnwc620s2iep.us-east-1.rds.amazonaws.com",
        "port": "5432"
    }
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="_XZUt-7U.QZCCV6c",
                            host="datastore.cnwc620s2iep.us-east-1.rds.amazonaws.com")
    curs = conn.cursor(cursor_factory=RealDictCursor)
    sql = ("SELECT * FROM progress WHERE username=%s AND workout_name=%s")
    curs.execute(sql, (username, workout_name))
    past = curs.fetchall()
    update_records(past, curs, weight, reps, sets, workout_name, username, date, conn)
    user_stats(past, curs, conn, username, workout_name)


def start_listener_thread():
    thread = threading.Thread(target=listen_for_notifications, daemon=True)
    thread.start()
