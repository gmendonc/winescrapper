import pandas as pd
import plotly.graph_objects as go 
import plotly.express as px


class Result():

    def __init__(self, dtf):
        self.dtf = dtf


    def plot_prices_bycountry(self):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=self.dtf["country"], y=self.dtf["lowest_price"], mode='markers', name='data', line={"color":"black"}))

        fig.update_layout(plot_bgcolor='white', autosize=False, width=1000, height=550)
        
        return fig

    def plot_prices_byscore(self,country, top_boundary):
        fig = go.Figure()
        filtered_df = self.dtf if country == 'World' else self.dtf.loc[(self.dtf.country == country)]
        filtered_df = filtered_df.loc[(filtered_df.lowest_price <= float(top_boundary))]
        nafil = values = {'vivino_rating': 1}
        filtered_df= filtered_df.fillna(value= nafil)
        filtered_df= filtered_df.astype({'vivino_rating':'int32'})
        filtered_df['marker_size'] = pd.cut(filtered_df.vivino_rating, bins=4, labels= [6, 12, 18, 24])
        print("plotando")
        print(filtered_df['vivino_rating'].head())
        fig = px.scatter(
            filtered_df,
            x="vivino_score", 
            y="lowest_price",
            size="marker_size",
            hover_name="wine_name",
            hover_data= {
                'description': True,
                'vivino_rating': True,
                'marker_size': False
            }
        )
        fig.update_traces(marker=dict(color="purple"))
        fig.update_layout(plot_bgcolor='white', autosize=False, width=1000, height=550)
        
        return fig

    def recalibrate_slider(self, country):
        filtered_df = self.dtf if country == 'World' else self.dtf.loc[(self.dtf.country == country)]
        return filtered_df['lowest_price'].max()