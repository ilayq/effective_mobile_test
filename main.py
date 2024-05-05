from src import FileDataBase
from src import FinanceControllerApp
import sys

if len(sys.argv) > 1:
    filename = sys.argv[1]
else: 
    filename = 'data.db'

db = FileDataBase(filename)

with FinanceControllerApp(db) as app: # autocommit on exit
    app.run()
