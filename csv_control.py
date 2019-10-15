
#This will all change when moved to sql thats why its a seperate file

import csv

def add_user_to_csv(profile):
	with open('This_will_be_a_database.csv', mode='a') as user_info:
		writer = csv.writer(user_info)
		writer.writerow(profile)
	user_info.close()

def get_info_from_csv(username):
	with open('This_will_be_a_database.csv') as user_info:
		info = csv.reader(user_info, delimiter=',')
		for row in info:
			if row[0] == username:
				return row
	user_info.close()

add_user_to_csv(['sat','Sat','123',{},1000])


# def reader():
# 	df = pd.read_csv('This_will_be_a_database.csv')
# 	return(df)
# def find_person(username):
# 	df = reader()
# 	ind_data = df.loc[df['Username'] == username]
# 	return(ind_data)

