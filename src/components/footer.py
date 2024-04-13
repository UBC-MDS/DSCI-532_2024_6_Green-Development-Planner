from dash import html
from utils.utils import REPO_URL, get_repo_last_updated_time

# Dashboard footer
footer = html.P([
    "This dashboard offers a high-level overview of renewable energy metrics \
    across the globe and identifies developing countries with high potential \
    for green development.",
    html.Br(),  # Line break
    "Author: Ben Chen, Hayley Han, Ian MacCarthy, Joey Wu",
    html.Br(),  # Line break
    "Latest update/deployment: " + get_repo_last_updated_time().strftime("%B %d, %Y"),
    html.Br(),  # Line break
    html.A('GitHub URL', href=REPO_URL, target='_blank')
], className="footer")