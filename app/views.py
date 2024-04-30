from flask import Blueprint, request, jsonify

app_routes = Blueprint('app_routes', __name__)


@app_routes.route('/')
def welcome():
    return jsonify({'message': 'Welcome to Fitness Buddy Backend!'})


@app_routes.route('/workouts', methods=['GET'])
def workouts():
    import psycopg2
    from psycopg2.extras import DictCursor
    params = {
        "dbname": "postgres",
        "user": "postgres",
        "password": "_XZUt-7U.QZCCV6c",
        "host": "datastore.cnwc620s2iep.us-east-1.rds.amazonaws.com",
        "port": "5432"
    }
    conn = psycopg2.connect(**params)

    with conn.cursor(cursor_factory=DictCursor) as cur:
        sql = ("SELECT * "
               "FROM workouts "
               "WHERE name ILIKE %s")
        search = "%" + request.args.get("search", None) + "%"
        cur.execute(sql, (search,))
        results = cur.fetchall()
        print(results)
    return results
