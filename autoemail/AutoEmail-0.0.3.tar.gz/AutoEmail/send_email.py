'''
Automatatically send emails to given email addresses with given content
'''
# Import library
import smtplib
import pandas as pd
import data_management

# Global variables
email_address = 'yyu.mam2020@london.edu'
password = 'Yxf7315066..!'
DATA = data_management.query()
SUBJECT = 'Request for next Tuesday\'s TMC meeting slides'
BODY = 'This is Yifei from TMC Ops. This is a reminder to upload the team slides for tomorrow\'s TMC Club Meeting.\nBlank slides imply a oral presentation but even some brief notes can help other Exco members who will not be present to keep up with the club agenda.\nDisregard this email if you have already uploaded the slides or you are not the person in your team responsible for updating slides.\nIf you are, please add your slides to the google slide on the drive titled 03/10/20 TMC Club Meeting\nLet me know if you have any question.\nBest,\nYifei'

def initialisation():
	smtp_obj = smtplib.SMTP('smtp-mail.outlook.com', 587)
	print('Hello Message Response:\n' + str(smtp_obj.ehlo()))
	print('Encryption Status:\n' + str(smtp_obj.starttls()))
	print('Login Status:\n' + str(smtp_obj.login(email_address, password)))
	return smtp_obj

def data_import(data = DATA):
	return dict(zip(data.iloc[:,0].tolist(), data.iloc[:,1].tolist()))

def content_generate(contact_list, SUBJECT, BODY):
	first_name_list = []
	content_dict = {}
	subject_dict = {}
	for key in contact_list:
		first_name = key.split()[0]
		content_dict[key] = 'Hello ' + first_name + ',\n' + BODY
		subject_dict[key] = SUBJECT
	return subject_dict, content_dict

def send_email(smtp_obj, subject_dict, content_dict, contact_list):
	response = []
	for key in content_dict:
		response.append(smtp_obj.sendmail(email_address, contact_list[key], 'Subject: ' + subject_dict[key]+ '\n\n' + content_dict[key]))
	print(response)

def disconnection(smtp_obj):
	print('Disconnection Status:\n' + str(smtp_obj.quit()))

def main():
	smtp_obj = initialisation()
	contact_list = data_import()
	subject_dict, content_dict = content_generate(contact_list, SUBJECT, BODY)
	print(contact_list)
	send_email(smtp_obj, subject_dict, content_dict, contact_list)
	disconnection(smtp_obj)






if __name__ == '__main__':
	main()
