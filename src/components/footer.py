from dash import html
# from utils.utils import REPO_URL, get_repo_last_updated_time

# Dashboard footer
footer = html.P([
    "Author: Ben Chen, Hayley Han, Ian MacCarthy, Joey Wu",
    html.Br(),  # Line break
    "Latest update/deployment: April 20, 2024",
    html.Br(),  # Line break
    html.A('GitHub URL', href="https://github.com/UBC-MDS/DSCI-532_2024_6_Green-Development-Planner", target='_blank')
], className="footer")