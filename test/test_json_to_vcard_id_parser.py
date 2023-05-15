import json
import vobject

# Import functions that are going to be tested
from assignment2cache.json_to_vcard_id_parser import get_address_fields, set_address_fields


# Testing the function 'get_address_fields' and check if it splits on the semicolons. 
def test_get_address_fields():
    address = ";;One Microsoft Way;Redmond;WA;98052-6399;USA"
    
    result = get_address_fields(address)

    # Assert the correctness of the serialization
    expected_result = ["One Microsoft Way", "Redmond", "WA", "98052-6399", "USA"]
    assert result == expected_result


# Testing the function 'set_address_fields' includes a empty string if there are fewer than 5 items.
def test_set_address_fields():
    address_fields = ["One Microsoft Way", "Redmond"]

    # Call the function
    result = set_address_fields(address_fields)

    # Define the expected result
    expected_result = ["One Microsoft Way", "Redmond", "", "", ""]


    # Assert that the Address object is created correctly
    assert result == expected_result