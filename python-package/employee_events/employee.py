from .query_base import QueryBase
from .sql_execution import QueryMixin

class Employee(QueryBase, QueryMixin):
    """ Provides SQL queries for specific employees
    """
    name = "employee"
   
    def names(self):
        """ returns employee full names and id as list of tuples
        """
        return self.query(f"""
            SELECT first_name || ' ' || last_name, employee_id
            FROM employee
            """)

    def username(self, entity_id):
        """ returns full name of a single employee by ID
        """
        return self.query(f"""
                         SELECT first_name || ' ' || last_name 
                          FROM {self.name}
                          WHERE {self.name}.{self.name}_id = {entity_id}
                          """)

    def model_data(self, id):
        """ reutnrs aggregated event counts for model prediction
        """
        return self.pandas_query(f"""
                    SELECT SUM(positive_events) positive_events
                         , SUM(negative_events) negative_events
                    FROM {self.name}
                    JOIN employee_events
                        USING({self.name}_id)
                    WHERE {self.name}.{self.name}_id = {id}
                """)