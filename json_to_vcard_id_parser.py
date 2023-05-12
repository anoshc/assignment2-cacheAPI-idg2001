# Denne parseren er inspirert fra IDG2001 Cloud Technologies Lab 3

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
    # The get() adds a default text if the item doesn't exsist.
    vcard.add('birthday').value = data.get('birthday', 'No Birthday')
    vcard.add('version').value = data.get('version', 'No Version')
    vcard.add('name').value = data.get('name', 'No Name')
    vcard.add('fn').value = data.get('first name', 'No First Name')
    vcard.add('org').value = data.get('organisation', 'No Organisation')
    vcard.add('tel').value = data.get('telefon', 'No Telefon')
    vcard.add('email').value = data.get('email', 'No Email')
    address = data.get('address')
    if address:
        street = address.split(';')[2]
        city = address.split(';')[3]
        region = address.split(';')[4]
        code = address.split(';')[5]
        country = address.split(';')[6]
        vcard.add('adr').value = vobject.vcard.Address(
            street=street or '',
            city=city or '',
            region=region or '',
            code=code or '',
            country=country or ''
        )

    # Serialize the vCards to a list of strings in
    vcard_str = vcard.serialize()

    # Combine the vCard strings into a single JSON string
    # Source: https://docs.python.org/3/library/json.html
    vcards_id_json = json.dumps(vcard_str, indent=2)
    
    # Return the output so we can access it in the api
    return {"message" : vcards_id_json}
