from flask import Flask, jsonify, request
import mysql.connector
import os
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Статическая информация о приложении как метрика
metrics.info('app_info', 'Application info', version='1.0.3')

def get_db_connection():
    connection = mysql.connector.connect(
        host=os.getenv('MYSQL_HOST'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DATABASE')
    )
    return connection

@app.route('/smartphones', methods=['GET'])
def get_smartphones():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM smartphones')
    smartphones = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(smartphones)

@app.route('/skip')
@metrics.do_not_track()
def skip():
    return "This route is not tracked for metrics."

@app.route('/<item_type>')
@metrics.do_not_track()
@metrics.counter('invocation_by_type', 'Number of invocations by type',
         labels={'item_type': lambda: request.view_args['item_type']})
def by_type(item_type):
    return f"Type: {item_type}"

@app.route('/long-running')
@metrics.gauge('in_progress', 'Long running requests in progress')
def long_running():
    return "Long running request"

@app.route('/status/<int:status>')
@metrics.do_not_track()
@metrics.summary('requests_by_status', 'Request latencies by status',
                 labels={'status': lambda r: r.status_code})
@metrics.histogram('requests_by_status_and_path', 'Request latencies by status and path',
                   labels={'status': lambda r: r.status_code, 'path': lambda: request.path})
def echo_status(status):
    return f'Status: {status}', status

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

