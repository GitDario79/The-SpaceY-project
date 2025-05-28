# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# TASK 1: Prepare dropdown options
# Get unique launch sites for the dropdown
launch_sites = spacex_df['Launch Site'].unique()
site_options = [{'label': 'All Sites', 'value': 'ALL'}]
for site in launch_sites:
    site_options.append({'label': site, 'value': site})

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown', # ID for the dropdown
                                             options=site_options, # Options generated above
                                             value='ALL', # Default selected value
                                             placeholder="Select a Launch Site here", # Placeholder text
                                             searchable=True # Allows users to search sites
                                             ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0,
                                                max=10000,
                                                step=1000,
                                                marks={0: '0 kg',
                                                    2500: '2500 kg',
                                                    5000: '5000 kg',
                                                    7500: '7500 kg',
                                                    10000: '10000 kg'},
                                                value=[min_payload, max_payload] # Uses your calculated min_payload and max_payload
                                                ),
                                html.Br(), 

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        # For 'ALL' sites, create a pie chart showing total successful launches by site.
        # The 'class' column = 1 for success, 0 for failure.
        # px.pie will sum 'class' for each 'Launch Site'.
        fig = px.pie(spacex_df,
                     values='class',  # Sum of 'class' (1s for successes) for each site
                     names='Launch Site',
                     title='Total Successful Launches by Site')
        return fig
    else:
        # For a specific site, filter the DataFrame.
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        # Create a pie chart showing success (1) vs. failure (0) counts for the site.
        # px.pie will count occurrences of each unique value in 'class' for the filtered data.
        fig = px.pie(filtered_df,
                     names='class',  # Slices will be named '0' and '1' based on 'class' values
                     title=f'Total Launch Outcomes for Site: {entered_site}')
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_chart(entered_site, payload_range):
    # payload_range is a list e.g., [min_selected_payload, max_selected_payload]
    low, high = payload_range
    
    # Filter DataFrame based on selected payload range
    # Create a mask for rows where 'Payload Mass (kg)' is within the selected range
    payload_mask = (spacex_df['Payload Mass (kg)'] >= low) & \
                   (spacex_df['Payload Mass (kg)'] <= high)
    filtered_df_payload = spacex_df[payload_mask]

    if entered_site == 'ALL':
        # If ALL sites are selected, use the payload-filtered data for all sites
        fig = px.scatter(filtered_df_payload,
                         x='Payload Mass (kg)',
                         y='class',
                         color='Booster Version Category',
                         title=f'Payload vs. Launch Outcome for All Sites (Payload: {low:,}-{high:,} kg)')
    else:
        # If a specific site is selected, further filter the payload-filtered data for that site
        filtered_df_site = filtered_df_payload[filtered_df_payload['Launch Site'] == entered_site]
        fig = px.scatter(filtered_df_site,
                         x='Payload Mass (kg)',
                         y='class',
                         color='Booster Version Category',
                         title=f'Payload vs. Launch Outcome for site {entered_site} (Payload: {low:,}-{high:,} kg)')
    
    return fig
# Run the app
if __name__ == '__main__':
    app.run(debug=True) # Use app.run and enable debug mode