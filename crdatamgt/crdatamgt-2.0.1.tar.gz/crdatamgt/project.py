import pandas as pd
import crdatamgt.topic as topic
from crdatamgt.helpers import (
    topic_directories,
    workbook_load_file,
    workbook_save,
    rename_dictionary,
)
import datetime
import re
from crdatamgt.formulations import (
    formulations_for_log_file,
    update_formulation_table,
)


def project_load_from_workbooks(workbooks, **kwargs):
    result_wb = workbooks
    project_sheets = []
    formulation_sheets = []
    formatting = {}
    if kwargs.get("OUTPUT DIRECTORY"):
        output_path = kwargs.get("OUTPUT DIRECTORY")
    else:
        import os

        output_path = os.path.split(kwargs.get("RESULTS DIRECTORY"))[0]
    for result in result_wb:
        result_data = topic.read_topic(result, kwargs.get("FORMULATION DIRECTORY"))
        formulation_data = result_data.pop("Formulation", pd.DataFrame())
        if not formulation_data.empty:
            formulation_data.loc[:, "Topic ID"] = (
                result_data.get("Summary").get("Topic ID").values
            )
            formulation_sheets.append(formulation_data)
        else:
            print(
                f"No Formulation data or Formulation tab misspelled {result_data.get('Summary').get('Topic ID').values}"
            )
        if len(result_data.get("Results").columns) > 2:
            exploded_results = result_data.pop("Results", pd.DataFrame())
            normal_sheets = pd.concat(result_data.values(), axis=1, sort=False)
            exploded_results[normal_sheets.columns] = normal_sheets
            normal_sheets = exploded_results.fillna(method="ffill")
        else:
            normal_sheets = pd.concat(result_data.values(), axis=1, sort=False)
        project_sheets.append(normal_sheets)

    compiled = (
        pd.concat(project_sheets[::-1], sort=False)
        .set_index("Topic ID")
        .sort_index()
        .reset_index()
        .drop(columns=["Test"], errors="ignore")
    )

    cleaned_formulations = formulation_work(formulation_sheets)
    update_formulation_table(
        cleaned_formulations.drop(columns="topic id", errors="ignore"),
        kwargs.get("FORMULATION DIRECTORY"),
    )
    updated_formulations = formulations_for_log_file(cleaned_formulations)
    compiled = compiled.merge(updated_formulations, how="outer")

    formatting["header"] = {
        "bold": True,
        "text_wrap": False,
        "valign": "top",
        "fg_color": "#D7E4BC",
        "border": 1,
        "font_size": 16,
    }

    # Write the column headers with the defined format.

    project_name = re.search(r"\\(Project .*)\\", kwargs.get("RESULTS DIRECTORY"))[1]
    dt = datetime.datetime.now().strftime("%d_%m_%Y")
    excel_name = f"{project_name}_{dt}"
    workbook_save(excel_name, output_path, compiled, project_name, **formatting)
    workbook_save(project_name, output_path, compiled, project_name, **formatting)


def project_load(**kwargs):
    if kwargs.get("TOPIC STRUCTURED"):
        topic_name, topic_path = topic_directories(kwargs.get("PROJECT DIRECTORY"))
        workbooks = [topic.load_topic(t_path) for t_path in topic_path]
        project_load_from_workbooks(workbooks, **kwargs)
    else:  # if kwargs.get('RESULT STRUCTURED'):
        workbooks = workbook_load_file(kwargs.get("RESULTS DIRECTORY"))
        project_load_from_workbooks(workbooks, **kwargs)


def formulation_work(data_frame_list):
    cleaned = [sheet.dropna(how="all") for sheet in data_frame_list]
    cleaned = list(
        map(
            lambda sheet: sheet.rename(str.lower, axis="columns").rename(
                columns=rename_dictionary()
            ),
            cleaned,
        )
    )
    clean_frame = pd.concat(cleaned)
    clean_frame.drop_duplicates(inplace=True)
    clean_frame.reset_index(inplace=True)
    clean_frame.drop(
        columns=["index", "units", "formulation"], errors="ignore", inplace=True
    )
    clean_frame.dropna(how="all", inplace=True)
    return clean_frame
