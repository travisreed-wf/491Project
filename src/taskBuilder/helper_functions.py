import resources


def get_elements():
    multipleChoice = resources.Element("Multiple Choice", "elements/multipleChoice")
    freeResponse = resources.Element("Free Response", "elements/freeResponse")
    trueFalse = resources.Element("True/False", "elements/trueFalse")
    supplementary = resources.Element("Supp. Material", "elements/supplementary")
    elements = [multipleChoice, freeResponse, trueFalse, supplementary]
    return elements
