from datetime import date, datetime
from collections import Counter, OrderedDict


def choose_menu():
    # stub
    return Counter({'Milk': 5, 'Egg': 1, 'Meat': 100000})


def choose_dayshedule():
    # stub
    s1 = RangeShedule({'Milk': 3, 'Egg': 2, 'Meat': 100000}, 9, 11)
    s2 = RangeShedule({'Milk': 3, 'Egg': 2, 'Meat': 100000}, 4, 22)
    s3 = RangeShedule({'Milk': 1, 'Egg': 2, 'Meat': 100000}, 6)
    return DayShedule([s1, s2, s3])


def list_products(product_counter):
    return ''.join("{} pieces of {}\n".format(value, key) for key, value in product_counter.items()) + "\n"


def update_menu(product_counter, name):
    print("Now in your " + name + ": \n" + list_products(product_counter))
    want_to_change_smth = True
    print("To add product to the " + name + " or increase its amount write '+ [product_name] [amount]'. For example '+ Milk 5'")
    print(
        "To delete product from the " + name + " or decrease its amount write '- [product_name] [amount]'. For example '- Egg 2'")
    print("Use one format of product's name to avoid collisions")
    print("To see your " + name + ", write '?'")
    print("If you are ready, write '.'")
    while want_to_change_smth is True:
        response = input()
        try:
            if response == '?':
                print("Now in your " + name + ": \n" + list_products(product_counter))
            elif response == '.':
                want_to_change_smth = False
            elif response[0] == '+' or response[0] == '-':
                resp = response.split(" ")
                product_name = resp[1]
                amount = int(resp[2])
                if resp[0] == '+':
                    product_counter += Counter({product_name: amount})
                else:
                    product_counter -= Counter({product_name: amount})
            else:
                print("Incorrect format. Write '.' if you want to exit this form")
        except Exception as e:
            print("Incorrect format. Write '.' if you want to exit this form")


def change_rangeshedule(rangeshedule):
    range_process = True
    while range_process is True:
        action = input("Do you want to change start hour/end hour/menu? '1'/'2'/'3':").strip()
        if action == '1':
            print("Write new start hour")
            try:
                start_hour = int(input())
                if 0 < start_hour < rangeshedule.end_hour:
                    rangeshedule.start_hour = start_hour
                else:
                    print("Start hour must be >= 0 and < end hour")
            except Exception:
                print("Incorrect start hour format.")
        elif action == '2':
            print("Write new end hour")
            try:
                end_hour = int(input())
                if rangeshedule.start_hour < end_hour < 25:
                    rangeshedule.end_hour = end_hour
                else:
                    print("Start hour must be <= 24 and > start hour")
            except Exception:
                print("Incorrect end hour format.")
        elif action == '3':
            update_menu(rangeshedule.product_counter, name="menu")
        else:
            print('Incorrect format.')
        range_process_loop = input(
            "Do you want to change another part of range? 'Y'/'n'(not 'Y'):").strip()
        if range_process_loop != 'Y':
            range_process = False


