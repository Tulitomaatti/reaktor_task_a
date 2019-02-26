import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from reaktor_task_a import data_utils

# Init global data
data, metadata = data_utils.fetch_data(10)
ds = 'co2'

data[ds].set_index(['Country Name', 'Country Code'], inplace=True)
data['pop'].set_index(['Country Name', 'Country Code'], inplace=True)

def get_countries(df):
    countries = []
    for name, code in df.index.values:
        countries.append( dict(label=name, value=code) )

    return countries

# Define a plotly/Dash application layout

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children="CO2 Emission Explorer"),
    html.Div(children=''''Lorem ipsum dolor sit amet climate change is coming.'''),
    html.Div([
        html.Label('Select countries to compare.'),
        dcc.Dropdown(
            id='country_selector',
            options= get_countries(data[ds]),
            value=['WLD', 'FIN'],
            multi=True
        ),
        dcc.Checklist(
            id='option_checkboxes',
            options=[
                {'label': 'Show values per capita', 'value':'percapita_on'},
                {'label': 'Show yearly change', 'value':'diffs_on' },
                {'label': 'Stack selected countries', 'value':'stacked_on'}
            ],
            values=['percapita_on'],
        ),
    ]),

    dcc.Graph(
        id='co2graph',
        figure={
            'layout': {
                'title': 'Graph title placeholder',
                'xaxis': {
                    'rangeslider': dict(visible=True),
                    'range': [1990, 2018] # Set initial range
                },
                'yaxis': {
                    'label': 'CO2 Emissions (kg)'
                },
                'showlegend': True
            }
        }
    )
])


# Callbacks for making the graph interactive

@app.callback(
    Output('co2graph', 'figure'),
    [Input('country_selector', 'value'),
     Input('option_checkboxes', 'values'),
     ])
def update_fig(selected_countries, option_checks):
    series = []

    print option_checks
    for country in selected_countries: # TODO: Clean data columns earlier to dodge arbitrary column indices.
        country_data = data[ds].loc[(slice(None), country), data[ds].columns[2]:data[ds].columns[-2]]

        # TODO: Make options to enums?
        if 'percapita_on' in option_checks:
            country_popdata = data['pop'].loc[(slice(None), country), data['pop'].columns[2]:data['pop'].columns[-2]]
            country_data = country_data / country_popdata

        if 'diffs_on' in option_checks:
            country_data = country_data.diff(axis=1)
            # Precalculating commonly used things might be nicer in a massive production.
            # Or, heaving some calculation to be done by the user's browser is an option too?

        x = [int(yearstr) for yearstr in list(country_data)]
        y = country_data.to_numpy().squeeze().tolist()

        series.append({'x': x, 'y': y, 'type': 'line', 'name': country})


    return {
        'data': series,
        'layout': {
            'title': 'Graph title placeholder',
            'xaxis': {
                'rangeslider': dict(visible=True),
                #'range': [1990, 2018]  # Set initial range
            },
            'yaxis': {
                'label': 'CO2 Emissions (kg)'
            },
            'showlegend': True
        }
    }


if __name__ == '__main__':
    app.run_server(debug=True)