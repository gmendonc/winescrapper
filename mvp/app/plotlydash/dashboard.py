import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_bootstrap_components as dbc 
import dash_table
import dash_html_components as html
from app.models import Winedb


def create_dashboard(server):
    dash_app = dash.Dash(server=server,
                          routes_pathname_prefix='/dashapp/',
                          external_stylesheets=[dbc.themes.COSMO]
                        )

    winedb = Winedb()
    data = winedb.get_dataframe()

    dash_app.layout = dbc.Container(fluid=True, children=[
        html.H1("Aqui vão os gráficos"),
        html.Br(), html.Br(), html.Br(),
        create_data_table(data),
    ])

    #init_callbacks(dash_app)

    return dash_app.server


def create_data_table(df):
    """Create Dash datatable from Pandas DataFrame."""
    table = dash_table.DataTable(
        id='database-table',
        style_data = {
            'whitespace':'normal',
            'height':'auto',
        },
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        sort_action="native",
        sort_mode='native',
        page_size=50
    )
    #table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
    return table
