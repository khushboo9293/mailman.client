# Copyright (C) 2010-2015 by the Free Software Foundation, Inc.
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

"""Client for Hyperkitty."""

from __future__ import absolute_import, unicode_literals

__metaclass__ = type
__all__ = [
    'Client_hyperkitty',
    
]

import six
import json

from base64 import b64encode
from httplib2 import Http
from mailmanclient import __version__
from operator import itemgetter
from six.moves.urllib_error import HTTPError
from six.moves.urllib_parse import urlencode, urljoin

class Client_hyperkitty:
    def __init__(self):
       self.url = "http://127.0.0.1:8000/hyperkitty/all_threads/"
       auth = '{0}:{1}'.format('hyperkitty', 'hkpass')
       auth_encode = b64encode(auth.encode('utf-8')).decode('utf-8')
       self.headers = {'Authorization' : 'Basic ' + auth_encode}

    def get_unique_subject_lines(self, mlist):
        response, content = Http().request(self.url+mlist, 'GET', None, self.headers)
        if response.status // 100 != 2:
            raise HTTPError(self.url, response.status, content, response, None)
        return content
      
    def get_no_of_subscribers_posted(self, mlist):
        url = self.url+'participants/'+mlist
        response, content = Http().request(url, 'GET', None, self.headers)
        if response.status // 100 != 2:
            raise HTTPError(url, response.status, content, response, None)
        return content

