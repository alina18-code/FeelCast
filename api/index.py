
import os
import sys

# Forces Python to look at the root folder where 'app' lives
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from app.routes import app as application

app = application


