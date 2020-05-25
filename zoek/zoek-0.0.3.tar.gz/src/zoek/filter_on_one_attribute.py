from typing import Callable, Generator, TypeVar

SI = TypeVar('SI', str, int)

get_attribute_from_namespace = getattr


# # function below is equivalent to:
# def filter_on_one_attribute(generator: Generator, attr: str,
#                             condition_checker: Callable[[SI], bool], value: SI) -> Generator:
#     for file in generator:
#         if attr == "name":
#             namespace = file
#         else:
#             namespace = file.stat()
#
#         fileAttribute = get_attribute_from_namespace(namespace, attributeType)
#
#         if condition_checker(fileAttribute, value):
#             yield file
def filter_on_one_attribute(generator: Generator, attributeType: str,
                            condition_checker: Callable[[SI], bool], value: SI) -> Generator:
    """Returns a generator based on filter"""
    return (file for file in generator if
                condition_checker(  # noqa: E128, E127 (to ignore flake8 indent commentary)
                    get_attribute_from_namespace(file if attributeType == "name" else file.stat(), attributeType),
                    value
                )
            )
