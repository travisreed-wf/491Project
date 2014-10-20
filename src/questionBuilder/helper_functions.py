import resources


def get_elements():
    multipleChoice = resources.Element("Multiple Choice", "elements/multipleChoice")
    freeResponse = resources.Element("Free Response", "elements/freeResponse.html")
    trueFalse = resources.Element("True/False", "elements/trueFalse.html")
    video = resources.Element("Video", "elements/video.html")
    elements = [multipleChoice, freeResponse, trueFalse, video]
    return elements
