#!/usr/bin/python

import pydelicious

# delicious website keeps throw 503 now (2017.02)
# cannot login, and no idea about useable api list

a = pydelicious.apiNew('user', 'passwd')
a.tags_get() # Same as:
a.request('tags/get', )

