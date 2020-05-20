'''
This programme fetches and filters emails from Yifei's outlook mailbox
'''
import imapclient
import imaplib
import pprint
import pyzmail # import libraries
imaplib._MAXLINE = 10000000


'''
GLobal Variables
'''
IMAP_SERVER = 'imap-mail.outlook.com'
OWN_EMAIL = 'yyu.mam2020@london.edu' # Configure the programme
PASSWORD = 'Yxf7315066..!'
SEARCH_KEYWORDS = ['SUBJECT', "EUROUT 2019"]

'''
Body
'''
def initialisation(folder = 'INBOX', own_email = OWN_EMAIL, password = PASSWORD, imap_server = IMAP_SERVER):
	'''Initialise IMAP client object'''
	imap_obj = imapclient.IMAPClient(imap_server, ssl = True)
	print('Authentication Status:\n' + str(imap_obj.login(own_email, password)))
	imap_obj.select_folder(folder, readonly = True)
	return imap_obj

def search(imap_obj, search_keywords):
	'''Search the folder with a specific string'''
	UIDS = imap_obj.search(search_keywords)
	raw_messages = imap_obj.fetch(UIDS, ['BODY[]'])
	messages = []
	for key in UIDS:
		messages.append(pyzmail.PyzMessage.factory(raw_messages[key][b'BODY[]']))
	addresses = [messages[index].get_addresses('from') for index in range(len(messages))]
	for message in messages:
		if message.text_part != None:
			print(message.text_part.get_payload().decode(message.text_part.charset))
	#body = [messages[index].text_part.get_payload().decode(messages[index].text_part.charset) for index in range(len(messages))]

def main():
	imap_obj = initialisation()
	search(imap_obj, SEARCH_KEYWORDS)














if __name__ == '__main__':
	main()
