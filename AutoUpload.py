# -*- coding:utf-8 -*-
"""
文件自动上传工具
主要功能：
监控制定目录下的数据文件修改，当文件修改后 文件自动上传到服务器
"""
__author__ = 'Tu'
import Queue
import threading
from PyQt4.QtCore import *
from PyQt4.QtGui import *

eventQueue  = Queue.Queue()             #事件队列 当监控器接受到事件后将事件信息发送到队列


