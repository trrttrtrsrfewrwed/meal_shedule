
NOTIFIER_TABLE_NAME = 'notifier'
SCHEDULES_TABLE_NAME = 'schedules'
DAY_SCHEDULES_TABLE_NAME = 'day_schedules'
MEALS_TABLE_NAME = 'meals'
TABLE_NAMES = {SCHEDULES_TABLE_NAME, DAY_SCHEDULES_TABLE_NAME, MEALS_TABLE_NAME}
DATABASE_NAME = 'meal_schedule_database'
database_params = dict(user='postgres', host='localhost', password='Timurkiller45')
meals_dict = {"nice_breakfast": {'Milk': 1, 'Egg': 1, 'Buckwheat': 1}, "nice_lunch": {'Meat': 1, 'Rice': 1, 'Tomato': 2, 'Tea': 1},
              "nice_dinner": {'Fish': 1, 'Coffee': 1, 'Cucumber': 2, 'Oyster': 1, 'Potato': 2}}
day_schedules_dict = {"nice_day": [{"start_hour": 8, "end_hour": 9, "product_counter": meals_dict["nice_breakfast"]},
                                 {"start_hour": 13, "end_hour": 14, "product_counter": meals_dict["nice_lunch"]},
                                 {"start_hour": 18, "end_hour": 19, "product_counter": meals_dict["nice_dinner"]}]}
schedules_dict = {"nice_week": {"2019-05-01": day_schedules_dict["nice_day"],
                               "2019-05-02": day_schedules_dict["nice_day"],
                               "2019-05-03": day_schedules_dict["nice_day"],
                               "2019-05-04": day_schedules_dict["nice_day"],
                               "2019-05-05": day_schedules_dict["nice_day"],
                               "2019-05-06": day_schedules_dict["nice_day"],
                               "2019-05-07": day_schedules_dict["nice_day"]}}
dicts = {SCHEDULES_TABLE_NAME: schedules_dict, DAY_SCHEDULES_TABLE_NAME: day_schedules_dict, MEALS_TABLE_NAME: meals_dict}
