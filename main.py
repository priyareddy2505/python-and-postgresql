# importing the psycopg2 library
import psycopg2
import psycopg2.extras

# variables to store the database connection details
hostname = 'localhost'
database = 'cs623_pythonproject'
username = 'postgres'
password = 'Priya@5284'
port_id = 5432

# database connection object
connection = None

# script to drop the tables before recreating them
dropTableProduct = 'DROP TABLE IF EXISTS Product'
dropTableDepot = 'DROP TABLE IF EXISTS Depot'
dropTableStock = 'DROP TABLE IF EXISTS Stock'

# script to create a table if only it does not exist
createProductTable = ''' CREATE TABLE IF NOT EXISTS Product(
                    prodid     varchar(10) PRIMARY KEY NOT NULL,
                    pname      varchar(40) NOT NULL,
                    price      int NOT NULL) '''

# script to create a table if only it does not exist
createDepotTable = ''' CREATE TABLE IF NOT EXISTS Depot(
                    depid      varchar(10) PRIMARY KEY NOT NULL,
                    addr       varchar(40) NOT NULL,
                    volume     int NOT NULL) '''

# script to create a table if only it does not exist
createStockTable = ''' CREATE TABLE IF NOT EXISTS Stock(
                    prodid      varchar(10) NOT NULL,
                    depid       varchar(10) NOT NULL,
                    quantity    int NOT NULL) '''

# script to insert data
insertProductData = 'INSERT INTO Product (prodid, pname, price) VALUES (%s, %s, %s)'
productValues = [('p1', 'tape', 2.5), ('p2', 'tv', 250), ('p3', 'vcr', 80)]

insertDepotData = 'INSERT INTO Depot (depid, addr, volume) VALUES (%s, %s, %s)'
depotValues = [('d1', 'New York', 9000), ('d2', 'Syracuse', 6000), ('d4', 'New York', 2000)]

insertStockData = 'INSERT INTO Stock (prodid, depid, quantity) VALUES (%s, %s, %s)'
stockValues = [('p1', 'd1', 1000), ('p1', 'd2', -100), ('p1', 'd4', 1200), ('p3', 'd1', 3000), ('p3', 'd4', 2000),
               ('p2', 'd4', 1500), ('p2', 'd1', -400), ('p2', 'd2', 2000)]

# script to add specified depot (d100,Chicago,100)
addDepot = 'INSERT INTO Depot (depid, addr, volume) VALUES (%s, %s, %s)'
depotValue = ('d100', 'Chicago', 100)

# script to add specified stock (p100,d2,50)
addStock = 'INSERT INTO Stock (prodid, depid, quantity) VALUES (%s, %s, %s)'
stockValue = ('p1', 'd100', 100)

# script to fetch all the data
fetchAllData_Depot = 'SELECT * FROM Depot'
fetchAllData_Stock = 'SELECT * FROM Stock'


# functon to create product table (isolated from depot and stock table creating functions)
def createProductTableFunction(cursor):
    cursor.execute(dropTableProduct)
    cursor.execute(createProductTable)


# functon to create depot table (isolated from product and stock table creating functions)
def createDepotTableFunction(cursor):
    cursor.execute(dropTableDepot)
    cursor.execute(createDepotTable)


# functon to create depot table (isolated from depot and product table creating functions)
def createStockTableFunction(cursor):
    cursor.execute(dropTableStock)
    cursor.execute(createStockTable)


# function to add data to product table (isolated from depot and stock insert functions)
def insertProductDataFunction(insertProductData, productValues):
    for record in productValues:
        cursor.execute(insertProductData, record)


# function to add data to product table (isolated from product and stock insert functions)
def insertDepotDataFunction(insertDepotData, depotValues):
    for record in depotValues:
        cursor.execute(insertDepotData, record)


# function to add data to product table (isolated from depot and product insert functions)
def insertStockDataFunction(insertStockData, stockValues):
    for record in stockValues:
        cursor.execute(insertStockData, record)


# function to add the specified depot (d100,Chicago,100)
def addSpecifiedDepot():
    cursor.execute(addDepot, depotValue)


# function to add specified stock (p100,d2,50)
def addSpecifiedStock():
    cursor.execute(addStock, stockValue)


# main function
if __name__ == '__main__':

    # try catch block to catch any error that might occur in during connection and communication with the database
    try:
        # connecting to the database (Using 'with' clause)
        with psycopg2.connect(
                host=hostname, database=database, user=username, password=password, port=port_id
        ) as connection:

            # creating a database cursor to help us in performing the database operations
            with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:

                # create the Product,Depot and Stock tables
                createProductTableFunction(cursor)
                createDepotTableFunction(cursor)
                createStockTableFunction(cursor)

                # add data to the tables
                insertProductDataFunction(insertProductData, productValues)
                insertDepotDataFunction(insertDepotData, depotValues)
                insertStockDataFunction(insertStockData, stockValues)

                # results before adding the specified depot and stock
                cursor.execute(fetchAllData_Depot)
                print("*********Depot (Before)********")
                for record1 in cursor.fetchall():
                    print(record1['depid'], record1['addr'], record1['volume'])
                cursor.execute(fetchAllData_Stock)
                print()
                print("*********Stock (Before)********")
                for record2 in cursor.fetchall():
                    print(record2['prodid'], record2['depid'], record2['quantity'])

                # add the specified depot (d100,Chicago,100)
                addSpecifiedDepot()
                # add the specified stock (p100,d2,50)
                addSpecifiedStock()

                # results after adding the specified depot and stock 
                cursor.execute(fetchAllData_Depot)
                print()
                print("*********Depot (After)********")
                for record1 in cursor.fetchall():
                    print(record1['depid'], record1['addr'], record1['volume'])
                cursor.execute(fetchAllData_Stock)
                print()
                print("*********Stock (After)********")
                for record2 in cursor.fetchall():
                    print(record2['prodid'], record2['depid'], record2['quantity'])

    except Exception as error:
        # print the error that has occurred
        print(error)
    finally:
        if connection is not None:
            # close the database connection
            connection.close()
