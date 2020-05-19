import pandas
import json
import os

class Processed:
    """
    Processed objects are used to hold the results of analysis from Reading Image
    ...

    Attributes
    ----------
    name : str
        User defined name for the file that was analysed
    entities : pandas.DataFrame
        Dataframe containing text entity data
    basicOCR : pandas.DataFrame
        Dataframe containing extracted ocr data
    translation : pandas.DataFrame
        Dataframe containing data from translation of text
    advancedOCR : pandas.DataFrame
        Dataframe containing table data
    """

    def __init__(self, name, json_response):
        """Initialise reading_image.Processed

        Args:
            name (str): User defined name for the file that was analysed
            json_response (dict): server response for analysis
        """

        self._name = name

        entities = json_response.get("entities")
        df_counter = 0
        for dataframe_json in entities.values():
            df_counter += 1
            if df_counter == 1:
                entities_df  = pandas.read_json(dataframe_json, orient='index')
            else:
                entities_df.append(pandas.read_json(dataframe_json, orient='index'))
        self._entities = entities_df

        ocr = json_response.get("basic_ocr")
        basic_ocr_df = None
        translation_ocr_df = None

        page_counter = 0
        if ocr:
            for data in ocr.values():

                # NOTE: Indexes can change so safer to count rather than ocr.items()
                page_counter += 1

                ocr_entities = data.get('entities')
                translation = data.get('translate')

                if ocr_entities:
                    if page_counter == 1:
                        basic_ocr_df  = pandas.read_json(ocr_entities, orient='index')
                    else:
                        basic_ocr_df.append(pandas.read_json(ocr_entities, orient='index'))

                if translation != '':
                    if page_counter == 1:
                        translation_ocr_df  = pandas.read_json(translation, orient='index')
                    else:
                        translation_ocr_df.append(pandas.read_json(translation, orient='index'))

        self._basic_ocr = basic_ocr_df
        self._translation = translation_ocr_df

        advanced_ocr = json_response.get("advanced_ocr")
        advanced_ocr_df = None

        if advanced_ocr:

            for page_number, page_data in advanced_ocr.items():

                data_as_dataframe = pandas.DataFrame(page_data)
                data_as_dataframe["Page"] = page_number

                if int(page_number) == 1:
                    advanced_ocr_df  = data_as_dataframe
                else:
                    advanced_ocr_df = advanced_ocr_df.append(data_as_dataframe)

        self._advanced_ocr = advanced_ocr_df

    @property
    def name(self):
        """User defined name for the file that was analysed
        """
        return self._name

    @property
    def entities(self):
        """Dataframe containing text entity data
        """
        return self._entities

    @property
    def basicOCR(self):
        """Dataframe containing extracted ocr data
        """
        return self._basic_ocr

    @property
    def translation(self):
        """Dataframe containing data from translation of text
        """
        return self._translation

    @property
    def advancedOCR(self):
        """Dataframe containing table data
        """
        return self._advanced_ocr

    @staticmethod
    def fromJson(json_filepath):
        """Create Processed object directly from downloaded json
        """

        with open(json_filepath, 'r') as json_file:
            json_data = json.load(json_file)

        return Processed(
                    name = os.path.basename(json_filepath).split(".")[0],
                    json_response = json_data
                )
