import psycopg2
import psycopg2.extras
from psycopg2 import sql

class PostgresHandler:
    def __init__(self, host, port, db, user, password):
        self.connection = None
        self.cursor = None
        self.host = host
        self.port = port
        self.db = db
        self.user = user
        self.password = password

    def connect(self):
        self.connection = psycopg2.connect(
            host = self.host,
            port = self.port,
            database = self.db,
            user = self.user,
            password = self.password
        )

        if self.connection:
            self.cursor = self.connection.cursor(cursor_factory = psycopg2.extras.DictCursor)
    
    def close_connection(self):
        self.connection.close()
        self.connection = None
        self.cursor.close()
        self.cursor = None

    def reset_tables(self):
        if self.connection == None:
            self.connect()

        try:
            reset_query = sql.SQL(
                '''
                DROP TABLE IF EXISTS service_orders;
                CREATE TABLE service_orders (
                    order_id VARCHAR(64) NOT NULL,
                    lpn VARCHAR(16) NOT NULL,
                    car_model VARCHAR(64) NOT NULL,
                    description VARCHAR(128) NOT NULL,
                    CONSTRAINT "PK_service_orders" PRIMARY KEY (order_id)
                )
                '''
            )

            self.cursor.execute(reset_query)
            self.connection.commit()

            print('The database was reset.')
        
        except Exception as e:
            print(f'Error "{e}" occured while reseting the data.')

        self.close_connection()

    def insert_data(self, table_name, data_dict):
        inserted = None
        
        if self.connection == None:
            self.connect()
        
        try:
            insert_query = sql.SQL(
                '''
                INSERT INTO {} ({})
                VALUES ({})
                RETURNING *;
                '''
            ).format(
                sql.Identifier(table_name),
                sql.SQL(',').join(map(sql.Identifier, data_dict.keys())),
                sql.SQL(',').join(map(sql.Literal, data_dict.values()))
            )

            self.cursor.execute(insert_query)
            self.connection.commit()

            inserted = self.cursor.fetchone()
        
        except Exception as e:
            print(f'Error "{e}" occured while inserting the data.')

        self.close_connection()
        return inserted

    def get_data(self, table_name, columns, target_column = None, target_value = None):
        retrieved = []
        
        if self.connection == None:
            self.connect()

        try:
            select_query = None
            
            if target_column == None or target_value == None:
                select_query = sql.SQL(
                    '''
                    SELECT {}
                    FROM {};
                    '''
                ).format(
                    sql.SQL(',').join(map(sql.Identifier, columns)),
                    sql.Identifier(table_name)
                )
            
            else: 
                select_query = sql.SQL(
                    '''
                    SELECT {}
                    FROM {}
                    WHERE {} = {};
                    '''
                ).format(
                    sql.SQL(',').join(map(sql.Identifier, columns)),
                    sql.Identifier(table_name),
                    sql.Identifier(target_column),
                    sql.Literal(target_value)
                )
            
            self.cursor.execute(select_query)
            retrieved = self.cursor.fetchall()
        
        except Exception as e:
            print(f'Error "{e}" occured while retrieving the data.')

        self.close_connection()
        return retrieved
    
    def update_data(self, table_name, target_column, target_value, new_column, new_value):
        updated = None
        
        if self.connection == None:
            self.connect()

        try:
            update_query = sql.SQL(
                '''
                UPDATE {}
                SET {} = {}
                WHERE {} = {}
                RETURNING *;
                '''
            ).format(
                sql.Identifier(table_name),
                sql.Identifier(new_column),
                sql.Literal(new_value),
                sql.Identifier(target_column),
                sql.Literal(target_value)
            )

            self.cursor.execute(update_query)
            self.connection.commit()

            updated = self.cursor.fetchone()
        
        except Exception as e:
            print(f'Error "{e}" occured while updating the data.')

        self.close_connection()
        return updated
    
    def delete_data(self, table_name, delete_column, delete_value):
        if self.connection == None:
            self.connect()

        try:
            delete_query = sql.SQL(
                '''
                DELETE FROM {}
                WHERE {} = {};
                '''
            ).format(
                sql.Identifier(table_name),
                sql.Identifier(delete_column),
                sql.Literal(delete_value)
            )

            self.cursor.execute(delete_query)
            self.connection.commit()
            self.close_connection()

            return True
        
        except Exception as e:
            print(f'Error "{e}" occured while deleting the data.')
            self.close_connection()
        
            return False
