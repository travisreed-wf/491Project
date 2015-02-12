import json

import models


class Grader:

    def __init__(self):
        pass

    def grade_automatic_questions(self, response_id):
        task_response = models.TaskResponse.query.filter_by(id=response_id).first()
        if task_response.graded_response:
            return
        response = json.loads(task_response.response)
        task = task_response.task
        task_questions = json.loads(task.questions)
        for question in response['automatic_questions']:
            for task_question in task_questions:
                if task_question['questionID'] == question['questionID']:
                    correctOption = task_question['correctOption']
                    correct = (question['selectedOption'] == correctOption)
                    question['correctOption'] = correctOption
                    question['correct'] = correct
        task_response.graded_response = json.dumps(response)
        models.db.session.commit()
        return response['automatic_questions']