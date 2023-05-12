# Denne parseren er inspirert fra IDG2001 Cloud Technologies Lab 3

# * This function finds all collections objects, and parses it from json to vcard
def json_parser():

    import vobject
    import json
    from database import collection

    # Load the JSON object from the MongoDB collection
    data = list(collection.find())

    # Create a vCard object
    vcard = vobject.vCard()

    # Create empty vcard object list
    vcards = []

    # Loop through the items in data
    for item in data:
        # Create a vCard object
        vcard = vobject.vCard()

        # Set the properties from the MongoDB data
        # The get() adds a default text if the item doesn't exsist.
        vcard.add('birthday').value = item.get('birthday', 'No Birthday')
        vcard.add('version').value = item.get('version', 'No Version')
        vcard.add('name').value = item.get('name', 'No Name')
        vcard.add('fn').value = item.get('first name', 'No First Name')
        vcard.add('org').value = item.get('organisation', 'No Organisation')
        vcard.add('tel').value = item.get('telefon', 'No Telefon')
        vcard.add('email').value = item.get('email', 'No Email')
        address = item.get('address')
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

        # Add the vCard to the list
        vcards.append(vcard)

    # Serialize the vCards to a list of strings in
    vcard_str_list = [vcard.serialize() for vcard in vcards]

    # Combine the vCard strings into a single JSON string
    # Source: https://docs.python.org/3/library/json.html
    vcards_json = json.dumps(vcard_str_list, indent=2)

    # Return the output so we can access it in the API
    return {"message" : vcards_json}
