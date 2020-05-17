from apiclient import errors


def ModifyMessage(service, msg_id, msg_labels):
    """Modify the Labels on the given Message.

    Args:
        service: Authorized Gmail API service instance.
        msg_id: The id of the message required.
        msg_labels: A dictionary indicating the change in labels.

    Returns:
        Modified message, containing updated labelIds, id and threadId.
    """
    try:
        message = service.users().messages().modify(userId="me", id=msg_id,
                                                    body=msg_labels).execute()
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
