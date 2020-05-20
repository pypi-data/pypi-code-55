'''
This package sends customised emails to selected recipients whose information is stored in a local mysql database
'''

import numpy as np
import pandas as pd
import mysql.connector
import smtplib

class AutoEmail:
	def __init__(self, database, query, database_password, subject, body, to_self, self_query, own_email, own_email_password, name_col = 'name', email_col = 'email'):
		self.own_email = own_email
		print('{0:*^80}'.format('Querying MySQL database for recipient information...'))
		self.query_response, self.contact_list = self.send_query(database, query, database_password, to_self, self_query, name_col, email_col)
		print('{0:*^80}'.format('Initialising email server connection...'))
		self.smtp_obj = self.initialisation(self.own_email, own_email_password)
		print('{0:*^80}'.format('Generating email content...'))
		self.subject_dict, self.content_dict = self.generate_content(self.contact_list, subject, body)
		print('{0:*^80}'.format('Preparation complete. Please use .send method to send emails'))

	def send_query(self, database, query, password, to_self, self_query, name_col, email_col):
		cnx = mysql.connector(user = 'root', database = database, password = password)
		if to_self:
			query_response = pd.io.sql.read_sql(self_query, con = cnx, index_col = None)
		else:
			query_response = pd.io.sql.read_sql(query, con = cnx, index_col = None)
		cnx.close()
		contact_list = dict(zip(query_response.loc[:, name_col].tolist(), query_response.loc[:, email_col].tolist()))
		print('{0:*^80}'.format('Here is the list of recipients you selected:'))
		[print(full_name) for full_name in contact_list]
		return query_response, contact_list

	def initialisation(self, own_email, own_email_password):
		smtp_obj = smtplib.SMTP('smtp-mail.outlook.com', 587)
		print('Hello Message Response:\n' + str(smtp_obj.ehlo()))
		print('Encryption Status:\n' + str(smtp_obj.starttls()))
		print('Login Status:\n' + str(smtp_obj.login(own_email, own_email_password)))
		return smtp_obj

	def generate_content(self, contact_list, subject, body):
		first_name_list, content_dict, subject_dict = [], {}, {}
		for full_name in contact_list:
			first_name = full_name.split()[0]
			content_dict[full_name] = 'Dear ' + first_name + ',\n' + body
			subject_dict[full_name] = subject
		return subject_dict, content_dict

	def send(self):
		response = []
		for full_name in self.content_dict:
			response.append(self.smtp_obj.sendmail(self.own_email, self.contact_list[full_name], 'Subject: ' + self.subject_dict[full_name] + '\n\n' + self.content_dict[full_name]))		
		print('{0:*^80}'.format('Here is the response from the email server:'))
		print('{0:*^80}'.format('Note: the number of {} represents the number of successfully delivered emails'))
		print(response)
		self.smtp_obj.quit()
		print('{0:*^80}'.format('Disconnected with the email server'))
