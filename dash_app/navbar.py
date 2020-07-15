
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html

from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

################
# Logo
################
SGS_LOGO = "https://www.switchdoc.com/SGfulllogocolor.png"



################
# Navbar
################
def Navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("SGS Status", href="/status_page")),
            dbc.NavItem(dbc.NavLink("Valve Graphs", href="/valve_graphs")),
            dbc.NavItem(dbc.NavLink("Weather", href="/weather_page")),
            dbc.NavItem(dbc.NavLink("Hydroponics", href="/hydroponics")),
            dbc.NavItem(dbc.NavLink("Herb Garden", href="/herb_garden")),
            dbc.NavItem(dbc.NavLink("Next Events", href="/valves_scheduled")),
            dbc.NavItem(dbc.NavLink("P/V Programming", href="/p_v_programming")),
            dbc.NavItem(dbc.NavLink("Logs", href="/log_page")),
            dbc.NavItem(dbc.NavLink("Documentation", href="https://shop.switchdoc.com/collections/smart-garden-system/products/smart-garden-system-v2-raspberry-pi-based-smart-gardening-kit-no-soldering")),
                ],
                id='navbar',
                brand="SmartGardenSystem",
                brand_href="#",
                color="primary",
                dark=True,

    )
    return navbar

def Logo():
    logo = html.Img(src=SGS_LOGO, height=100, style={'margin' :'20px'})
    return logo



