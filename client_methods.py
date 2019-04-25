import requests
import json
import client_shedule
import collections
import datetime


class Client:
    def __init__(self):
        self.client_notifier = None
        self.server_url = ""

    def notify(self):
        print(self.client_notifier.notify())

    def show(self):
        print(self.client_notifier.show())

    def update_product_list(self):
        self.client_notifier.update_product_list()

    def clear_product_list(self):
        self.client_notifier.clear_product_list()

    def update_shedule(self):
        print("Now your shedule is: \n" + self.client_notifier.shedule.show())
        response = input("Do you want to change your shedule/choose new one/go back to menu? '1'/'2'/'3':").strip()
        if response == '1':
            self.client_notifier.change_shedule()
        elif response == '2':
            self.client_notifier.shedule = self._choose_shedule()
        elif response == '3':
            print('You are in the main menu now')
        else:
            print('Incorrect format. You were redirected to the main menu.')

    def _choose_shedule(self):
        # stub
        s1 = client_shedule.RangeShedule({'Milk': 3, 'Egg': 2, 'Meat': 100000}, 9, 11)
        s2 = client_shedule.RangeShedule({'Milk': 3, 'Egg': 2, 'Meat': 100000}, 4, 22)
        s3 = client_shedule.RangeShedule({'Milk': 1, 'Egg': 2, 'Meat': 100000}, 6)
        s4 = client_shedule.RangeShedule({'Milk': 3, 'Egg': 3, 'Meat': 100000}, 9, 11)
        s5 = client_shedule.RangeShedule({'Milk': 4, 'Egg': 2, 'Meat': 100000}, 13, 15)
        s6 = client_shedule.RangeShedule({'Milk': 5, 'Egg': 1, 'Meat': 100000}, 8)
        d1 = client_shedule.DayShedule([s1, s2, s3])
        d2 = client_shedule.DayShedule([s4, s5, s6])

        return client_shedule.Shedule([(datetime.date.today() + datetime.timedelta(days=1), d1),
                                       (datetime.date.today(), d2)])

    def _set_url(self, server_url):
        server_url = server_url[1:-1].strip()
        if server_url[-1] == '/':
            server_url = server_url[:-1]
        self.server_url = server_url
        self._get_notifier()

    def _get_notifier(self):
        response = requests.get(self.server_url + '/get_notifier').json()
        self.client_notifier = get_notifier_from_json(response)

    def _set_notifier(self):
        requests.post(self.server_url + '/set_notifier', data=json.dumps(self.client_notifier.get_json()))

    def _check_connection(self):
        try:
            response = requests.get(self.server_url + '/check').json()
            check = response['check_info']
        except Exception as e:
            print("url incorrect, try again")
            return False
        if check == 'meal_shedule':
            print("connection successful")
            return True
        else:
            print("url incorrect, try again")
            return False


def get_notifier_from_json(response):
    json_shedule = response['shedule']
    product_counter = collections.Counter(response['product_counter'])
    shedule = get_shedule_from_json(json_shedule)
    return client_shedule.Notifier(shedule, product_counter)


def get_shedule_from_json(json_shedule, with_updating_date=False):
    dayshedules = []

    for json_date, json_rangeshedules in json_shedule.items():
        temp = json_date.split("-")
        d = datetime.date(int(temp[0]), int(temp[1]), int(temp[2]))
        dayshedules.append([d, get_dayshedule_from_json(json_rangeshedules)])
    if with_updating_date is True:
        start_date = min(key[0] for key in dayshedules)
        delta = datetime.date.today() - start_date
        if delta > datetime.timedelta(0):
            for key in dayshedules:
                key[0] += delta
    return client_shedule.Shedule(dayshedules)


def get_dayshedule_from_json(json_rangeshedules):
    rangeshedules = []

    for json_rangeshedule in json_rangeshedules:
        rangeshedules.append(client_shedule.RangeShedule(product_counter=json_rangeshedule["product_counter"],
                                                         start_hour=json_rangeshedule["start_hour"],
                                                         end_hour=json_rangeshedule["end_hour"]))
    return client_shedule.DayShedule(rangeshedules)

