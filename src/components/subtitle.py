import dash_bootstrap_components as dbc

subtitle = dbc.CardBody('This dashboard assesses potential for renewable energy development projects around the world, using data from the World Bank and International Energy Agency. \
                         The map on the left shows values of one selected metric for all countries, while the charts on the right show values of each metric for one selected country.',
                    style={
                        'font-family': 'helvetica',
                        'font-size': '16px',
                        'color': '#f2fff2',
                        'background-color':'#245724',
                        'text-align': 'center',
                        'width': '101.8%',
                        'margin-left': '-11px'
                    }
)
