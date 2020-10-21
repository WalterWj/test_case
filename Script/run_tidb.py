#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import mysql.connector
import argparse
import time
import os
import threading

from multiprocessing import Process

try:
    import Queue
except:
    import queue

## If Python is version 2.7, encoding problems can reload sys configuration
try:
    import sys

    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

