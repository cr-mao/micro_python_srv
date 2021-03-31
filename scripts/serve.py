# -*- coding: utf-8 -*-
import sys

# 暂时这么解决了
sys.path.append("/Users/mac/code/micro_python_srv")

from user_srv import app

if __name__ == "__main__":
    app.serve()
