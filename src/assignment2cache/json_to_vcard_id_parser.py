# Denne parseren er inspirert fra IDG2001 Cloud Technologies Lab 3
def get_address_fields(address):
    return address.split(';')[2:]


def set_address_fields(address_fields):
    return address_fields + ['']*(5 - len(address_fields))


# * This function finds a collection object based on id, and parses it from json to vcard
def json_id_parser(id):

    import vobject
    import json
    from database import collection
    from bson.objectid import ObjectId

    # Load the JSON object from the MongoDB colelction
    data = collection.find_one({"_id": ObjectId(id)})  
    
    # Create a vCard object
    vcard = vobject.vCard()
    
    # Set the properties from the MongoDB data
    vcard_properties = {
        'birthday': 'birthday',
        'version': 'version',
        'name': 'name',
        'fn': 'first name',
        'org': 'organisation',
        'tel': 'telefon',
        'email': 'email'
    }

    # The get() adds a default text if the item doesn't exist.
    for vcard_property, mongo_property in vcard_properties.items():
        value = data.get(mongo_property, f'No {vcard_property.capitalize()}')
        vcard.add(vcard_property).value = value

    address = data.get('address')
    if address:
        address_fields = get_address_fields(address)
        street, city, region, code, country = set_address_fields(address_fields)
        vcard.add('adr').value = vobject.vcard.Address(
            street=street, city=city, region=region, code=code, country=country
        )

    # Serialize the vCards to a list of strings in
    vcard_str = vcard.serialize()

    # Combine the vCard strings into a single JSON string
    # Source: https://docs.python.org/3/library/json.html
    vcards_id_json = json.dumps(vcard_str, indent=2)

    # Return the output so we can access it in the api
    return {"message" : vcards_id_json}
