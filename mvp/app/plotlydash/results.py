import pandas as pd
import plotly.graph_objects as go 


class Result():

    def __init__(self, dtf):
        self.dtf = dtf


    def plot_prices_bycountry(self):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=self.dtf["country"], y=self.dtf["lowest_price"], mode='markers', name='data', line={"color":"black"}))

        fig.update_layout(plot_bgcolor='white', autosize=False, width=1000, height=550)
        
        return fig

    def plot_prices_byscore(self,country):
        fig = go.Figure()
        filtered_df = self.dtf if country == 'World' else self.dtf.loc[(self.dtf.country == country)]
        print("plotando")
        print(filtered_df['vivino_score'].head())
        fig.add_trace(go.Scatter(
            x=filtered_df["vivino_score"], 
            y=filtered_df["lowest_price"], 
            mode='markers', 
            marker_color='purple',
            text=filtered_df['wine_name'] 
        ))

        fig.update_layout(plot_bgcolor='white', autosize=False, width=1000, height=550)
        
        return fig