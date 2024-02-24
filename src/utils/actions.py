from uuid import uuid4

class Actions:
    def __init__(self, db_handler):
        self.db_handler = db_handler

    def create_uuid(self):
        return uuid4().hex

    def reset_database(self, password, reset_password):
        if password == reset_password:
            self.db_handler.reset_tables()
        else:
            print('Unauthorized access!')
    
    def list_orders(self):
        orders = self.db_handler.get_data('service_orders', ['car_model', 'description'])

        if len(orders) == 0:
            print('No orders at the moment!')
        else:
            for i, order in enumerate(orders):
                print(f'{i + 1}.)\n{order['car_model']}\n{order['description']}')
            
    
    def create_order(self):
        lpn = input('Enter LPN of your vehicle: ')
        model = input('Enter model of you vehicle: ')
        desc = input('Enter description of your order: ')

        uuid = self.create_uuid()

        order = self.db_handler.insert_data('service_orders', {
            'order_id': uuid,
            'lpn': lpn,
            'car_model': model,
            'description': desc
        })

        if order:
            print('You have sucessfully created the following order:')
            print(f'ID: {order['order_id']}\nLPN: {order['lpn']}\nCar Model: {order['car_model']}\nDescription: {order['description']}')
            print(f'Please save your order ID ({order['order_id']}). It is necessary for managing your orders!')

    def show_order(self, id_check_only = False):
        id = input('Enter your order ID: ')
        order = self.db_handler.get_data('service_orders', ['lpn', 'car_model', 'description'], 'order_id', id)
        
        if len(order) == 0:
            if id_check_only:
                return False, id
            print('No order with such ID!')
        else:
            if id_check_only:
                return True, id
            order = order[0]
            print('Your order details:')
            print(f'LPN: {order['lpn']}\nCar Model: {order['car_model']}\nDescription: {order['description']}')
    
    def update_order(self):
        id_is_valid, id = self.show_order(True)
        
        if not id_is_valid:
            print('No order with such ID!')
            return
        
        print('1.) LPN 2.) Car Model 3.) Description')

        try:
            property = int(input(('Select property you would like to update from above: ')))
        except ValueError:
            print('Invalid Entry!')
            return
        
        column = None
        
        for i, _column in enumerate(['lpn', 'car_model', 'description']):
            if i + 1 == property:
                column = _column
                break

        if not column:
            print('Invalid entry!')
            return
        
        new_content = input("Enter new content: ")
        order = self.db_handler.update_data('service_orders', 'order_id', id, column, new_content)

        if order:
            print('Your updated order:')
            print(f'ID: {order['order_id']}\nLPN: {order['lpn']}\nCar Model: {order['car_model']}\nDescription: {order['description']}')
        
    def delete_order(self):
        id_is_valid, id = self.show_order(True)

        if not id_is_valid:
            print('No order with such ID!')
            return
        
        success = self.db_handler.delete_data('service_orders', 'order_id', id)
        
        if success:
            print(f'Your order ({id}) was successfully deleted.')
        else:
            print('Your order was not deleted because of an error.')
