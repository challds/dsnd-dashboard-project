from .query_base import QueryBase
from .sql_execution import QueryMixin

class Team(QueryBase, QueryMixin):
    """ provides SQL queries for teams
    """
    name = "team"

    def names(self):
        """ returns all team names and IDs as list of tuples
        """
        return self.query(f"""
                      SELECT team_name, team_id
                      FROM team
                      """)

    def username(self, entity_id):
        """ returns team name for a single team by ID
        """
        return self.query(f"""
                          SELECT team_name
                          FROM {self.name}
                          WHERE {self.name}.{self.name}_id = {entity_id}
                          """)

    def model_data(self, id):
        """ returns per employee event counts for team-level prediction
        """
        return self.pandas_query(f"""
            SELECT positive_events, negative_events FROM (
                    SELECT employee_id
                         , SUM(positive_events) positive_events
                         , SUM(negative_events) negative_events
                    FROM {self.name}
                    JOIN employee_events
                        USING({self.name}_id)
                    WHERE {self.name}.{self.name}_id = {id}
                    GROUP BY employee_id
                   )
                """)