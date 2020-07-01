import psycopg2
import pandas
import pandas.io.sql

# Here's the shortest code that will do the job:
# 
# from pandas import DataFrame
# df = DataFrame(resoverall.fetchall())
# df.columns = resoverall.keys()
# 
# You can go fancier and parse the types as in Paul's answer.

try:
    print()
    print("Beginning Mr. Nuertey Odzeyem's stock_trading PostgreSQL database test...")
    print()

    connect_str = "dbname='stock_trading' user='nuertey' host='localhost' " + \
                  "password='krobo2003'"

    # use our connection values to establish a connection
    connection = psycopg2.connect(connect_str)

    # create a psycopg2 cursor that can execute queries
    cursor = connection.cursor()
    cursor.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")
    connection.commit() # <--- makes sure the change is shown in the database
    rows = cursor.fetchall()
    print(rows)
    print()

    cursor.execute("""SELECT * FROM information_schema.tables
                    WHERE table_schema = 'public'""")
    for table in cursor.fetchall():
        print(table)

    print()

    trades = pandas.read_sql('select * from trades', connection)
    quotes = pandas.io.sql.read_sql("SELECT * FROM quotes", connection)
    orders = pandas.read_sql('select * from orders', connection)

    print(trades)
    print()

    print(quotes)
    print()

    print(orders)
    print()

except Exception as e:
    print("Error! Can't connect to database. Invalid dbname, user or password...")
    print(e)

finally:
    #closing database connection.
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
        print()

    print("Ending Mr. Nuertey Odzeyem's stock_trading PostgreSQL database test...")
