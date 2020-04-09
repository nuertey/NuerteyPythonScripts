import psycopg2

try:
    print("Beginning Mr. Nuertey Odzeyem's stock_trading PostgreSQL database test...")
    connect_str = "dbname='stock_trading' user='nuertey' host='localhost' " + \
                  "password='krobo2003'"
    # use our connection values to establish a connection
    conn = psycopg2.connect(connect_str)
    # create a psycopg2 cursor that can execute queries
    cursor = conn.cursor()
    # create a new table with a single column called "name"
    #cursor.execute("""CREATE TABLE tutorials (name char(40));""")
    # run a SELECT statement - no data in there, but we can try it
    cursor.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")
    conn.commit() # <--- makes sure the change is shown in the database
    rows = cursor.fetchall()
    print(rows)
    cursor.execute("""SELECT * from trades""")
    conn.commit() # <--- makes sure the change is shown in the database
    rows = cursor.fetchall()
    print(rows)
    cursor.execute("""SELECT * from quotes""")
    conn.commit() # <--- makes sure the change is shown in the database
    rows = cursor.fetchall()
    print(rows)
    cursor.execute("""SELECT * from orders""")
    conn.commit() # <--- makes sure the change is shown in the database
    rows = cursor.fetchall()
    print(rows)
    cursor.close()
    conn.close()
except Exception as e:
    print("Error! Can't connect to database. Invalid dbname, user or password...")
    print(e)
