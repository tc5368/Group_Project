
import csv
import pandas as pd

def writer():
	with open('This_will_be_a_database.csv', mode='w') as user_info:
		None

def get_info_from_csv(username):
	with open('This_will_be_a_database.csv') as user_info:
		info = csv.reader(user_info, delimiter=',')
		for row in info:
			if row[0] == username:
				return row

#One approach
# def reader():
# 	df = pd.read_csv('This_will_be_a_database.csv')
# 	return(df)
# def find_person(username):
# 	df = reader()
# 	ind_data = df.loc[df['Username'] == username]
# 	return(ind_data)

