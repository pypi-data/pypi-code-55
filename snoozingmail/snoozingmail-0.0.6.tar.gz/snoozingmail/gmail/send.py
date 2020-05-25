import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import os

from apiclient import errors


def SendMessage(service, message):
    """Send an email message.

    Args:
        service: Authorized Gmail API service instance.
        message: Message to be sent.

    Returns:
        Sent Message.
    """
    try:
        message = service.users().messages().send(
            userId="me",
            body=message
        ).execute()
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)


def CreateMessage(to, subject, message_body, html=False,
                  attachments=[]):
    """Create a message for an email.

    Args:
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_body: The content of the email message.
        html: Whether the mesage_body is formatted as html
        attachments: List of file paths to files that should be
                     attached to the email

    Returns:
        An object containing a base64 encoded email object.
    """
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = "me"
    message['subject'] = subject

    # Add message body, using html formatting if it was used
    if html:
        msg = MIMEText(message_body, 'html')
    else:
        msg = MIMEText(message_body)
    message.attach(msg)

    # Add attacments if they exist
    if len(attachments):
        for attachment in attachments:
            content_type, encoding = mimetypes.guess_type(attachment)

            if content_type is None or encoding is not None:
                content_type = 'application/octet-stream'
                main_type, sub_type = content_type.split('/', 1)

            if main_type == 'text':
                fp = open(attachment, 'rb')
                msg = MIMEText(fp.read(), _subtype=sub_type)
                fp.close()
            elif main_type == 'image':
                fp = open(attachment, 'rb')
                msg = MIMEImage(fp.read(), _subtype=sub_type)
                fp.close()
            elif main_type == 'audio':
                fp = open(attachment, 'rb')
                msg = MIMEAudio(fp.read(), _subtype=sub_type)
                fp.close()
            else:
                fp = open(attachment, 'rb')
                msg = MIMEBase(main_type, sub_type)
                msg.set_payload(fp.read())
                fp.close()

            msg.add_header('Content-Disposition', 'attachment',
                           filename=os.path.basename(attachment))
            message.attach(msg)

    b64_bytes = base64.urlsafe_b64encode(message.as_bytes())
    b64_string = b64_bytes.decode()
    return {'raw': b64_string}
