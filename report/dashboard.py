from fasthtml.common import *
import matplotlib.pyplot as plt
from employee_events import QueryBase, Employee, Team
from utils import load_model

"""
Below, we import the parent classes
you will use for subclassing
"""
from base_components import (
    Dropdown,
    BaseComponent,
    Radio,
    MatplotlibViz,
    DataTable
    )

from combined_components import FormGroup, CombinedComponent


class ReportDropdown(Dropdown):
    """ dropdown populated with entity names from db
    """
    def build_component(self, entity_id, model):
        self.label = model.name
        return super().build_component(entity_id, model)

    def component_data(self, entity_id, model):
        return model.names()


class Header(BaseComponent):
    """ displays entity type as page header
    """
    def build_component(self, entity_id, model):
        return H1(model.name)


class LineChart(MatplotlibViz):
    """ cumulative pos and neg event counts over time
    """
    # strange behavior exists when selected a person with no data, so updated it
    # to handle empty data more reliably
    def build_component(self, entity_id, model):
        df = model.event_counts(entity_id)
        if df.empty:
            return P("No data found for this selection.")
        return super().build_component(entity_id, model)
    def visualization(self, entity_id, model):
        df = model.event_counts(entity_id)
        df = df.fillna(0)
        df = df.set_index('event_date')
        df = df.sort_index()
        df = df.cumsum()
        df.columns = ['Positive', 'Negative']
        fig, ax = plt.subplots()
        df.plot(ax = ax)
        ax.set_title('Cumulative Event Counts')
        self.set_axis_styling(ax, bordercolor = 'black', fontcolor = 'black')
        ax.set_xlabel('Date', fontsize = 10,
                       color = 'black', fontweight = 'bold')
        ax.set_ylabel('Cumulative Count', fontsize = 10,
                       color = 'black', fontweight = 'bold')


class BarChart(MatplotlibViz):
    """ predicted recruitment risk from the ml model
    """
    predictor = load_model()

    def build_component(self, entity_id, model):
        data = model.model_data(entity_id)
        if data.empty:
            return P("No data found for this selection.")
        return super().build_component(entity_id, model)

    def visualization(self, entity_id, model):
        data = model.model_data(entity_id)
        pred_proba = self.predictor.predict_proba(data)
        pred_proba = pred_proba[:, 1]
        if model.name == 'team':
            pred = pred_proba.mean()
        else:
            pred = pred_proba[0]
        fig, ax = plt.subplots()
        ax.barh([''], [pred])
        ax.set_xlim(0, 1)
        ax.set_title('Predicted Recruitment Risk', fontsize=20)
        self.set_axis_styling(ax)


class Visualizations(CombinedComponent):
    children = [LineChart(), BarChart()]
    outer_div_type = Div(cls='grid')
            

class NotesTable(DataTable):
    def component_data(self, entity_id, model):
        return model.notes(entity_id)

class DashboardFilters(FormGroup):
    id = "top-filters"
    action = "/update_data"
    method="POST"
    children = [
        Radio(
            values=["Employee", "Team"],
            name='profile_type',
            hx_get='/update_dropdown',
            hx_target='#selector'
            ),
        ReportDropdown(
            id="selector",
            name="user-selection")
        ]
    

class Report(CombinedComponent):

    children = [Header(), DashboardFilters(), Visualizations(), NotesTable()]
app, rt = fast_app()
report = Report()
@rt("/")
def get():
    return report(1, Employee())
@rt('/employee/{id:str}')
def get_employee(id: str):
    return report(id, Employee())
@rt('/team/{id:str}')
def get_team(id: str):
    return report(id, Team())
@app.get('/update_dropdown{r}')
def update_dropdown(r):
    dropdown = DashboardFilters.children[1]
    print('PARAM', r.query_params['profile_type'])
    if r.query_params['profile_type'] == 'Team':
        return dropdown(None, Team())
    elif r.query_params['profile_type'] == 'Employee':
        return dropdown(None, Employee())


@app.post('/update_data')
async def update_data(r):
    from fasthtml.common import RedirectResponse
    data = await r.form()
    profile_type = data._dict['profile_type']
    id = data._dict['user-selection']
    if profile_type == 'Employee':
        return RedirectResponse(f"/employee/{id}", status_code=303)
    elif profile_type == 'Team':
        return RedirectResponse(f"/team/{id}", status_code=303)
    


serve()
