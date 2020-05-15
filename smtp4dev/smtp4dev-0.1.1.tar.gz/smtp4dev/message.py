from datetime import datetime


def _clean_dt(dt):
    clean = dt.split(".")[0]
    return f"{clean}+00:00"


class Message:
    """
    Object representation of an email.
    """

    def __init__(
        self,
        pk,
        sender,
        recipients,
        received_date,
        subject,
        attachment_count,
        is_unread,
    ):
        """
        Constructor of an email
        :param pk: the email's primary key (a UUID)
        :param sender: the email's sender
        :param recipients: a tuple of all recipients of the email
        :param received_date: a GMT datetime of the reception of the email
        :param subject: a str, subject of the message
        :param attachment_count: the number of attachments to the email
        :param is_unread: a boolean whether the email was read
        """
        self.pk = pk
        self.sender = sender
        self.recipients = recipients
        self.received_date = received_date
        self.subject = subject
        self.attachment_count = attachment_count
        self.is_unread = is_unread
        self.body = None

    @staticmethod
    def deserialize(msg, html=None):
        """
        Deseriaize a dict of data into a Message
        :param msg: The message as JSON
        :param html: The message's body as HTML (str)
        :returns: Message
        """
        unread = False
        if "attachmentCount" in msg:
            # This is the excerpt from the list
            attachments = msg["attachmentCount"]
            unread = msg["isUnread"]
        else:
            attachments = len([x for x in msg["parts"] if x["isAttachment"]])

        message = Message(
            pk=msg["id"],
            sender=msg["from"],
            recipients=tuple(m.strip() for m in msg["to"].split(",")),
            received_date=datetime.fromisoformat(_clean_dt(msg["receivedDate"])),
            subject=msg["subject"],
            attachment_count=attachments,
            is_unread=unread,
        )
        if html is not None:
            message.set_body(html)
        return message

    def __str__(self):
        rcpts = ", ".join(self.recipients)
        return f"From: {self.sender} To: {rcpts} Subject: {self.subject}"

    def __repr__(self):
        return self.__str__()

    def set_body(self, html):
        """
        Sets the message's body
        :param html: the html body to set
        """
        self.body = html
