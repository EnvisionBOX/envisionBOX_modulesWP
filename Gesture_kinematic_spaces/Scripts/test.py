import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)
import json
import os
from pathlib import Path  # Import pathlib.Path to handle file paths

app = Dash(__name__)
# -- Import and clean data (importing csv into pandas)
df = pd.read_csv('../assets/main.csv')

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Multimodal Dynamic Data Visualizer", style={'text-align': 'center'}),

    dcc.Dropdown(id="mode_rep",
                 options=[
                     {"label": "acting", "value": "acting"},
                     {"label": "representing", "value": "representing"},
                     {"label": "personification", "value": "personification"}],
                 multi=False,
                 value="acting",
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container', children=[], style = {'color': 'white'}),
    html.Br(),
    dcc.Graph(id='MY_XY_Map', figure={},style={'width': '49%', 'textAlign': 'center','display': 'inline-block'}),
    html.Video(controls=True, id='videoplayer', src='', style={'width': '49%', 'textAlign': 'center', 'display': 'inline-block', 'vertical-align': 'top'}, autoPlay=True)

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='MY_XY_Map', component_property='figure'),
     Output(component_id ='videoplayer', component_property='src')],
    [Input(component_id='mode_rep', component_property='value'), Input('MY_XY_Map', 'clickData')]
)


def update_graph(option_slctd, clickData):
    container = "Click on any point to inspect the multimodal event associated with it. \n You subselected events for: {}".format(option_slctd)
    dff = df.copy()
    dff = dff[dff["Mode_of_rep"] == option_slctd]

    # Plotly Express
    fig = px.scatter(
        data_frame=dff,
        x=dff['x'],
        y=dff['y'],
        opacity=0.75,
        #color='Pct of Colonies Impacted',
        hover_data=['English'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'1st dimension': 'second dimension'},
        template='plotly_dark'
    )
    fig.update_traces(marker_size=15)

    #get the video clicked on
    check = str(clickData)
    converted_to_legal_json = check.replace("'", '"')
    test = eval(converted_to_legal_json)
    src = ''
    if test is not None:
        test = eval(str(converted_to_legal_json))
        test = eval(str(test['points']))
        test = eval(str(test[0]))
        src = os.path.abspath( '../Videos/WithMotionTracking/' + test['customdata'][0] + '_silent_gesture.mp4')            
        print(src)
    return container, fig, src

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
