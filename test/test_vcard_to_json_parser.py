# Import functions that are going to be tested
from assignment2cache.vcard_to_json_parser import split_on_newlines, split_on_colon


def test_split_on_newlines():
    contact_text = "John Doe\njohndoe@example.com\n123-456-7890"

    result = split_on_newlines(contact_text)

    expected_lines = [
        "John Doe",
        "johndoe@example.com",
        "123-456-7890"
    ]

    assert result == expected_lines


def test_split_on_colon():
    line = "FN:John Doe"

    result = split_on_colon(line)

    expected_result = ["FN", "John Doe"]

    assert result == expected_result
