import client_methods


def get_all_functions(_class):
    return [key for key in _class.__dict__ if not key.startswith("private")]


opening_string = "Glad to see you in the 'MEAL SCHEDULE'. We will notify you when to buy and eat products." \
                 "\nAll you need to do is to choose schedule or make your own and update products you have"
instructions_for_use = "In order to use the program you have to choose schedule" \
                       "\n TODO: \n - write 'update_schedule' without params, you will see the following sentence: " \
                       "\n 'Do you want to change your schedule/choose new one/go back to menu? '1'/'2'/'3':' " \
                       "\n - write '2' and follow appeared instructions." \
                       "\nAlso you need to fill list of products with products you have now" \
                       "\n TODO: \n - write 'update_product_list' without params and follow appeared instructions." \
                       "\nAfter these two steps you can completely use all other options."
help_string = "Options:" +\
              "\n 'instructions' -shows instructions for using programm" + \
              "\n 'exit' -ends the programm" + \
              "\n 'show' -shows your schedule if it exists" + \
              "\n 'notify' -notifies you to eat and buy products if you have schedule" + \
              "\n 'update_product_list' -allows you to change product list" + \
              "\n 'clear_product_list' -clears product list" + \
              "\n 'update_schedule' -allows you to change schedule" + \
              "\n all methods don't require arguments"

if __name__ == '__main__':
    check_connection = False
    client = client_methods.Client()

    while not check_connection:
        try:
            server_url = input("To start using client, enter server url in quotes: ")
            client.private_set_url(server_url)
            check_connection = client.private_check_connection()
        except Exception:
            print("url incorrect, try again")

    functions = get_all_functions(client_methods.Client)
    end_of_prog = False
    print(opening_string)
    print(instructions_for_use)
    print(help_string)
    while not end_of_prog:
        input_ = input().split()
        if len(input_) > 0:
            function = input_[0]
            if function in functions:
                args = input_[1:]
                try:
                    getattr(client, function)(*args)
                except Exception as e:
                    print('Your request is incorrect and caused exception: ', e,
                          "Write 'help' to revise request type.", sep='\n')
            elif function == 'help':
                print(help_string)
            elif function == 'instructions':
                print(instructions_for_use)
            elif function == 'exit':
                client.private_set_notifier()
                end_of_prog = True
                print('See you again')
            else:
                print("Function not found. Write 'help' to revise request type.")
