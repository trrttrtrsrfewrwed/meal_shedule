import requests
import json
import client_schedule
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
        self.private_set_notifier()

    def clear_product_list(self):
        self.client_notifier.clear_product_list()
        self.private_set_notifier()

    def update_schedule(self):
        print("Now your schedule is: \n" + self.client_notifier.schedule.show())
        response = input("Do you want to change your schedule/choose new one/go back to menu? '1'/'2'/'3':").strip()
        if response == '1':
            self.client_notifier.change_schedule(self.database_client)
        elif response == '2':
            self.client_notifier.schedule = client_schedule.choose('schedule', self.database_client)
        elif response == '3':
            pass
        else:
            print('Incorrect format. You were redirected to the main menu.')
        self.show()
        self.private_set_notifier()
        print('You are in the main menu now')

    def private_set_url(self, server_url):
        server_url = server_url[1:-1].strip()
        if server_url[-1] == '/':
            server_url = server_url[:-1]
        self.server_url = server_url
        self.private_get_notifier()
        self.database_client = DatabaseClient(self.server_url)

    def private_get_notifier(self):
        response = requests.get(self.server_url + '/get_notifier').json()
        self.client_notifier = client_schedule.Notifier.get_notifier_from_json(response)

    def private_set_notifier(self):
        requests.post(self.server_url + '/set_notifier', data=json.dumps(self.client_notifier.get_json()))

    def private_check_connection(self):
        try:
            response = requests.get(self.server_url + '/check').json()
            check = response['check_info']
        except Exception:
            print("url incorrect, try again")
            return False
        if check == 'meal_schedule':
            print("connection successful")
            return True
        else:
            print("url incorrect, try again")
            return False


class DatabaseClient:
    def __init__(self, server_url):
        self.server_url = server_url

    def get_schedule_names(self):
        response = requests.get(self.server_url + '/get_schedule_names').json()
        return response

    def get_day_schedule_names(self):
        response = requests.get(self.server_url + '/get_day_schedule_names').json()
        return response

    def get_meal_names(self):
        response = requests.get(self.server_url + '/get_meal_names').json()
        return response

    def get_schedule(self, name):
        response = requests.get(self.server_url + "/get_schedule?name='{}'".format(name)).json()
        return response

    def get_day_schedule(self, name):
        response = requests.get(self.server_url + "/get_day_schedule?name='{}'".format(name)).json()
        return response

    def get_meal(self, name):
        response = requests.get(self.server_url + "/get_meal?name='{}'".format(name)).json()
        return response









