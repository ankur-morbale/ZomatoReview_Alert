import MySQLdb

import smtplib


input_text = '"review": {'+'"rating": 2,'+'"review_text": "poor Nutrition quotient - 3 / 5 Ambience - 3.5 / 5 Taste - 4.5 / 5 Value for money - 4 / 5 Service - 3.5 / 5  I have been wanting to visit this place for quite sometime, and it surely dint disappoint. I relished the food here much more than at punjab grill (owned by the same owner). right from the maska buns to the almond kebabs to the mushroom kofta and assorted breads, each dish was unique and had a distinct flavour to it. we landed us eating the breads and the mains separately as individual dishes...",'+'"id": "30179137",'+'"rating_color": "5BA829",'+'"review_time_friendly": "yesterday",'+'"rating_text": "Great!",'+'"timestamp": 1493313400,'+'"likes": 1,'+'"user": {'+'"name": "Dhvani Shah",'+'"zomato_handle": "Itsdhvanishah",'+'"foodie_level": "Big Foodie",'+'"foodie_level_num": 4,'+'"foodie_color": "ffae4f",'+'"profile_url": "https://www.zomato.com/Itsdhvanishah?utm_source=api_basic_user&utm_medium=api&utm_campaign=v2.1",'+'"profile_image": "https://b.zmtcdn.com/data/user_profile_pictures/e44/b9df205022407e7532ae9deb56c48e44.jpg?fit=around%7C100%3A100&crop=100%3A100%3B%2A%2C%2A",'+'"profile_deeplink": "zomato://u/115517"'+"}"

def sendalert(content):
	mail=smtplib.SMTP('smtp.gmail.com',587)
    
	mail.ehlo()
	mail.starttls()
	mail.login('ab127765@gmail.com','terry2694')
    
	mail.sendmail('ab127765@gmail.com','ankurmorbale26@gmail.com',content)
	mail.close()

def readreview(user_review):
	tag_rating = '"rating":'
	length_of_tag_rating=10
	
	tag_rev_text = '"review_text": '
	length_of_tag_rev_text=15
	
	tag_id = '"id": '
	length_of_tag_id=6

	tag_name = '"name": '
	length_of_tag_name=8

	sentiment=['bad','poor','disappoint','disappoints','worst','tasteless','not value for money','bland','disappointed','sad','not worth','slow','not fresh']

	if tag_rating in user_review:
		rating= user_review[user_review.index(tag_rating)+length_of_tag_rating]
		print rating

	if tag_rev_text in user_review:
		index_of_review=user_review.index(tag_rev_text)+length_of_tag_rev_text
		
		temp_string=user_review[index_of_review:]
		
		index_of_comma =temp_string.index('","')

		review_text = temp_string[1:index_of_comma]

		review_text_seperated = review_text.split();

	if tag_id in user_review:
		index_of_id= user_review.index(tag_id)+length_of_tag_id

		temp_id=user_review[index_of_id:]
		
		index_of_comma=temp_id.index('","')

		user_id = temp_id[1:index_of_comma]
		

	if tag_name in user_review:
		index_of_name= user_review.index(tag_name)+length_of_tag_name

		temp_name=user_review[index_of_name:]

		index_of_comma=temp_name.index('","')

		user_name = temp_name[1:index_of_comma]
		




	db = MySQLdb.connect(host="localhost",    # host, localhost
                     user="root",        	  # username
                     passwd="ankur",  		  # password
                     db="zomato")        	  # name of the data base
	
	cur = db.cursor() # opening cursor

	
	insert_stmt = ("INSERT INTO zomato_review_data (user_id,rating, review_text,username)"
					"VALUES (%s, %s,%s,%s)")

	if int(rating) < 2:
		data=(user_id,str(rating),review_text,user_name)
		cur.execute(insert_stmt,data)
 		# inserting data into MYSQL db
		sendalert(review_text) # sending the email alert



	if(int(rating) == 2):
		for word in review_text_seperated:
			if word in sentiment:
				data=(user_id,str(rating),review_text,user_name)
				cur.execute(insert_stmt,data) 
				 # inserting data into MYSQL db
				sendalert(review_text) # sending the email alert 

	if(int(rating) > 2):
		print "Positve rating"

	# for row in cur.fetchall():
	# 	print row[0] + row[1] + row[2] + row[3]


	db.commit() # since it is an insert we need to commit the data
	db.close() # closing connection with db

  
readreview(input_text)




