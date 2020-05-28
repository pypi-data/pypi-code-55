class Formula:
    def __init__(self, callback, target_cell_coords):
        self.formula = callback
        self.target_cell = target_cell_coords

    def get_value(self, target_cell_value):
        args = [target_cell_value]
        return self.formula.__call__(*args)

    def json(self):
        return {"formula": {"name": self.formula.__name__, "target": self.get_target()}}

    def get_target(self):
        return self.target_cell
