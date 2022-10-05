import dash
from dash import html as dhtml
from dash import dcc
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output

from django_plotly_dash import DjangoDash

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

data = pd.read_csv(str(BASE_DIR) + "/pages/test_data/soccer_data.csv")
data.Date = pd.to_datetime(data.Date)
data.sort_values("Date", inplace=True)

ext_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

stat_types = [
    "Performance Duration [min]",
    "Total Distance [m]",
    "Walk Distance [m]",
    "Jog Distance [m]",
    "Run Distance [m]",
    "Sprint Distance [m]",
    "Hard Running [m]",
    "Hard Running Efforts",
    "Work Rate [m/min]",
    "Top Speed [m/s]",
    "Intensity",
    "Load 2D",
    "Load 3D",
    "ACWR_AVG",
]

app = DjangoDash("ACWR_App", external_stylesheets=ext_stylesheets)
app.title = "Griz Soccer Analytics: Understand Your Data!"

app.layout = dhtml.Div(
    children=[
        dhtml.Div(
            children=[
                dhtml.P(children="⚽", className="header-emoji"),
                dhtml.H1(children="Griz Soccer Analytics", className="header-title"),
                dhtml.P(
                    children="Analyze the ACWR data for your team",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        dhtml.Div(
            children=[
                dhtml.Div(
                    children=[
                        dhtml.Div(children="Player", className="menu-title"),
                        dcc.Dropdown(
                            id="player-filter",
                            options=[
                                {"label": Name, "value": Name}
                                for Name in np.sort(data.Name.unique())
                            ],
                            value="Allie Larsen",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                # dhtml.Div(
                #     children=[
                #         dhtml.Div(children="Stat", className="menu-title"),
                #         dcc.Dropdown(
                #             id="type-filter",
                #             options=[
                #                 {"label": stat_type, "value": stat_type}
                #                 for stat_type in stat_types
                #             ],
                #             value="ACWR_AVG",
                #             clearable=False,
                #             searchable=False,
                #             className="dropdown",
                #         ),
                #     ],
                # ),
                dhtml.Div(
                    children=[
                        dhtml.Div(children="Date Range", className="menu-title"),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=data.Date.min().date(),
                            max_date_allowed=data.Date.max().date(),
                            start_date=data.Date.min().date(),
                            end_date=data.Date.max().date(),
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        dhtml.Div(
            children=[
                dhtml.Div(
                    children=dcc.Graph(
                        id="acwr-chart",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)


@app.callback(
    [Output("acwr-chart", "figure")],
    [
        Input("player-filter", "value"),
        # Input("type-filter", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
    ],
)
def update_charts(Name, start_date, end_date):
    mask = (data.Name == Name) & (data.Date >= start_date) & (data.Date <= end_date)
    filtered_data = data.loc[mask, :]
    acwr_char_figure = [
        {
            "data": [
                {
                    "x": filtered_data.Date.values,
                    "y": filtered_data["ACWR_AVG"].values,
                    "type": "lines",
                },
            ],
            "layout": {
                "title": {
                    "text": "Average ACWR",
                    "x": 0.05,
                    "xanchor": "left",
                },
                "xaxis": {"fixedrange": True},
                "yaxis": {"fixedrange": True},
                "colorway": ["#17B897"],
            },
        }
    ]
    return acwr_char_figure


if __name__ == "__main__":
    app.run_server(debug=True)
