from sqlite3 import connect
from pathlib import Path
from functools import wraps
import pandas as pd

# create path variable to point to abs path for employee events db
db_path = Path(__file__).parent / 'employee_events.db'

# class to receive sql querys
class QueryMixin:
    """ class to receive SQL querys, method to return results as a dataframe
        and method to return as tuples
        """

    def pandas_query(self, sql_query):
        conn = connect(db_path)
        df = pd.read_sql_query(sql_query, conn)
        conn.close()
        return df

    def query(self, sql_query):
        conn = connect(db_path)
        cursor = conn.cursor()
        cursor.execute(sql_query)
        results = cursor.fetchall()
        conn.close()
        return results
    

def query(func):
    """
    Decorator that runs a standard sql execution
    and returns a list of tuples
    """

    @wraps(func)
    def run_query(*args, **kwargs):
        query_string = func(*args, **kwargs)
        connection = connect(db_path)
        cursor = connection.cursor()
        result = cursor.execute(query_string).fetchall()
        connection.close()
        return result
    
    return run_query
