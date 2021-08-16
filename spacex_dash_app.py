# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id = 'site-dropdown',options = [
                                    {'label': 'All Sites','value':'All Sites'},
                                    {'label':'CCAFS LC-40','value':'CCAFS LC-40'},
                                    {'label':'CCAFS SLC-40','value':'CCAFS SLC-40'},
                                    {'label':'VAFB SLC-4E','value':'VAFB SLC-4E'},
                                    {'label':'KSC LC-39A','value':'KSC LC-39A'}],
                                
                                value = 'All Sites', 
                                placeholder = 'Select a Launch Site here', searchable = True),

                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites


                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0,
                                    max=10000,
                                    step=1000,
                                    value=[min_payload, max_payload]
                                ),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# add callback decorator
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
                Input(component_id='site-dropdown', component_property='value'))

                                # Add computation to callback function and return graph
def get_graph(entered_launch_site):
    if entered_launch_site == 'All Sites':
        grouped_data = spacex_df.groupby('Launch Site')['class'].sum().reset_index()
        fig = px.pie(grouped_data, values = 'class', names = 'Launch Site', title = 'Total success launches')
        return fig
    else:
        pie_data = spacex_df[spacex_df['Launch Site'] == entered_launch_site]
        fig = px.pie(pie_data['class'], names = 'class',title = 'Distribution of success and failure for '+entered_launch_site)
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
                [Input(component_id='site-dropdown', component_property='value'), 
                Input(component_id='payload-slider', component_property="value")])

                                # Add computation to callback function and return graph
def get_graph2(entered_launch_site,payload_slider):
    low, high = payload_slider
    mask = (spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
    spacex_df2 = spacex_df[mask]
    if entered_launch_site == 'All Sites':
        fig = px.scatter(spacex_df2, x = 'Payload Mass (kg)', y = 'class', color = 'Booster Version Category', title = 'Payload mass vs Success Outcome for All Sites')
        return fig
    else:
        scatter_data = spacex_df2[spacex_df2['Launch Site'] == entered_launch_site]
        fig = px.scatter(scatter_data, x = 'Payload Mass (kg)', y = 'class', color = 'Booster Version Category', title = 'Payload mass vs Success Outcome for '+entered_launch_site)
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
