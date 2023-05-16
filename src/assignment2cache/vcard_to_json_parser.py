# Denne parseren er inspirert fra IDG2001 Cloud Technologies Lab 3
def split_on_newlines(lines):

    return lines.split('\n')


def split_on_colon(line):

    return line.split(':')

# * This function takes the uploaded file as input, and parses it from vcard to json

    # Set the file as a parameter


def vcard_parser(file):

    import json

    # Set the name of the files
    INPUT_NAME = file
    OUTPUT_NAME = 'data.json'

    # Open the input file
    with open(INPUT_NAME, 'r') as f:
        text = f.read()

    # Split the texts from start to end
    contact_texts = text.split('END:VCARD\nBEGIN:VCARD')

    contact_texts[0] = contact_texts[0].replace('BEGIN:VCARD\n', '')
    contact_texts[-1] = contact_texts[-1].replace('END:VCARD\n', '')

    # Fixing keys
    def fix_key(key):
        key_main = key.split(';')[0]
        return {
            'BDAY': 'birthday',
            'VERSION': 'version',
            'N': 'name',
            'FN': 'first name',
            'ORG': 'organisation',
            'ADR': 'address',
            'TEL': 'telefon',
            'EMAIL': 'email'
        }.get(key_main, key)

    # Put the contacts inside a contact object
    contacts = []
    for contact_text in contact_texts:

        contact = {}
        lines = split_on_newlines(contact_text)

        for line in lines:
            if len(line) < 1:
                continue

            key, *value = split_on_colon(line)
            value = ':'.join(value)

            key = fix_key(key)

            contact[key] = value
        contacts.append(contact)

    json_text = json.dumps(contacts, indent=2)

    # Put the result inside file
    # This step is optional, but if you want a better view of the output then we added a file here as well.
    with open(OUTPUT_NAME, 'w') as f:
        f.write(json_text)
