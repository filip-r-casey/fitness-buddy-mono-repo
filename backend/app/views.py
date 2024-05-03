from flask import Blueprint, request, jsonify
import json
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor

app_routes = Blueprint('app_routes', __name__)

@app_routes.route('/')
def welcome():
    return jsonify({'message': 'Welcome to Fitness Buddy Backend!'})

@app_routes.route('/workouts', methods=['GET'])
def workouts():
    # Updated database connection
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="_XZUt-7U.QZCCV6c",
        host="datastore.cnwc620s2iep.us-east-1.rds.amazonaws.com",
        port="5432"
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM workouts")
    workouts = cur.fetchall()
    return jsonify(workouts)

@app_routes.route('/events/<int:event_id>/messages', methods=['POST'])
def post_message(event_id):
    content = request.json['content']
    sender_id = request.json['sender_id']  # Assuming sender's ID is provided in the request
    try:
        # Updated database connection
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="_XZUt-7U.QZCCV6c",
            host="datastore.cnwc620s2iep.us-east-1.rds.amazonaws.com",
            port="5432"
        )
        cur = conn.cursor()
        cur.execute("INSERT INTO messages (event_id, sender_id, content) VALUES (%s, %s, %s)",
                    (event_id, sender_id, content))
        conn.commit()
        return jsonify({'status': 'success'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app_routes.route('/events/<int:event_id>/messages', methods=['GET'])
def get_messages(event_id):
    try:
        # Updated database connection
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="_XZUt-7U.QZCCV6c",
            host="datastore.cnwc620s2iep.us-east-1.rds.amazonaws.com",
            port="5432"
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM messages WHERE event_id = %s ORDER BY timestamp DESC", (event_id,))
        messages = cur.fetchall()
        return jsonify(messages), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
