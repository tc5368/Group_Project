
#This will all change when moved to sql thats why its a seperate file

import csv

def add_user_to_csv(profile):
	with open('This_will_be_a_database.csv', mode='a') as user_info:
		writer = csv.writer(user_info)
		writer.writerow(profile)
	user_info.close()


all_info = []

def update_current_user(profile):
	with open('This_will_be_a_database.csv',mode='r') as user_info:
		info = csv.reader(user_info, delimiter = ',')
		for row in info:
			if row[0] != profile[0]:
				all_info.append(row)
	user_info.close()
	all_info.append(profile)
	with open('This_will_be_a_database.csv', mode='w') as user_info:
		writer = csv.writer(user_info)
		for i in all_info:
			writer.writerow(i)
	user_info.close()

def get_info_from_csv(username):
	with open('This_will_be_a_database.csv') as user_info:
		info = csv.reader(user_info, delimiter = ',')
		for row in info:
			if row[0] == username:
				return row
	user_info.close()

