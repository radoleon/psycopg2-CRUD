## psycopg2 CRUD operations
### Description
A simple console application, where the user has options to read, create, update, and delete databse records. Each record in the database represents car service order with these properties: ***LPN, car model, description of the problem*** There are also additional options to list all orders and reset database when authorized.

>[!CAUTION]
> I am aware that this project shows several security vulnerabilities, and therefore should never be used in production. The authentification process is simulated for simplicity.

>[!NOTE]
> To run this project on your machine, ensure you have installed python and psycopg2. Afterward, change `src/config/postgres_login.py` file, so it contains information about your own PostgreSQL database and your reset password.

### Technologies
[![My Skills](https://skillicons.dev/icons?i=python,postgres&perline=10)](https://skillicons.dev)
