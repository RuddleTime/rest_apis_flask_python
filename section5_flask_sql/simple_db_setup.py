import sqlite3  # gives ability to connect and run querries

# initialising a connection
connection = sqlite3.connect('data.db')

# curser -> allows you to connect and start things
cursor = connection.cursor()

# creating 3 column table in db
# schema -> how the data will look
create_table = "CREATE TABLE users (id int, username text, password text)"
cursor.execute(create_table)

user = (1, "Danny", "pa$$word")
insert_query = "INSERT INTO users VALUES (?, ?, ?)"
# Insert single item
cursor.execute(insert_query, user)

users = [
    (2, "Christina", "pa$$word"),
    (3, "Puppy", "pa$$w0rd")
]
# Inserting multiple queries
cursor.executemany(insert_query, users)

# Retrieving data
select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)

# need to say data inserted is to be saved onto disk
connection.commit()




connection.close()
