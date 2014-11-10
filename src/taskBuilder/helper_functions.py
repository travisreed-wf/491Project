import resources


def get_elements():
    multipleChoice = resources.Element("Multiple Choice", "elements/multipleChoice")
    freeResponse = resources.Element("Free Response", "elements/freeResponse")
    trueFalse = resources.Element("True/False", "elements/trueFalse")
    video = resources.Element("Video", "elements/video")
    elements = [multipleChoice, freeResponse, trueFalse, video]
    return elements
