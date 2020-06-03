import sqlite3
from sqlite3 import Error

conn = sqlite3.connect('lfgbot.db')  # You can create a new database by changing the name within the quotes
c = conn.cursor() # The database will be saved in the location where your 'py' file is saved

# Create table - USERS
c.execute('''CREATE TABLE USERS
             ([User_ID] INTEGER PRIMARY KEY,[User_Name] text, [Score] integer)''')                 
conn.commit()

# Note that the syntax to create new tables should only be used once in the code (unless you dropped the table/s at the end of the code). 
# The [generated_id] column is used to set an auto-increment ID for each record
# When creating a new table, you can add both the field names as well as the field formats (e.g., Text)
