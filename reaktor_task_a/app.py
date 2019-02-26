import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

from reaktor_task_a import data_utils


# Init global data
data, metadata = data_utils.fetch_data(10)
ds = 'co2'

data[ds].set_index(['Country Name', 'Country Code'], inplace=True)
data['pop'].set_index(['Country Name', 'Country Code'], inplace=True)


def get_countries(df):
    countries = []
    for name, code in df.index.values:
        countries.append(dict(label=name, value=code))

    return countries


# Define a plot.ly/Dash application layout

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children="CO2 Emission Explorer"),
    html.Div([
        html.Label('Select countries or groups to compare, and select additional display options using the checkboxes.'),
        dcc.Dropdown(
            id='country_selector',
            options=get_countries(data[ds]),
            value=['EUU', 'EAS', 'NAC', 'MIC', 'LDC', 'FIN'],
            multi=True
        ),
        html.P(),
        dcc.Checklist(
            id='option_checkboxes',
            options=[
                {'label': 'Show values per capita ', 'value': 'percapita_on'},
                {'label': 'Show yearly change ', 'value': 'diffs_on'},
                {'label': 'Stack selected countries or groups ', 'value': 'stacked_on'},
            ],
            values=['percapita_on'],
        ),
    ]),
    html.P(),
    dcc.Graph(
        id='co2graph',
        figure={
            'layout': {
                'title': '',
                'xaxis': {
                    'rangeslider': dict(visible=True, step=1),
                    'range': [1980, 2014]  # Set initial range
                },
                'showlegend': True,
                'margin': go.layout.Margin(t=30, b=0),
            }
        }
    ),
    html.P(children="Use the slider above to select a time range to inspect."),
    html.Div(children="Data source: The World Bank Indicators API / EN.ATM.CO2E.KT & SP.POP:TOTL")
])


# Callbacks for making the graph interactive

@app.callback(
    Output('co2graph', 'figure'),
    [Input('country_selector', 'value'),
     Input('option_checkboxes', 'values')],
    [State('co2graph', 'figure')])  # Keep state to retain time range selection.
def update_fig(selected_countries, option_checks, figure):

    title = 'CO2 Emission per year'
    ytitle = 'kilotonnes of CO2'

    series = []
    for country in selected_countries:  # TODO: Clean data columns earlier to dodge arbitrary column indices.
        country_data = data[ds].loc[(slice(None), country), data[ds].columns[2]:data[ds].columns[-6]]

        # TODO: Make options to enums?
        if 'percapita_on' in option_checks:
            country_popdata = data['pop'].loc[(slice(None), country), data['pop'].columns[2]:data['pop'].columns[-6]]
            country_data = country_data / country_popdata * 1000000  # Convert to kg
            title = 'CO2 Emissions per capita per year'
            ytitle = 'kg of CO2'

        if 'diffs_on' in option_checks:
            country_data = country_data.diff(axis=1)
            #  Pre-calculating commonly used things might be nicer in a massive production.
            #  Or, heaving some calculation to be done by the user's browser is an option too?

        # Dash should work with pandas dataframes?
        # cleaning the data to a proper time format instead of strings
        # should allow not doing something like this.
        x = [int(yearstr) for yearstr in list(country_data)]
        y = country_data.to_numpy().squeeze().tolist()

        series.append({'x': x, 'y': y, 'mode': 'lines+markers', 'name': country})
        if 'stacked_on' in option_checks:
            series[-1]['stackgroup'] = 'one'

    if 'diffs_on' in option_checks:
        title = 'Change of ' + title

    figure['layout']['title'] = title
    figure['layout']['yaxis']['title'] = ytitle

    return {
        'data': series,
        'layout': figure['layout']
    }


if __name__ == '__main__':
    app.run_server(debug=False)
