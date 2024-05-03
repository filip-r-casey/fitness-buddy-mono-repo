import requests
import psycopg2
def lambda_handler(event, context):
    # small change 23
    params = {
        "dbname": "postgres",
        "user": "postgres",
        "password": "_XZUt-7U.QZCCV6c",
        "host": "datastore.cnwc620s2iep.us-east-1.rds.amazonaws.com",
        "port": "5432",
        "sslmode": "require"
    }

    conn = psycopg2.connect(**params)

    cur = conn.cursor()

    current_pages = 10000
    api_headers = {
        "X-Api-Key": "DQ0BRks/FbPbANkPVS0JNw==GJJNP1vx1wzVwG2D"
    }
    api_url = "https://api.api-ninjas.com/v1/exercises"
    sql =("INSERT INTO workouts(name, type, muscle, equipment, difficulty, instructions)"
          "VALUES (%s, %s, %s, %s, %s, %s)"
          "ON CONFLICT (name)"
          "DO NOTHING")

    for page in range(1, current_pages, 10):
        response = requests.get(api_url + "?offset=" + str(page), headers=api_headers)
        if len(response.json()) == 0:
            break
        for workout in response.json():
            data = tuple(workout.values())
            cur.execute(sql, data)
        conn.commit()

    cur.close()
    conn.close()