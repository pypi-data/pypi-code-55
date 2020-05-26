from typing import (
    List,
    Generator,
    Type
)
from googleapiclient.discovery import build
from datetime import datetime
import numpy as np
from npyetl.collab.gmail_.gmail.objects import (
    make_message,
    BaseMessage,
    FullMessage,
    Thread,
    Label,
    Draft,
    History
)


class Api:

    def __init__(self,
                 credentials: dict,
                 version: str = 'v1'):
        self._service = build('gmail', version, credentials=credentials)

    def get_labels(self) -> List[Label]:
        """
        Returns all labels in the user's mailbox.
        
        :returns:
            A list of :class:`gmail.objects.Label` instances.
        """
        return self._service.users().labels().list(userId='me').execute()
    
    def get_message(self,
                    id: str,
                    user_id: str = 'me',
                    format: str = 'raw') -> BaseMessage:
        """
        Returns the specified message.
        
        :param id:
            The ID of the message to retrieve.
        :param user_id:
            The user's email address. Special value 'me'.
        :param format:
            The format to return the message in.
        :return:
            A list of :class:`gmail.objects.BaseMessage` instances.
        """
        if format not in ('full','metadata','minimal','raw'):
            raise ValueError("Parameter 'format' must be one of 'full','metadata','minimal','raw'")
        response = self._service.users().messages().get(userId=user_id,id=id,format=format).execute()
        return make_message(**response)

    def get_messages(self,
                     user_id: str = 'me',
                     include_spam_trash: bool = False,
                     label_ids: List[str] = None,
                     max_results: int = None,
                     query: str = None,
                     format: str = 'raw') -> Generator[BaseMessage, None, None]:
        """
        Returns the messages in the user's mailbox.
        
        :param user_id:
            The user's email address. The special value 'me' can be used to indicate the 
            authenticated user, defaults to 'me'
        :param include_spam_trash:
            Include messages from **SPAM** and **TRASH** in the results, defaults to False
        :param label_ids:
            Only return messages with labels that match all of the specified label IDs.
        :param max_results:
            Maximum number of messages to return.
        :param query:
            Only return messages matching the specified query. Supports the same query format
            as the Gmail search box. For example, **"from:someuser@example.com
            rfc822msgid:<somemsgid@example.com> is:unread"**. Parameter cannot be used when
            accessing the api using the gmail.metadata scope.
        :param format:
            The format to return the message in. Accepted values are:
            * "full": Returns the full email message data with body content parsed in the
                      payload field; the raw field is not used. (default)
            * "metadata": Returns only email message ID, labels, and email headers.
            * "minimal": Returns only email message ID and labels; does not return the email
                         headers, body, or payload.
            * "raw": Returns the full email message data with body content in the raw field
                     as a base64url encoded string; the payload field is not returned.
        :return:
            A list of :class:`gmail.objects.BaseMessage` instances.
        """
        list_params = {'userId':user_id, 'includeSpamTrash':include_spam_trash, 'labelIds':label_ids,
                       'maxResults':max_results, 'q':query}
        #
        response = self._service.users().messages().list(**list_params).execute()
        count = response['resultSizeEstimate']
        #
        if 'messages' in response:
            for message in response['messages']:
                yield self.get_message(message['id'], user_id, format)
        #
        while 'nextPageToken' in response and (not max_results or count < max_results):
            page_token = response['nextPageToken']
            response = self._service.users().messages().list(pageToken=page_token,**list_params).execute()
            count += response['resultSizeEstimate']
            if 'messages' in response:
                for message in response['messages']:
                    yield self.get_message(message['id'], user_id, format)

    def get_thread(self,
                   id: str,
                   user_id: str = 'me') -> Thread:
        """
        """
        return Thread.from_dict(self._service.users().threads().get(userId=user_id, id=id).execute())

    def get_threads(self,
                    user_id: str = 'me',
                    query: str = None,
                    max_results: int = np.inf) -> Generator[Thread, None, None]:
        """
        """
        response = self._service.users().threads().list(userId=user_id, q=query,
                                                        maxResults=max_results).execute()
        count = response['resultSizeEstimate']
        #
        if 'threads' in response:
            for thread in response['threads']:
                yield self.get_thread(thread['id'], user_id)
        #
        while 'nextPageToken' in response and count < max_results:
            page_token = response['nextPageToken']
            response = self._service.users().threads().list(userId=user_id, pageToken=page_token,
                                                            q=query, maxResults=max_results).execute()
            count += response['resultSizeEstimate']
            for thread in response['threads']:
                yield self.get_thread(thread['id'], user_id)
