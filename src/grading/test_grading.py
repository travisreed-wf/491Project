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

class TestCalcualate_Correctness_Input_Characteristics(unittest.TestCase):

        def setUp(self):
            models = patch.object(grading, "models")
            self.addCleanup(models.stop)
            self.models = models.start()

        def test1ValidId(self):
            # questions answered correctly  = true
            # percent graded  = 0
            # number of questions = 0
            # reponse id is valid = true
            # question type = manual
            grader = grading.Grader()
            taskResponse = Mock()
            self.models.TaskResponse.query.filter_by.return_value.first.return_value = taskResponse
            taskResponse.graded_response = json.dumps({
            'automatic_questions':[],
            'manual_questions':[]
            })
            taskResponse.graded = None
            ret = grader.calculate_correctness(1)
            self.assertEqual(taskResponse.graded, True)
            self.assertEqual(ret,0)

        def test2InvalidIdInfeasible(self):
            # questions answered correctly  = true
            # percent graded  = 1-99
            # number of questions = multiple
            # reponse id is valid = false
            # question type = automatic
            grader = grading.Grader()
            taskResponse = Mock()
            self.models.TaskResponse.query.filter_by.return_value.first.return_value = taskResponse
            taskResponse.graded_response = json.dumps({
                'automatic_questions':[{'correct':True},{'correct':False}],
                'manual_questions':[]
                })
            taskResponse.graded = None
            ret = grader.calculate_correctness(1)
            # length of questions = 2
            # total graded = 2
            # 0 = 0 so true.
            self.assertEqual(taskResponse.graded, True)
            self.assertEqual(ret,50)

        def test3InvalidIdInfeasible(self):
            # questions answered correctly  = true
            # percent graded  = 100
            # number of questions = 1
            # reponse id is valid = false
            # question type = manual
            grader = grading.Grader()
            taskResponse = Mock()
            self.models.TaskResponse.query.filter_by.return_value.first.return_value = taskResponse
            taskResponse.graded_response = json.dumps({
                'automatic_questions':[],
                'manual_questions':[{'correct': True}]
                })
            taskResponse.graded = None
            ret = grader.calculate_correctness(1)
            # length of questions = 0
            # total graded = 0
            # 0 = 0 so true.
            self.assertEqual(taskResponse.graded, True)
            self.assertEqual(ret,100)

        def test4InvalidIdInfeasible(self):
            # questions answered correctly  = false
            # percent graded  = 0
            # number of questions = multiple
            # reponse id is valid = false
            # question type = automatic
            grader = grading.Grader()
            taskResponse = Mock()
            self.models.TaskResponse.query.filter_by.return_value.first.return_value = taskResponse
            taskResponse.graded_response = json.dumps({
                'automatic_questions':[{'correct': False},{'correct': False}],
                'manual_questions':[]
                })
            taskResponse.graded = None
            ret = grader.calculate_correctness(1)
            # length of questions = 0
            # total graded = 0
            # 0 = 0 so true.
            self.assertEqual(taskResponse.graded, True)
            self.assertEqual(ret,0)

            #infeasible - Can't have 1 question answered correctly with automatic grdaed question
            #with percent graded as 1-99
        def test5ValidId(self):
            # questions answered correctly  = false
            # percent graded  = 1-99
            # number of questions = 1
            # reponse id is valid = true
            # question type = automatic
            grader = grading.Grader()
            taskResponse = Mock()
            self.models.TaskResponse.query.filter_by.return_value.first.return_value = taskResponse
            taskResponse.graded_response = json.dumps({
                'automatic_questions':[{'correct':False}],
                'manual_questions':[]
                })
            taskResponse.graded = None
            ret = grader.calculate_correctness(1)
            self.assertEqual(taskResponse.graded, True)
            self.assertEqual(ret,0)

        def test6InvalidIdInfeasible(self):
            # questions answered correctly  = false
            # percent graded  = 100
            # number of questions = 0
            # reponse id is valid = false
            # question type = automatic
            grader = grading.Grader()
            taskResponse = Mock()
            self.models.TaskResponse.query.filter_by.return_value.first.return_value = taskResponse
            taskResponse.graded_response = json.dumps({
                'automatic_questions':[],
                'manual_questions':[]
                })
            taskResponse.graded = None
            ret = grader.calculate_correctness(1)
            # length of questions = 0
            # total graded = 0
            # 0 = 0 so true.
            self.assertEqual(taskResponse.graded, True)
            self.assertEqual(ret,0)

        def test7InvalidIdInfeasible(self):
            # questions answered correctly  = Not graded
            # percent graded  = 0
            # number of questions = 1
            # reponse id is valid = false
            # question type = automatic
            grader = grading.Grader()
            taskResponse = Mock()
            self.models.TaskResponse.query.filter_by.return_value.first.return_value = taskResponse
            taskResponse.graded_response = json.dumps({
                'automatic_questions':[{'correct':''}],
                'manual_questions':[]
                })
            taskResponse.graded = None
            ret = grader.calculate_correctness(1)
            self.assertEqual(taskResponse.graded, True)
            self.assertEqual(ret,0)

            #infeasible. Can't have zero questions and a grade 1-99
        def test8ValidId(self):
            # questions answered correctly  = Not Graded
            # percent graded  = 1-99
            # number of questions = 0
            # reponse id is valid = true
            # question type = manual
            grader = grading.Grader()
            taskResponse = Mock()
            self.models.TaskResponse.query.filter_by.return_value.first.return_value = taskResponse
            taskResponse.graded_response = json.dumps({
                'automatic_questions':[],
                'manual_questions':[]
                })
            taskResponse.graded = None
            ret = grader.calculate_correctness(1)
            # length of questions = 0
            # total graded = 0
            # 0 = 0 so true.
            self.assertEqual(taskResponse.graded, True)
            self.assertEqual(ret,0)

        def test9ValidIdInfeasible(self):
            # questions answered correctly  = Not Graded
            # percent graded  = 100
            # number of questions = multiple
            # reponse id is valid = true
            # question type = manual
            grader = grading.Grader()
            taskResponse = Mock()
            self.models.TaskResponse.query.filter_by.return_value.first.return_value = taskResponse
            taskResponse.graded_response = json.dumps({
                'automatic_questions':[],
                'manual_questions':[{'correct':''},{'correct':''}]
                })
            taskResponse.graded = None
            ret = grader.calculate_correctness(1)
            # length of questions = 0
            # total graded = 0
            # 0 = 0 so true.
            self.assertEqual(taskResponse.graded, True)
            self.assertEqual(ret,0)

        def test10InvalidIdInfeasible(self):
            # questions answered correctly  = Not Answered
            # percent graded  = 0
            # number of questions = multiple
            # reponse id is valid = false
            # question type = automatic
            grader = grading.Grader()
            taskResponse = Mock()
            self.models.TaskResponse.query.filter_by.return_value.first.return_value = taskResponse
            taskResponse.graded_response = json.dumps({
                'automatic_questions':[{'correct':False},{'correct':False}],
                'manual_questions':[]
                })
            taskResponse.graded = None
            ret = grader.calculate_correctness(1)
            self.assertEqual(taskResponse.graded, True)
            self.assertEqual(ret,0)

            #Infeasible. If the questions aren't answered then the score will be 0
            # not 1-99
        def test11ValidId(self):
            # questions answered correctly  = Not Answered
            # percent graded  = 1-99
            # number of questions = 1
            # reponse id is valid = true
            # question type = manual
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

        def test12InvalidIdInfeasible(self):
            # questions answered correctly  = Not Answered
            # percent graded  = 100
            # number of questions = 0
            # reponse id is valid = false
            # question type = automatic
            grader = grading.Grader()
            taskResponse = Mock()
            self.models.TaskResponse.query.filter_by.return_value.first.return_value = taskResponse
            taskResponse.graded_response = json.dumps({
                'automatic_questions':[],
                'manual_questions':[]
                })
            taskResponse.graded = None
            ret = grader.calculate_correctness(1)
            self.assertEqual(taskResponse.graded, True)
            self.assertEqual(ret,0)

        def test13InvalidIdInfeasible(self):
            # questions answered correctly  = false
            # percent graded  = 0
            # number of questions = 1
            # reponse id is valid = false
            # question type = manual
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











