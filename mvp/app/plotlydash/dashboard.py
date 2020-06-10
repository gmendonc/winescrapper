import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_bootstrap_components as dbc 
import dash_table
import dash_html_components as html
from app.models import Wineset
from app.plotlydash.results import Result
from app import mongo
import math

def get_log(value, flag= False):
    log_value = math.log10(value)
    return int(log_value) if flag else log_value

def get_navbar():
    # Navbar
    navbar = dbc.NavbarSimple(className="nav nav-pills", children=[
        dbc.NavItem(
            dbc.NavLink("Home", href="/index")
        )
    ])
    return navbar

def create_dashboard(server):
    dash_app = dash.Dash(server=server,
                          routes_pathname_prefix='/dashapp/',
                          external_stylesheets=[dbc.themes.LUX]
                        )

    wineset = Wineset(mongo.cx)
    data = wineset.get_formatted_dataframe()

    # Input
    inputs = dbc.FormGroup([
        html.H4("Selecione o País"),
        dcc.Dropdown(id="country", options=[{"label":x,"value":x} for x in Wineset.get_countrylist(data)], value="World")
    ]) 

    dash_app.layout = dbc.Container(fluid=True, children=[
        get_navbar(),
        dbc.Row([
            dbc.Col(md=2, children=[
                inputs,
                html.Br(),html.Br(),html.Br(),
                html.Div(id="output-panel")
            ]),
            dbc.Col(md=10, children=[
                dbc.Col(html.H4("Catálogo Wine"), width={"size":6,"offset":3}),
                dbc.Tabs(className="nav", children = [
                    dbc.Tab(
                        create_first_data_table('database-table', data), 
                    label="Tabela de Dados"),
                    dbc.Tab(children = [
                        dcc.Graph(id='wine_score_graph'),
                        dcc.Slider(
                            id='price_slider',
                            min=0,
                            max=get_log(data['lowest_price'].max()),
                            value=get_log(data['lowest_price'].max()),
                            marks = {i: '{}'.format(10 ** i) for i in range(get_log(data['lowest_price'].max(),True)+1)},
                            step= 0.01
                        ),
                        html.Div(id='slider_output_container')],
                        label="Gráfico Avaliação x Preço")
                ]),
            ]),
        ]),
    ])

    init_callbacks(dash_app, data)

    return dash_app.server


def create_first_data_table(table_id, df):
    """Create Dash datatable from Pandas DataFrame."""
    filtered_df = df[['Nome', 'country', 'lowest_price', 'Score']]
    table = dash_table.DataTable(
        id = table_id,
        style_data = {
            'whitespace':'normal',
            'height':'auto',
        },
        columns=[{
            "name": i, 
            "id": i,
            "presentation": "markdown"} for i in filtered_df.columns],
        data=filtered_df.to_dict('records'),
        filter_action="native",
        sort_action="native",
        sort_mode='native',
        page_size=50
    )
    #table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
    return table

def init_callbacks(dash_app, df):

    result = Result(df)

    @dash_app.callback(
        Output("database-table","data"),
        [Input('country', 'value')])
    def create_data_table(country):
        print("Criando tabela de dados para o país:", country)
        """Create Dash datatable from Pandas DataFrame."""
        filtered_df = df[['Nome', 'country', 'lowest_price', 'Score']]
        countrydf = filtered_df if country == 'World' else df.loc[(df.country == country)]
        data=countrydf.to_dict('records')
        return data
    
    @dash_app.callback(
        Output("wine_score_graph","figure"),
        [Input('country', 'value'),
         Input('price_slider', 'value')])
    def update_graph(country, value):
        return result.plot_prices_byscore(country, 10 ** value)

    @dash_app.callback(
        Output("price_slider","max"),
        [Input('country', 'value')])
    def update_slider(country):
        return get_log(result.recalibrate_slider(country))

    @dash_app.callback(
        Output("slider_output_container","children"),
        [Input('price_slider', 'value')])
    def show_slider_value(value):
        return 'Preço Máximo: "${:20,.2f}"'.format(10 ** value)
        


#def plot_prices(df):
#    result = Result(df)
#    print("Estou no plot_prices")
#    print(df['vivino_score'].head())
#
#    return result.plot_prices_byscore()

