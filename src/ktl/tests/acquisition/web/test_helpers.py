import pytest

from ktl.acquisition.data.web import change_column_names


@pytest.mark.parametrize("test_input,expected", [
    ("SimpleColumnName", "simplecolumnname"),
    ("Column Name with 123 & Special Characters", "column_name_with_123_special_characters"),
    ("Column_Name_With_Spaces", "column_name_with_spaces"),
    ("", ""),
    ("!@#$%^&*()", ""),
    ("      ", ""),
    ("______", ""),
    ("normalized_column_name", "normalized_column_name"),
])
def test_change_column_names(test_input: str, expected: str) -> None:
    assert change_column_names(test_input) == expected
