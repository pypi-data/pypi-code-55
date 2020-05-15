import ipywidgets as widgets
from IPython.display import display


class Checkbox:

    """
    descriptions = ["aa", "ba", "c", "h", "u", "p"]

    choices = Checkbox(descriptions)

    choices.values
    """

    def __init__(self, attributes):
        """
        selects from a list of attributes
        :param attributes:
        """
        options_dict = {
            description: widgets.Checkbox(description=description, value=False)
            for description in attributes
        }
        options = [options_dict[description] for description in attributes]
        self.options_widget = widgets.VBox(options, layout=widgets.Layout(overflow='scroll'))
        display(self.options_widget)

    @property
    def values(self):
        return [x.description for x in self.options_widget.children if x.value]


