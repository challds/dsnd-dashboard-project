from .sql_execution import QueryMixin


class QueryBase:
    """Base class providing shared SQL queries
    """
    name = ""

    def names(self):
        return []

    def event_counts(self, entity_id):
        """returns cumulative pos and neg event counts grouped by date
        """
        
        query = f"""
             SELECT event_date,
                  SUM(positive_events) AS positive_events,
                  SUM(negative_events) AS negative_events
             FROM {self.name}
             INNER JOIN employee_events
                  ON {self.name}.{self.name}_id = employee_events.{self.name}_id
             WHERE {self.name}.{self.name}_id = {entity_id}
             GROUP BY event_date
             ORDER BY event_date
         """
        return self.pandas_query(query)
            
    def notes(self, entity_id):
        """ returns notes for the entity
        """
        query = f"""
            SELECT note_date, note
            FROM {self.name}
            INNER JOIN notes
                ON {self.name}.{self.name}_id = notes.{self.name}_id
            WHERE {self.name}.{self.name}_id = {entity_id}
        """
        return self.pandas_query(query)
