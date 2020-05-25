import snoozin.gmail.creds as creds
import snoozin.gmail.read_email as read_email
import snoozin.gmail.send_email as send_email

class Snoozin:
    def __init__(self):
        self.service = creds.get_gmail_service()

    def get_matches(self, query):
        return read_email.ListMessagesMatchingQuery(self.service, "me", query)

    def get_sender(self, match):
        # Get message
        message = read_email.GetMimeMessage(self.service, "me", match['id'])

        # Get email address of sender
        sender_full = message["From"]
        sender_address = re.search('<(.*)>', sender_full).group(1)
        return sender_address

    def read_message(self, match):
        """Gets the body of a message that comes before the 'end' delimiter,
        and marks the message as 'read'"""
        # Get message
        message = read_email.GetMimeMessage(self.service, "me", match['id'])

        # Mark message as read
        msgLabel = { 'removeLabelIds': ['UNREAD'] }
        self.service.users().messages().modify(userId="me", id=match['id'], body= msgLabel).execute()

        # Go through message and capture text of message body
        message_body = ""
        for part in message.walk():
            message.get_payload()
            if part.get_content_type() == 'text/plain':
                return part.get_payload()
        return None


    def send(self, to, subject, message_text):
        sender = "snoozinforabruisin@gmail.com"
        message = send_email.CreateMessage(sender, to, subject, message_text)
        send_email.SendMessage(self.service, "me", message)