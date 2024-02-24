from src.config.postgres_login import postgres_login_data, reset_password
from src.utils.postres_handler import PostgresHandler
from src.utils.actions import Actions

def print_menu():
    print(
        '''
        Welcome in car service, to work with the data, pick one of theese commands:
        [1] List all orders
        [2] Create new order
        [3] Show your order
        [4] Update your order
        [5] Delete your order
        [6] Reset database
        [7] Terminate the program
        '''
    )

pg_handler = PostgresHandler(*postgres_login_data.values())
actions = Actions(pg_handler)

if __name__ == '__main__':
    print_menu()

    while True:

        command = input('Select a command from the menu above: ')

        if not command.isnumeric() or int(command) < 1 or int(command) > 7:
            print('Incorrect entry!\n')
            continue
        
        command = int(command)

        if command == 1:
            actions.list_orders()
        if command == 2:
            actions.create_order()
        if command == 3:
            actions.show_order()
        if command == 4:
            actions.update_order()          
        if command == 5:
            actions.delete_order()

        if command == 6:
            password = input('Input password: ')
            actions.reset_database(password, reset_password)

        if command == 7:
            print('Program was terminated.')
            break

        print()
