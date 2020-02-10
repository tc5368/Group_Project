import mysql.connector

cnx = mysql.connector.connect(user='c1769261',password='apmWzUswLy6LvfX',
							  host='csmysql.cs.cf.ac.uk',database='c1769261_Second_Year')

cursor = cnx.cursor()

query = ("SELECT * FROM Customer_Info")
cursor.execute(query)

for i in cursor:
	print(i)

cnx.close()
