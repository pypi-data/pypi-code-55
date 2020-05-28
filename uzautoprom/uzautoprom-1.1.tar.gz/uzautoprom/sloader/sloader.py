"""
MIT License

Copyright (c) 2020 LidaRandom

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import os
import time
from pathlib import Path
from typing import Dict, List

import xlrd

from ..abc import Loader
from .browser_tab import BrowserTab


class SLoader(Loader):
    """Built-in Loader, that uses BrowserTab to work with the network.

       Args:
        login - Dealer profile login
        password - Dealer profile password
    """

    def __init__(self, login: str, password: str):
        self._login = str(login)
        self._password = str(password)
        self._browser_tab = BrowserTab("dealer.uzavtosanoat.uz")
        self._dump_file_path = str(
            Path(__file__).parent.absolute() / Path("Заказы.xlsx")
        )

    def contracts(self) -> List[Dict[str, str]]:
        self._dump()
        contracts = self._contracts_from_file()
        self._delete_table()
        return contracts

    def _delete_table(self):
        if os.access(self._dump_file_path, os.R_OK,):
            os.remove(self._dump_file_path)

    def _contracts_from_file(self) -> List[Dict[str, str]]:
        try:
            sheet = xlrd.open_workbook(self._dump_file_path).sheet_by_index(0)
            contracts = []
            for row_index in range(1, sheet.nrows):
                contract = {}
                for field_index, field_name in enumerate(
                    [
                        sheet.cell_value(0, field_index).strip()
                        for field_index in range(sheet.ncols)
                    ]
                ):
                    cell_value = sheet.cell_value(row_index, field_index)
                    if cell_value:
                        contract[field_name] = cell_value
                contracts.append(contract)
            return contracts
        except Exception as exc:
            self._delete_table()
            raise exc

    def _wait_for_table(self):
        while True:
            if os.access(self._dump_file_path, os.R_OK):
                break

    def _dump(self):
        try:
            self._browser_tab.open()
            # Login
            self._browser_tab.set_element_value(
                "//*[@id='login']", self._login
            )
            self._browser_tab.set_element_value(
                "//*[@id='password']", self._password
            )
            self._browser_tab.click(
                "/html/body/div[3]/form/div[3]/button",
                "/html/body/div[3]/div[2]/ul/li[2]/a",
            )
            self._browser_tab.exec_js_file("table_config.js")
            # Open table
            self._browser_tab.click(
                "/html/body/div[3]/div[2]/ul/li[2]/a",
                "/html/body/div[3]/div[2]/ul/li[2]/ul[1]/li/div/div[2]/ul[1]/"
                + "li[1]/a",
            )
            self._browser_tab.click(
                "/html/body/div[3]/div[2]/ul/li[2]/ul[1]/li/div/div[2]/ul[1]/"
                + "li[1]/a",
                "/html/body/div[5]/div/div/b-page-toolbar/div/div[2]/"
                + "b-grid-controller/div/div[1]/div[2]/div[2]/button",
            )
            # Download xlsx file
            self._browser_tab.click(
                "/html/body/div[5]/div/div/b-page-toolbar/div/div[2]/"
                + "b-grid-controller/div/div[1]/div[2]/div[2]/button",
                "/html/body/div[5]/div/div/b-page-toolbar/div/div[2]/"
                + "b-grid-controller/div/div[1]/div[2]/div[2]/ul/li[3]/a",
            )
            self._browser_tab.click(
                "/html/body/div[5]/div/div/b-page-toolbar/div/div[2]/"
                + "b-grid-controller/div/div[1]/div[2]/div[2]/ul/li[3]/a"
            )
            self._wait_for_table()
        except Exception as exc:
            self._delete_table()
            raise exc
        finally:
            self._browser_tab.close()


__all__ = ["SLoader"]
