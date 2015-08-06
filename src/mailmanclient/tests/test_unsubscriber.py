# Copyright (C) 2015 by the Free Software Foundation, Inc.
#
# This file is part of mailman.client.
#
# mailman.client is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, version 3 of the License.
#
# mailman.client is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with mailman.client.  If not, see <http://www.gnu.org/licenses/>.

"""Test cases for client method to get count of unsubscribers"""

from __future__ import absolute_import, print_function, unicode_literals

__metaclass__ = type
__all__ = [
    'TestCountUnsubscriber',
    ]


import unittest

from mailmanclient import Client
from six.moves.urllib_error import HTTPError
import datetime

class TestCountUnsubscriber(unittest.TestCase):
    def setUp(self):
        self._client = Client(
            'http://localhost:9001/3.0', 'restadmin', 'restpass')

    def test_count_unsubscriber_invalid_start_date_format(self):
        # Trying to get count of unsubscribes with an invalid start date format.
        try:
            self._client.count_unsubscriber('dev@localhost.localdomain', '15-06-06')
        except ValueError as error:
            self.assertEqual(error.message, "Incorrect date format for the starting date, should be YYYY-MM-DD")

    def test_count_unsubscriber_invalid_start_date(self):
        # Trying to get count of unsubscribes with a start date after current date.
        start = datetime.date.today() + datetime.timedelta(days=1)
        try:
            self._client.count_unsubscriber('dev@localhost.localdomain', start.strftime('%Y-%m-%d'))
        except ValueError as error:
            self.assertEqual(error.message, "The starting date should not be greater than present date")

    def test_count_unsubscriber_invalid_stop_date_format(self):
        # Trying to get count of unsubscribes with an invalid stop date format.
        start = datetime.date.today() - datetime.timedelta(days=1)
        try:
            self._client.count_unsubscriber('dev@localhost.localdomain', start.strftime('%Y-%m-%d'), '15-06-06')
        except ValueError as error:
            self.assertEqual(error.message, "Incorrect date format for ending date, should be YYYY-MM-DD")

    def test_count_unsubscriber_invalid_dates(self):
        # Trying to get count of unsubscribes with a start date greater than stop date.
        start = datetime.date.today() - datetime.timedelta(days=1)
        stop = datetime.date.today() - datetime.timedelta(days=5)
        try:
            self._client.count_unsubscriber('dev@localhost.localdomain', start.strftime('%Y-%m-%d'), stop.strftime('%Y-%m-%d'))
        except ValueError as error:
            self.assertEqual(error.message, "The starting date should not be greater than ending date")

    def test_count_unsubscriber_only_stop_date(self):
        # Trying to get count of unsubscribes with only a stop date.
        stop = datetime.date.today()
        try: 
            self._client.count_unsubscriber('dev@localhost.localdomain', None, stop.strftime('%Y-%m-%d'))
        except ValueError as error:
            self.assertEqual(error.message, "Wrong Input: Only ending date provided")

