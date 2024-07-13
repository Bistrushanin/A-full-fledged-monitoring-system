from flask import Flask, jsonify
import mysql.connector
import os
from prometheus_client import generate_latest, Counter, Histogram, make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

app = Flask(__name__)

REQUEST_COUNT = Counter('request_count', 'Total Request Count')
LATENCY = Histogram('request_latency_seconds', 'Request latency in seconds')

def get_db_connection():
    connection = mysql.connector.connect(
        host=os.getenv('MYSQL_HOST'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DATABASE')
    )
    return connection

@app.route('/smartphones', methods=['GET'])
@LATENCY.time()
def get_smartphones():
    REQUEST_COUNT.inc()
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM smartphones')
    smartphones = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(smartphones)

# Добавляем маршрут для метрик
@app.route('/metrics')
def metrics():
    return generate_latest()

# Приложение Flask должно использовать DispatcherMiddleware для объединения приложений
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

