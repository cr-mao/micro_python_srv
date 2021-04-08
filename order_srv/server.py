import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from order_srv import app

if __name__ == "__main__":
    app.serve()
