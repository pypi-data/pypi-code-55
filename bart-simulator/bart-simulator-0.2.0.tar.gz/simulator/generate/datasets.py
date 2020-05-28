"""
Geração dos DataSets de Clientes, Produtos
"""
import random
from faker import Faker
from simulator.generate.utils import custom_uuid, random_sku

import pandas as pd
import numpy as np


fake = Faker("pt-BR")


def customers(number_of_rows: int) -> pd.DataFrame:
    ### Gerando DataSet de Clientes

    columns_customers = ["uuid", "name"]
    df_customers = pd.DataFrame(
        columns=columns_customers,
        data=[[custom_uuid(_id), fake.name()] for _id in np.arange(0, number_of_rows)],
    )
    return df_customers


def products(number_of_rows: int) -> pd.DataFrame:
    ### Gerando DataSet de Produtos

    columns_products = ["sku", "title", "description", "price"]
    df_products = pd.DataFrame(
        columns=columns_products,
        data=[
            [random_sku(_id), fake.sentence(), fake.text(), random.randint(1, 1000)]
            for _id in np.arange(0, number_of_rows)
        ],
    )
    return df_products
