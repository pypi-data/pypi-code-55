import base64
import email
from apiclient import errors


def GetMimeMessage(service, msg_id):
    """Get a Message and use it to create a MIME Message.

    Args:
        service: Authorized Gmail API service instance.
        msg_id: The ID of the Message required.

    Returns:
        A MIME Message, consisting of data from Message.
    """
    try:
        message = service.users().messages().get(userId="me", id=msg_id,
                                                 format='raw').execute()

        # Decode raw message to bytes
        msg_bytes = base64.urlsafe_b64decode(message['raw'])

        # Transform raw bytes into MIME Message
        msg_mime = email.message_from_bytes(msg_bytes)

        return msg_mime
    except errors.HttpError as error:
        print('An error occurred: %s' % error)


def ListMessagesMatchingQuery(service, query=''):
    """List all Messages of the user's mailbox matching the query.

    Args:
        service: Authorized Gmail API service instance.
        query: String used to filter messages returned.
        Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

    Returns:
        List of Messages that match the criteria of the query. Note that the
        returned list contains Message IDs, you must use get with the
        appropriate ID to get the details of a Message.
    """
    try:
        response = service.users().messages().list(userId="me",
                                                   q=query).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(
                userId="me", q=query,
                pageToken=page_token
            ).execute()
            messages.extend(response['messages'])

        return messages
    except errors.HttpError as error:
        print('An error occurred: %s' % error)


def ListMessagesWithLabels(service, label_ids=[]):
    """List all Messages of the user's mailbox with label_ids applied.

    Args:
        service: Authorized Gmail API service instance.
        label_ids: Only return Messages with these labelIds applied.

    Returns:
        List of Messages that have all required Labels applied. Note that the
        returned list contains Message IDs, you must use get with the
        appropriate id to get the details of a Message.
    """
    try:
        response = service.users().messages().list(
            userId="me",
            labelIds=label_ids
        ).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(
                userId="me",
                labelIds=label_ids,
                pageToken=page_token
            ).execute()
            messages.extend(response['messages'])

        return messages
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
