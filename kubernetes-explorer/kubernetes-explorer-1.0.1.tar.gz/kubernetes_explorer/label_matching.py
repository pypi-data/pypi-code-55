class LabelMatching():
    def __init__(self):
        self.map = {}

    def add(self, name, labels):
        for key, value in labels.items():

            if key not in self.map:
                self.map[key] = {}

            if value in self.map[key]:
                self.map[key][value].append(name)
            else:
                self.map[key][value] = [name]

    def get(self, selectors):
        if selectors is None:
            return []
        match_labels = selectors if type(
            selectors) is dict else selectors.match_labels

        selected_all = []
        for key, value in match_labels.items():
            if key in self.map and value in self.map[key]:
                selected_all.append(self.map[key][value])
            else:
                return []

        selected = []

        if len(selected_all) > 0:
            selected = selected_all[0]

        for selected_sublist in selected_all:
            selected = list(set(selected) & set(selected_sublist))

        return selected
