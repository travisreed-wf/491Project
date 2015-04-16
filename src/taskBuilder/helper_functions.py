import resources


def get_elements():
    multipleChoice = resources.Element("Multiple Choice", "tasks/elements/multipleChoice", "../static/images/multiple-choice.png")
    freeResponse = resources.Element("Free Response", "tasks/elements/freeResponse", "../static/images/free-response.png")
    trueFalse = resources.Element("True or False", "tasks/elements/trueFalse", "../static/images/true-false.png")
    supplementary = resources.Element("Supp. Material", "tasks/elements/supplementary", "../static/images/video-button.png")
    textContent = resources.Element("Text Content", "tasks/elements/textContent", "../static/images/text-content.jpg")
    problemStatement = resources.Element("Problem Statement", "tasks/elements/problemStatement", "../static/images/problem-statement.png")
    elements = [problemStatement, multipleChoice, freeResponse, trueFalse, supplementary, textContent]
    return elements
