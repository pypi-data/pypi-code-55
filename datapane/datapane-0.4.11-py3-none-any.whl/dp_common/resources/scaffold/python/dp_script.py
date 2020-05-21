"""{{ scaffold.name }} script"""
import pandas as pd
import datapane as dp

# TODO - enter your code here...
df = pd.DataFrame.from_dict({"x": [4, 3, 2, 1], "y": [10.5, 20.5, 30.5, 40.5]})

# Create your datapane report components
dp.Report.create(
    dp.Markdown(f"#### **Sample** Markdown block"),
    dp.Table.create(df),
)