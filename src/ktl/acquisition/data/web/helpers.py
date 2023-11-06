"""
This module contains helper functions that are used in the web acquisition module.
"""

import re


def change_column_names(x: str) -> str:
    """
    Method that is used to change column names to a more readable format.
    :param x: Column name.
    :return: Normalized column name.
    """
    value = re.sub(r'[^\w\s_]', '', x.lower())
    return re.sub(r'[_\s]+', '_', value).strip('_')
