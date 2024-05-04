from flask import Blueprint, request, jsonify
import json
from datetime import datetime
# import here so testing works
import psycopg2
# small change 11

app_routes = Blueprint('app_routes', __name__)

@app_routes.route('/')
def welcome():
    return jsonify({'message': 'Welcome to Fitness Buddy Backend!'})

@app_routes.route('/workouts', methods=['GET'])
def workouts():
    # does this need to be dynamically imported? 
    import psycopg2
    from psycopg2.extras import RealDictCursor
    params = {
        "dbname": "postgres",
        "user": "postgres",
        "password": "_XZUt-7U.QZCCV6c",
        "host": "datastore.cnwc620s2iep.us-east-1.rds.amazonaws.com",
        "port": "5432"
    }
    conn = psycopg2.connect(**params)

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        sql = ("SELECT * "
               "FROM workouts "
               "WHERE name ILIKE %s")
        search = "%" + request.args.get("name", None) + "%"
        cur.execute(sql, (search,))
        results = cur.fetchall()
    return results


@app_routes.route('/sign_up', methods=["POST"])
def sign_up():
    if request.method == "POST":
        try:
            json_data = request.get_json()
        except json.JSONDecodeError:
            return jsonify({'error': 'Invalid JSON data'}), 400

        if not json_data:
            return jsonify({'error': 'No data provided'}), 400
        username = json_data.get('username')
        email = json_data.get('email')
        password = json_data.get('password')

        import psycopg2
        params = {
            "dbname": "postgres",
            "user": "postgres",
            "password": "_XZUt-7U.QZCCV6c",
            "host": "datastore.cnwc620s2iep.us-east-1.rds.amazonaws.com",
            "port": "5432"
        }
        conn = psycopg2.connect(**params)
        with conn.cursor() as cur:
            sql = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
            cur.execute(sql, (username, email, password))
        conn.commit()
        return jsonify({'message': 'Logged in', "username": username})

@app_routes.route("/sign_in", methods=["POST"])
def sign_in():
    if request.method == "POST":
        try:
            json_data = request.get_json()
        except json.JSONDecodeError:
            return jsonify({"error": "Invalid JSON data"})

        if not json_data:
            return jsonify({"error": "No data provided"})

        email = json_data.get('email')
        password = json_data.get('password')

        import psycopg2
        from psycopg2.extras import RealDictCursor
        params = {
            "dbname": "postgres",
            "user": "postgres",
            "password": "_XZUt-7U.QZCCV6c",
            "host": "datastore.cnwc620s2iep.us-east-1.rds.amazonaws.com",
            "port": "5432"
        }
        conn = psycopg2.connect(**params)
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            sql = "SELECT username FROM users WHERE email=%s AND password=%s"
            cur.execute(sql, (email, password))
            results = cur.fetchall()[0]
        conn.commit()
        return jsonify(results)

@app_routes.route("/add_progress", methods=['POST'])
def add_progress():
    if request.method == 'POST':
        try:
            json_data = request.get_json()
        except TypeError:
            return jsonify({'error': 'Invalid JSON data'}), 400

        if not json_data:
            return jsonify({'error': 'No data provided'}), 400
        username = json_data.get("user")
        import psycopg2
        params = {
            "dbname": "postgres",
            "user": "postgres",
            "password": "_XZUt-7U.QZCCV6c",
            "host": "datastore.cnwc620s2iep.us-east-1.rds.amazonaws.com",
            "port": "5432"
        }
        conn = psycopg2.connect(**params)
        with conn.cursor() as cur:
            sql = "SELECT * FROM users WHERE username=%s"
            cur.execute(sql, (username,))
            user_exists = cur.fetchone()

        if not user_exists:
            return jsonify({'error': 'User does not exist'}), 400

        workout_name = json_data.get("workout_name")
        date = datetime.fromtimestamp(json_data.get("date"))
        reps = json_data.get("reps")
        sets = json_data.get("sets")
        weight = json_data.get("weight")

        with conn.cursor() as cur:
            sql = ("INSERT INTO progress (username, workout_name, reps, sets, weight, date)"
                   "VALUES (%s, %s, %s, %s, %s, %s)")
            cur.execute(sql, (username, workout_name, reps, sets, weight, date))

        conn.commit()
        return jsonify({"message": "record created"}), 201
    else:
        return jsonify({'error': 'Must be POST'}), 405

@app_routes.route("/progress")
def view_progress():
    if request.method == 'GET':
        username = request.args.get('username', None)
        if not username:
            return jsonify({"error": "Username is required"})
        import psycopg2
        from psycopg2.extras import RealDictCursor
        params = {
            "dbname": "postgres",
            "user": "postgres",
            "password": "_XZUt-7U.QZCCV6c",
            "host": "datastore.cnwc620s2iep.us-east-1.rds.amazonaws.com",
            "port": "5432"
        }
        conn = psycopg2.connect(**params)
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            sql = "SELECT * FROM progress WHERE username=%s"
            cur.execute(sql, (username,))
            results = cur.fetchall()
        return jsonify(results)
    return jsonify({"error": "must be GET"}), 405