def change_dayshedule(dayshedule):
    day_process = True
    while day_process is True:
        resp = input(
            "Do you want to change/add/delete one of the ranges/go back? '1'/'2'/'3'/'4':").strip()
        if resp == '1' or resp == '2' or resp == '3':
            want_to_change_or_add_or_delete_range = True
            action = {'1': "change", '2': "add", '3': "delete"}
            while want_to_change_or_add_or_delete_range is True:
                range_ = input(
                    "Write range you want to " + action[resp] + " in format [start_hour] [end_hour](23:59 = 24):").strip().split(" ")
                try:
                    if resp == '1':
                        for rangeshedule in dayshedule.rangeshedules:
                            if rangeshedule.start_hour == int(range_[0]) and rangeshedule.end_hour == int(range_[1]):
                                print(rangeshedule.show())
                                change_rangeshedule(rangeshedule)
                                print(rangeshedule.show())
                                break
                        else:
                            print("Incorrect range. Try again")
                    elif resp == '2':
                        for rangeshedule in dayshedule.rangeshedules:
                            if rangeshedule.start_hour == int(range_[0]) and rangeshedule.end_hour == int(range_[1]):
                                print("You already have this range")
                                break
                        else:
                            if 0 <= (int(range_[0])) < (int(range_[1])) <= 24:
                                rangeshedule = RangeShedule({}, start_hour=int(range_[0]), end_hour=int(range_[1]))
                                print(rangeshedule.show())
                                query = input(
                                    "Do you want to fill menu by yourself/choose from existing 'Y'/'n'(not 'Y'):").strip()
                                if query != 'Y':
                                    rangeshedule.product_counter = choose_menu()
                                else:
                                    change_rangeshedule(rangeshedule)
                                dayshedule.rangeshedules.append(rangeshedule)
                                print(rangeshedule.show())
                            else:
                                print("Incorrect range. Try again")
                    elif resp == '3':
                        for rangeshedule in dayshedule.rangeshedules:
                            if rangeshedule.start_hour == int(range_[0]) and rangeshedule.end_hour == int(range_[1]):
                                dayshedule.rangeshedules.remove(rangeshedule)
                                print("deleted")
                                break
                        else:
                            print("You don't have this range")
                except Exception:
                    print("Incorrect range format. Try again")
                range_loop = input("Do you want to " + action[resp] + " another range? 'Y'/'n'(not 'Y'):").strip()
                if range_loop != 'Y':
                    want_to_change_or_add_or_delete_range = False
        elif resp == '4':
            day_process = False
        else:
            print("Incorrect format. If you want to go back, write '4'.")


class Notifier:
    def __init__(self, shedule, product_counter):
        self.shedule = shedule
        self.product_counter = product_counter

    def notify(self):
        if date.today() in self.shedule.shedule:
            return self.shedule.notify(self.product_counter)
        else:
            return "You don't have shedule for today"

    def show(self):
        self.shedule.up_to_date()
        return self.shedule.show()

    def change_shedule(self):
        process = True
        while process is True:
            response = input("Do you want to change/add/delete shedule of one of the days/go back to menu? '1'/'2'/'3'/'4':").strip()
            if response == '1' or response == '2' or response == '3':
                want_to_do_smth = True
                action = {'1': "change", '2': "add", '3': "delete"}
                while want_to_do_smth is True:
                    mm_dd = input("Write the day schedule in which you want to " + action[response] + " in format mm dd: ").strip().split(" ")
                    try:
                        month = int(mm_dd[0])
                        day = int(mm_dd[1])
                        change_date = date(year=date.today().year, month=month, day=day)
                    except Exception:
                        print("Incorrect date type. Try again")
                        continue
                    if response == '1':
                        if change_date in self.shedule.shedule:
                            dayshedule = self.shedule.get_dayshedule(change_date)
                            print(dayshedule.show())
                            change_dayshedule(dayshedule)
                            self.shedule.shedule[change_date] = dayshedule
                            print(dayshedule.show())
                        else:
                            print("No shedule of that day. Try again")
                    elif response == '2':
                        if change_date in self.shedule.shedule:
                            print("You already have shedule of this day")
                        else:
                            dayshedule = DayShedule([])
                            query = input(
                                "Do you want to fill day shedule by yourself/choose from existing 'Y'/'n'(not 'Y'):").strip()
                            if query != 'Y':
                                dayshedule = choose_dayshedule()
                            else:
                                change_dayshedule(dayshedule)
                            self.shedule.shedule[change_date] = dayshedule
                            print(dayshedule.show())
                    elif response == '3':
                        if change_date in self.shedule.shedule:
                            del self.shedule.shedule[change_date]
                            print("deleted")
                        else:
                            print("You don't have this shedule")
                    loop = input(
                        "Do you want to " + action[response] + " shedule of another day? 'Y'/'n'(not 'Y'):").strip()
                    if loop != 'Y':
                        want_to_do_smth = False
            elif response == '4':
                print('You are in the main menu now')
                process = False
            else:
                print("Incorrect format. If you want to go back to menu, write '4'.")

    def clear_product_list(self):
        self.product_counter = Counter()
        print('product list is clear')

    def update_product_list(self):
        update_menu(self.product_counter, name="product list")
        print('You are in the main menu now')

    def get_json(self):
        return {"shedule": self.shedule.get_json(), "product_counter": dict(self.product_counter)}


