import datetime
import json
import unittest

from mock import Mock
from mock import patch

import views


class TestTaskListView(unittest.TestCase):

    def setUp(self):
        DT = patch.object(views, "DT")
        self.addCleanup(DT.stop)
        self.DT = DT.start()
        self.DT.date.today.return_value = datetime.date(2014, 01, 31)

        current_user = patch.object(views, "current_user")
        self.addCleanup(current_user.stop)
        self.current_user = current_user.start()
        self.current_user.task_responses = [Mock(task_id=1)]

        self.task1 = Mock()
        self.task1.serialize = {
            'duedate': "dd1"
        }

        self.course1 = Mock()
        self.course1.tasks = []

    def test_clause1_true(self):
        duedate = datetime.date(2014, 01, 30)
        self.task1.duedate.date.return_value = duedate
        self.task1.status = "available"
        self.task1.id = 1
        self.course1.tasks = [self.task1]
        self.current_user.courses = [self.course1]
        ret = views.TaskListView().get()
        ret = json.loads(ret)
        self.assertEqual(ret['complete'], [self.task1.serialize])

    def test_clause1_false(self):
        duedate = datetime.date(2014, 01, 30)
        self.task1.duedate.date.return_value = duedate
        self.task1.status = "available"
        self.task1.id = 1
        self.course1.tasks = [self.task1]
        self.current_user.courses = []
        ret = views.TaskListView().get()
        ret = json.loads(ret)
        self.assertEqual(ret['complete'], [])
