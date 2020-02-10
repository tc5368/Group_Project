import mysql.connector

def main():
	
	cnx = mysql.connector.connect(user='c1769261', password='apmWzUswLy6LvfX', host='csmysql.cs.cf.ac.uk', database='c1769261_Second_Year')
	cursor = cnx.cursor()

	query = ("SELECT Date, High, Low, Open ,Close FROM TSLA_HIST")
	cursor.execute(query)

	for (d,h,l,o,c) in cursor:
		print(d,round(o,2),round(c,2))

	cnx.close()
	


if __name__ == '__main__':
	main()