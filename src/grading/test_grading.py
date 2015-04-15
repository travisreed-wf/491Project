import json
import unittest

from mock import Mock
from mock import patch

import grading

class TestGradeAutomaticQuestions(unittest.TestCase):

    def setUp(self):
        models = patch.object(grading, "models")
        self.addCleanup(models.stop)
        self.models = models.start()

    def test_ABD(self):
        grader = grading.Grader()
        taskResponse = Mock()
        taskResponse.graded_response = True
        self.models.TaskResponse.query.filter_by.return_value.first.return_value = taskResponse
        ret = grader.grade_automatic_questions(1)
        self.assertEqual(ret, None)

    def test_ABCEFMPSUV(self):
        grader = grading.Grader()
        taskResponse = Mock()
        taskResponse.graded_response = False
        taskResponse.response = json.dumps({
            'automatic_questions':[],
            'manual_questions':[]
            })
        taskResponse.correctness_grade = None
        taskResponse.task = Mock()
        taskResponse.task.questions = json.dumps([])
        self.models.TaskResponse.query.filter_by.return_value.first.return_value = taskResponse
        ret = grader.grade_automatic_questions(1)
        self.assertEqual(taskResponse.correctness_grade, 0)
        self.assertEqual(ret,[])

class TestCalculate_Correctness(unittest.TestCase):

        def setUp(self):
            models = patch.object(grading, "models")
            self.addCleanup(models.stop)
            self.models = models.start()

        def test_ABCDEGBCDFGBHPRS(self):
            grader = grading.Grader()
            taskResponse = Mock()
            self.models.TaskResponse.query.filter_by.return_value.first.return_value = taskResponse
            taskResponse.graded_response = json.dumps({
            'automatic_questions':[{'correct': True},{'correct':False}],
            'manual_questions':[]
            })
            taskResponse.graded = None
            ret = grader.calculate_correctness(1)
            self.assertEqual(taskResponse.graded, True)
            self.assertEqual(ret,50)

        def test_ABHIJKMOHPRS(self):
            grader = grading.Grader()
            taskResponse = Mock()
            self.models.TaskResponse.query.filter_by.return_value.first.return_value = taskResponse
            taskResponse.graded_response = json.dumps({
            'automatic_questions':[],
            'manual_questions':[{'correct':False}]
            })
            taskResponse.graded = None
            ret = grader.calculate_correctness(1)
            self.assertEqual(taskResponse.graded, True)
            self.assertEqual(ret,0)

        def test_ABHIJKMNHIJKMNHPQS(self):
            grader = grading.Grader()
            taskResponse = Mock()
            self.models.TaskResponse.query.filter_by.return_value.first.return_value = taskResponse
            taskResponse.graded_response = json.dumps({
            'automatic_questions':[],
            'manual_questions':[{},{}]
            })
            taskResponse.graded = None
            ret = grader.calculate_correctness(1)
            self.assertEqual(taskResponse.graded, False)
            self.assertEqual(ret,0)

        def test_ABHIJLMOHIJLMOHPRS(self):
            grader = grading.Grader()
            taskResponse = Mock()
            self.models.TaskResponse.query.filter_by.return_value.first.return_value = taskResponse
            taskResponse.graded_response = json.dumps({
            'automatic_questions':[],
            'manual_questions':[{'correct':True},{'correct':True}]
            })
            taskResponse.graded = None
            ret = grader.calculate_correctness(1)
            self.assertEqual(taskResponse.graded, True)
            self.assertEqual(ret,100)



