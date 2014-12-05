#!/usr/bin/python3

import os
import sys
sys.path.insert(0, os.path.join(os.path.expanduser('~'), 'uni_web'))

from website import app as application
application.secret_key = b'\xda\x9a\xfa6\x0b\xf5`\xf8GS\xbb\xca\x9c\xb2\xed\x87\xdc\xf4 \xd6eY\xcf\x82'
