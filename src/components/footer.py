from dash import html
# from utils.utils import REPO_URL, get_repo_last_updated_time

# Dashboard footer
footer = html.P([
    "This dashboard offers a high-level overview of renewable energy metrics \
    across the globe and identifies developing countries with high potential \
    for green development.",
    html.Br(),  # Line break
    "Author: Ben Chen, Hayley Han, Ian MacCarthy, Joey Wu",
    html.Br(),  # Line break
    "Latest update/deployment: April 18, 2024",
    html.Br(),  # Line break
    html.A('GitHub URL', href="https://github.com/UBC-MDS/DSCI-532_2024_6_Green-Development-Planner", target='_blank')
], className="footer")