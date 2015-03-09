import resources


def get_elements():
    multipleChoice = resources.Element("Multiple Choice", "elements/multipleChoice", "../static/images/multiple-choice.png")
    freeResponse = resources.Element("Free Response", "elements/freeResponse", "../static/images/free-response.png")
    trueFalse = resources.Element("True or False", "elements/trueFalse", "../static/images/true-false.png")
    supplementary = resources.Element("Supp. Material", "elements/supplementary", "../static/images/video-button.png")
    textContent = resources.Element("Text Content", "elements/textContent", "../static/images/text-content.jpg")
    elements = [multipleChoice, freeResponse, trueFalse, supplementary, textContent]
    return elements
