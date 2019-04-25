from collections import OrderedDict

# Весь модуль не несёт практической ценности и будет удален по завершении работы,
# пока помогает мне тестировать взаимодействие клиента и сервера,
# в итоге на сервере и в базе данных будет работа с notifier только в json-формате


class Notifier:
    def __init__(self, shedule, product_dir):
        self.shedule = shedule
        self.product_dir = product_dir

    def get_json(self):
        return {"shedule": self.shedule.get_json(), "product_counter": self.product_dir}


class Shedule:
    def __init__(self, dayshedules):
        self.shedule = OrderedDict(sorted(dayshedules, key=lambda x: x[0]))

    def get_json(self):
        json = {}
        for key, value in self.shedule.items():
            json[key.strftime("%Y-%m-%d")] = value.get_json()

        return json


class DayShedule:
    def __init__(self, rangeshedules=None):
        self.rangeshedules = rangeshedules

    def get_json(self):
        json = []

        for rangeshedule in self.rangeshedules:
            json.append({"start_hour": rangeshedule.start_hour,
                         "end_hour": rangeshedule.end_hour,
                         "product_counter": rangeshedule.product_dir})
        return json


class RangeShedule:
    def __init__(self, product_dir, start_hour=0, end_hour=24):
        self.start_hour = start_hour
        self.end_hour = end_hour
        self.product_dir = product_dir

