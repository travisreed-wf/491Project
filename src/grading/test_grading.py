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


class TestCalcualateCorrectnessInputCharacteristics(unittest.TestCase):

        def setUp(self):
            models = patch.object(grading, "models")
            self.addCleanup(models.stop)
            self.models = models.start()

        def test1(self):
            # Response id valid  = true
            # Q1 type = manual
            # Q1 correct = true
            # Q2 type = manual
            # Q2 correct = true
            grader = grading.Grader()
            task_response = Mock()
            self.models.TaskResponse.query.filter_by.return_value.first.return_value = task_response
            question1 = {"correct": True}
            question2 = {"correct": True}
            task_response.graded_response = json.dumps({
                'automatic_questions':[],
                'manual_questions':[question1, question2]
            })
            task_response.graded = None
            ret = grader.calculate_correctness(1)
            self.assertEqual(task_response.graded, True)
            self.assertEqual(ret,100)



        def test21(self):
            # Response id valid = false
            # Q1 type = automatic
            # Q1 correct = true
            # Q2 type = none
            # Q2 correct = not answered
            grader = grading.Grader()
            task_response = Mock()
            self.models.TaskResponse.query.filter_by.return_value.first.return_value = None
            question1 = {"correct": True}
            question2 = {}
            task_response.graded_response = json.dumps({
                'automatic_questions': [question1],
                'manual_questions': []
            })
            task_response.graded = None
            with self.assertRaises(AttributeError):
                grader.calculate_correctness(1)

        def test22_infeasable(self):
            # Response id valid = True
            # Q1 type = automatic
            # Q1 correct = not graded
            # Q2 type = automatic
            # Q2 correct = not asked
            grader = grading.Grader()
            task_response = Mock()
            self.models.TaskResponse.query.filter_by.return_value.first.return_value = task_response
            question1 = {"correct": None}
            question2 = {}
            task_response.graded_response = json.dumps({
                'automatic_questions': [question1],
                'manual_questions': []
            })
            task_response.graded = None
            ret = grader.calculate_correctness(1)
            self.assertEqual(task_response.graded, True)
            self.assertEqual(ret, 0)

        def test23(self):
            # Response id valid = false
            # Q1 type = automatic
            # Q1 correct = not graded
            # Q2 type = automatic
            # Q2 correct = not asked
            grader = grading.Grader()
            task_response = Mock()
            self.models.TaskResponse.query.filter_by.return_value.first.return_value = None
            question1 = {"correct": None}
            question2 = {'correct': None}
            task_response.graded_response = json.dumps({
                'automatic_questions': [question1],
                'manual_questions': []
            })
            task_response.graded = None
            with self.assertRaises(AttributeError):
                grader.calculate_correctness(1)

        def test24(self):
            # Response id valid = false
            # Q1 type = automatic
            # Q1 correct = not graded
            # Q2 type = automatic
            # Q2 correct = not graded
            grader = grading.Grader()
            task_response = Mock()
            self.models.TaskResponse.query.filter_by.return_value.first.return_value = None
            question1 = {"correct": None}
            question2 = {'correct': None}
            task_response.graded_response = json.dumps({
                'automatic_questions': [question1, question2],
                'manual_questions': []
            })
            task_response.graded = None
            with self.assertRaises(AttributeError):
                grader.calculate_correctness(1)

        def test25(self):
            # Response id valid = false
            # Q1 type = manual
            # Q1 correct = not answered
            # Q2 type = none
            # Q2 correct = not asked
            grader = grading.Grader()
            task_response = Mock()
            self.models.TaskResponse.query.filter_by.return_value.first.return_value = None
            question1 = {"correct": None}
            question2 = {}
            task_response.graded_response = json.dumps({
                'automatic_questions': [question1],
                'manual_questions': []
            })
            task_response.graded = None
            with self.assertRaises(AttributeError):
                grader.calculate_correctness(1)








