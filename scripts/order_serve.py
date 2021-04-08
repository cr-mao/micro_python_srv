# -*- coding: utf-8 -*-
import os
import sys

# pycharm给我们会加上当前项目到path中  ，
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from order_srv import app

if __name__ == "__main__":
    app.serve()
