import resources


def get_elements():
    multipleChoice = resources.Element("Multiple Choice", "elements/multipleChoice", "../static/images/multiple-choice.png")
    freeResponse = resources.Element("Free Response", "elements/freeResponse", "../static/images/free-response.png")
    trueFalse = resources.Element("True/False", "elements/trueFalse", "../static/images/true-false.png")
    supplementary = resources.Element("Supp. Material", "elements/supplementary", "../static/images/video-button.png")
    questionContent = resources.Element("Question Content", "elements/questionContent", "../static/images/Manda-Pie-Back-To-School-Books.ico")
    elements = [multipleChoice, freeResponse, trueFalse, supplementary, questionContent]
    return elements