class Shedule:
    def __init__(self, dayshedules):
        self.shedule = OrderedDict(sorted(dayshedules, key=lambda x: x[0]))

    def up_to_date(self):
        keys_to_pop = []
        for key in self.shedule:
            if key < date.today():
                keys_to_pop.append(key)
        for key in keys_to_pop:
            self.shedule.pop(key)

    def get_dayshedule(self, key):
        return self.shedule[key]

    def notify(self, product_counter):
        return self.shedule[date.today()].notify(product_counter)

    def show(self):
        result = ""
        for key, value in self.shedule.items():
            result += key.strftime("%m.%d") + "\n+++++++++++++++++++++++++++++++++++++++\n\n" \
                      + value.show() + "---------------------------------------\n\n"
        return result

    def get_json(self):
        json = {}
        for key, value in self.shedule.items():
            json[key.strftime("%Y-%m-%d")] = value.get_json()

        return json


class DayShedule:
    def __init__(self, rangeshedules):
        self.rangeshedules = rangeshedules

    def show(self):
        if len(self.rangeshedules) > 0:
            self.rangeshedules.sort(key=lambda x: (x.start_hour, x.end_hour))
            return ''.join(str(i+1) + ")\n" + self.rangeshedules[i].show() + "\n" for i in range(len(self.rangeshedules)))
        else:
            return ''

    def notify(self, product_counter):
        self.rangeshedules.sort(key=lambda x: (x.end_hour, x.start_hour))
        curr_hour = datetime.now().hour
        result = "You need to eat these products: \n"
        must_be_purchased = Counter()
        for rangeshedule in self.rangeshedules:
            if rangeshedule.end_hour > curr_hour:
                must_be_purchased += rangeshedule.product_counter
                result += "from {} to {}:\n".format(str(rangeshedule.start_hour) + " o'clock",
                                                    str(rangeshedule.end_hour) + " o'clock"
                                                    if rangeshedule.end_hour < 24 else "the end of the day")
                result += list_products(rangeshedule.product_counter)
        must_be_purchased -= product_counter
        result += "You are lacking: \n"
        result += list_products(must_be_purchased)
        return result

    def get_json(self):
        json = []

        for rangeshedule in self.rangeshedules:
            json.append({"start_hour": rangeshedule.start_hour,
                         "end_hour": rangeshedule.end_hour,
                         "product_counter": dict(rangeshedule.product_counter)})
        return json


class RangeShedule:
    def __init__(self, product_counter, start_hour=0, end_hour=24):
        self.start_hour = start_hour
        self.end_hour = end_hour
        self.product_counter = Counter(product_counter)
        self.__timespace = 5

    def show(self):
        end_time = ((str(self.end_hour)) + ":00"
                    if self.end_hour < 24 else "23:59")
        start_time = (str(self.start_hour)) + ":00"

        if len(self.product_counter) > 0:
            max_len = max(max(len(key) for key in self.product_counter), self.__timespace)
            max_count_len = max(max(len(str(value)) for value in self.product_counter.values()), self.__timespace)

            return "{:>{}}-{:{}}".format(start_time, max_len, end_time, max_count_len) \
                + "\n" + ''.join(['-']*max_len) + "+" + ''.join(['-']*max_count_len) + "\n" \
                + ''.join(
                "{:^{}}|{:^{}}\n".format(key, max_len, value, max_count_len)
                for key, value in self.product_counter.items())
        else:
            max_len = self.__timespace
            max_count_len = self.__timespace
            return "{:>{}}-{:{}}".format(start_time, max_len, end_time, max_count_len) \
                + "\n" + ''.join(['-']*max_len) + "+" + ''.join(['-']*max_count_len) + "\n"
