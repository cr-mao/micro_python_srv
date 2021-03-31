import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from user_srv import app

if __name__ == "__main__":
    app.serve()
