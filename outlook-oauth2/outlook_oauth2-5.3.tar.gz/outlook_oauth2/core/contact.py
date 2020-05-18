import json
import requests

from outlook_oauth2.internal.utils import check_response

__all__ = ['Contact']


class Contact(object):
    """ Represents someone sending or receiving an email. Cuts down on the amount of dictionaries floating around that
    each hold the API's syntax and allows for functionality to be added in the future.

    Args:
        email (str): The email of the user
        name (str): The user's name, which is not always provided by the API.

    Keyword Args:
        focused: Whether messages from this sender are always sent to the Focused inbox, or to the Other tab.
            This value is set when retrieving a contact from the API, or after setting it via
            :func:`set_focused() <outlook_oauth2.core.contact.Contact.set_focused>`

    Attributes:
        email: The email of the user
        name: The name of the user
        focused: A boolean indicating whether this contact has an override for their messages to go to the Focused inbox
            or the "Other" inbox. None indicates that the value has not yet been retrieved by the API or set.
    """

    def __init__(self, email, name=None, focused=None):
        # type: (str, str, bool) -> None
        self.email = email
        self.name = name
        self.focused = focused

    def __str__(self):
        if self.name is None:
            return self.email
        return '{} ({})'.format(self.name, self.email)

    def __repr__(self):
        return str(self)

    @classmethod
    def _json_to_contact(cls, json_value):
        contact = json_value.get('EmailAddress', None)
        # The API returns this information in a different format if it's related to Focused inbox overrides
        contact_override = json_value.get('SenderEmailAddress', None)
        if contact is not None:
            email = contact.get('Address', None)
            name = contact.get('Name', None)

            return Contact(email, name)
        # This contains override information
        elif contact_override is not None:
            # Whether they are 'Focused' or 'Other'
            classification = json_value.get('ClassifyAs', 'Other')
            focused = True if classification == 'Focused' else False

            email = contact_override.get('Address', None)
            name = contact_override.get('Name', None)

            return Contact(email, name, focused=focused)
        else:
            return None

    @classmethod
    def _json_to_contacts(cls, json_value):
        # Sometimes, multiple contacts will be provided behind a dictionary with 'value' as the key
        try:
            json_value = json_value['value']
        except TypeError:
            pass
        return [cls._json_to_contact(contact) for contact in json_value]

    def api_representation(self):
        """ Returns the JSON formatting required by Outlook's API for contacts """
        return dict(EmailAddress=dict(Name=self.name, Address=self.email))

    def set_focused(self, mailbox, is_focused):
        # type: (Mailbox, bool) -> bool
        """ Emails from this contact will either always be put in the Focused inbox, or always put in Other, based on
        the value of is_focused.

        Args:
            mailbox (Mailbox): The :class:`Mailbox <outlook_oauth2.core.mailbox.Mailbox>`
                the override should be set for
            is_focused (bool): Whether this contact should be set to Focused, or Other.

        Returns:
            True if the request was successful
        """
        endpoint = 'https://outlook.office.com/api/v2.0/' + mailbox.route + '/InferenceClassification/Overrides'

        if is_focused:
            classification = 'Focused'
        else:
            classification = 'Other'

        data = dict(ClassifyAs=classification, SenderEmailAddress=dict(Address=self.email))

        r = requests.post(endpoint, headers=mailbox._headers, data=json.dumps(data))

        # Will raise an error if necessary, otherwise returns True
        result = check_response(r)

        self.focused = is_focused

        return result
