# -*- coding: utf-8 -*-
""" content container class module.

"""

import json
import os


class Container(object):
    SELECTOR_DELIMITER = "."
    LOG_FILENAME = "content.log"

    def __init__(self, content_path: str, default_language: str):
        self.path = content_path
        self.default_language = default_language
        self.current_page_data = None
        self.current_page_name = None
        self.validate_directory()

    def __getitem__(self, selector: str):
        return self.item(selector)

    def set_current_page(self, page_name: str):
        self.current_page_name = page_name
        self.current_page_data = self.load_page_data(page_name)

    def item(self, selector):
        if self.current_page_data is None:
            raise NotImplementedError("A page has not been set for this item.")
        page_name, item_name, language = self.decompose_selector("item", selector) \
            if isinstance(selector, str) else tuple(selector)
        if page_name != self.current_page_name:
            self.set_current_page(page_name)
        return self.current_page_data[item_name][language]

    def decompose_selector(self, entity_type: str, selector: str) -> tuple:
        if entity_type == "item":
            page_name = item_name = language = None
            selector_parts = selector.split(".", maxsplit=2)
            if len(selector_parts) == 1:
                page_name = self.current_page_name
                item_name = selector_parts[0]
                language = self.default_language
            elif len(selector_parts) == 2:
                page_name = self.current_page_name
                item_name, language = tuple(selector_parts)
            elif len(selector_parts) == 3:
                page_name, item_name, language = tuple(selector_parts)
            return page_name, item_name, language
        elif entity_type == "page":
            return selector,
        else:
            raise TypeError("Invalid entity type '{}'.".format(entity_type))

    def load_page_data(self, page_name: str) -> dict:
        return json.load(open(self.get_page_file_path(page_name), "r"))

    def save_page_data(self, page_data: dict, page_name: str):
        json.dump(page_data, open(self.get_page_file_path(page_name), "w+"))

    def get_page_file_path(self, page_name: str) -> str:
        return os.path.join(self.path, "{}.json".format(page_name))

    def validate_directory(self):
        if not os.path.isdir(self.path):
            os.makedirs(self.path)
        # TODO: add log file
