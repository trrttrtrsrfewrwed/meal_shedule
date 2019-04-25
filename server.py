import flask
import json
import argparse

# Будет удалено после завершения технических работ
import datetime
from shedule import RangeShedule, DayShedule, Shedule, Notifier

s1 = RangeShedule({'Milk': 3, 'Egg': 2, 'Meat': 100000}, 9, 11)
s2 = RangeShedule({'Milk': 3, 'Egg': 2, 'Meat': 100000}, 4, 22)
s3 = RangeShedule({'Milk': 1, 'Egg': 2, 'Meat': 100000}, 6)
s4 = RangeShedule({'Milk': 3, 'Egg': 3, 'Meat': 100000}, 9, 11)
s5 = RangeShedule({'Milk': 4, 'Egg': 2, 'Meat': 100000}, 13, 15)
s6 = RangeShedule({'Milk': 5, 'Egg': 1, 'Meat': 100000}, 8)
d1 = DayShedule([s1, s2, s3])
d2 = DayShedule([s4, s5, s6])

shed = Shedule([(datetime.date.today() + datetime.timedelta(days=1), d1), (datetime.date.today(), d2)])
dir_ = {'Milk': 5, 'Egg': 6}
notifier = Notifier(shed, dir_)
#
app = flask.Flask("meal_schedule")
app.json_notifier = notifier.get_json()
app.check_info = 'meal_shedule'


@app.route('/get_notifier', methods=['GET'])
def get_notifier():
    return json.dumps(app.json_notifier) + "\n"


@app.route('/check', methods=['GET'])
def check():
    return json.dumps({"check_info": app.check_info}) + "\n"


@app.route('/set_notifier', methods=['POST'])
def set_notifier():
    received_json_data = json.loads(flask.request.data)
    app.json_notifier = received_json_data
    return 'OK'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=50000, type=int)
    args = parser.parse_args()
    app.run('127.0.0.1', args.port, threaded=True)
