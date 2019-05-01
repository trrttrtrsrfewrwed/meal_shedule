import flask
import argparse
from database import *

app = flask.Flask("meal_schedule")
app.check_info = 'meal_shedule'


@app.route('/get_shedule_names', methods=['GET'])
def get_shedule_names():
    return json.dumps(get_names(SHEDULES_TABLE_NAME))


@app.route('/get_dayshedule_names', methods=['GET'])
def get_dayshedule_names():
    return json.dumps(get_names(DAYSHEDULES_TABLE_NAME))


@app.route('/get_meal_names', methods=['GET'])
def get_meal_names():
    return json.dumps(get_names(MEALS_TABLE_NAME))


@app.route('/get_shedule', methods=['GET'])
def get_shedule():
    if 'name' in flask.request.args:
        return json.dumps(get(SHEDULES_TABLE_NAME, flask.request.args['name']))


@app.route('/get_dayshedule', methods=['GET'])
def get_dayshedule():
    if 'name' in flask.request.args:
        return json.dumps(get(DAYSHEDULES_TABLE_NAME, flask.request.args['name']))


@app.route('/get_meal', methods=['GET'])
def get_meal():
    if 'name' in flask.request.args:
        return json.dumps(get(MEALS_TABLE_NAME, flask.request.args['name']))


@app.route('/get_notifier', methods=['GET'])
def get_notifier_():
    return json.dumps(get_notifier()) + "\n"


@app.route('/check', methods=['GET'])
def check():
    return json.dumps({"check_info": app.check_info}) + "\n"


@app.route('/set_notifier', methods=['POST'])
def set_notifier():
    received_json_data = json.loads(flask.request.data)
    update_notifier(received_json_data)
    return 'OK'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subs = parser.add_subparsers()
    run_parser = subs.add_parser('run')
    database_parser = subs.add_parser('create_database')
    drop_parser = subs.add_parser('drop_database')
    run_parser.set_defaults(method='run')
    run_parser.add_argument('--port', default=50000, type=int)
    database_parser.set_defaults(method='create_database')
    drop_parser.set_defaults(method='drop_database')

    args = parser.parse_args()
    if args.method == 'run':
        database_params['dbname'] = DATABASE_NAME
        app.run('127.0.0.1', args.port, threaded=True)
    elif args.method == 'create_database':
        create_database()
        create_tables()
    elif args.method == 'drop_database':
        drop_database()
