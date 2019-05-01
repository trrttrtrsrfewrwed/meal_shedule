import requests
import json
import client_shedule
import collections


class Client:
    def __init__(self):
        self.client_notifier = None
        self.server_url = ""
        self.database_client = None

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
            self.client_notifier.change_shedule(self.database_client)
        elif response == '2':
            self.client_notifier.shedule = client_shedule.choose('shedule', self.database_client)
        elif response == '3':
            pass
        else:
            print('Incorrect format. You were redirected to the main menu.')
        self.show()
        print('You are in the main menu now')

    def _set_url(self, server_url):
        server_url = server_url[1:-1].strip()
        if server_url[-1] == '/':
            server_url = server_url[:-1]
        self.server_url = server_url
        self._get_notifier()
        self.database_client = DatabaseClient(self.server_url)

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


class DatabaseClient:
    def __init__(self, server_url):
        self.server_url = server_url

    def get_shedule_names(self):
        response = requests.get(self.server_url + '/get_shedule_names').json()
        return response

    def get_dayshedule_names(self):
        response = requests.get(self.server_url + '/get_dayshedule_names').json()
        return response

    def get_meal_names(self):
        response = requests.get(self.server_url + '/get_meal_names').json()
        return response

    def get_shedule(self, name):
        response = requests.get(self.server_url + "/get_shedule?name='{}'".format(name)).json()
        return response

    def get_dayshedule(self, name):
        response = requests.get(self.server_url + "/get_dayshedule?name='{}'".format(name)).json()
        return response

    def get_meal(self, name):
        response = requests.get(self.server_url + "/get_meal?name='{}'".format(name)).json()
        return response




def get_notifier_from_json(response):
    json_shedule = response['shedule']
    product_counter = collections.Counter(response['product_counter'])
    shedule = client_shedule.get_shedule_from_json(json_shedule)
    return client_shedule.Notifier(shedule, product_counter)






