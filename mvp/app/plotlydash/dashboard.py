import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_bootstrap_components as dbc 
import dash_table
import dash_html_components as html
from app.models import Wineset
from app.plotlydash.results import Result
from app import mongo


def create_dashboard(server):
    dash_app = dash.Dash(server=server,
                          routes_pathname_prefix='/dashapp/',
                          external_stylesheets=[dbc.themes.LUX]
                        )

    wineset = Wineset(mongo.cx)
    data = wineset.get_dataframe()

    # Input
    inputs = dbc.FormGroup([
        html.H4("Selecione o País"),
        dcc.Dropdown(id="country", options=[{"label":x,"value":x} for x in Wineset.get_countrylist(data)], value="World")
    ]) 

    dash_app.layout = dbc.Container(fluid=True, children=[


        dbc.Row([
            dbc.Col(md=3, children=[
                inputs,
                html.Br(),html.Br(),html.Br(),
                html.Div(id="output-panel")
            ]),
            dbc.Col(md=9, children=[
                dbc.Col(html.H4("Wine Price Graph"), width={"size":6,"offset":3}),
                dbc.Tabs(className="nav", children = [
                    dbc.Tab(dash_table.DataTable(id='database-table'), label="Tabela de Dados"),
                    dbc.Tab(dcc.Graph(figure=plot_country_price(data)), label="Gráfico País x Preço")
                ]),
            ]),
        ]),
    ])

    init_callbacks(dash_app, data)

    return dash_app.server


#def create_data_table(df):
#    """Create Dash datatable from Pandas DataFrame."""
#    table = dash_table.DataTable(,
#        style_data = {
#            'whitespace':'normal',
#            'height':'auto',
#        },
#        columns=[{"name": i, "id": i} for i in df.columns],
#        data=df.to_dict('records'),
#        sort_action="native",
#        sort_mode='native',
#        page_size=50
#    )
#    #table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
#    return table

def init_callbacks(dash_app, df):
    @dash_app.callback([
        Output("database-table","style_data"),
        Output("database-table","columns"),
        Output("database-table","data"),
        Output("database-table","sort_action"),
        Output("database-table","sort_mode"),
        Output("database-table","page_size")],
        [Input('country', 'value')])
    def create_data_table(country):
        """Create Dash datatable from Pandas DataFrame."""
        style_data = {
            'whitespace':'normal',
            'height':'auto',
        },
        columns=[{"name": i, "id": i} for i in df.columns],
        if (country=='World'):
            countrydf = df
        else:
            countrydf = df.loc[(df.country == country)]
        data=countrydf.to_dict('records'),
        sort_action="native",
        sort_mode='native',
        page_size=50
        #table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
        return style_data, columns, data, sort_action, sort_mode, page_size



def plot_country_price(df):
    result = Result(df)

    return result.plot_prices_bycountry()

