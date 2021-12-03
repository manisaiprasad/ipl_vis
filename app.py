# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
# import libs
from flask.globals import session
from werkzeug.utils import redirect
import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import sqlalchemy
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import numpy as np
import dash_bootstrap_components as dbc
from layout import html_layout


def init_dashboard(server):
    app = dash.Dash(__name__, server=server, url_base_pathname='/dashboard/',
                    external_stylesheets=[dbc.themes.BOOTSTRAP, "/static/welcome.css", "https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"])

    # creating the sqlalchemy engine connection to the database
    engine = sqlalchemy.create_engine(
        "mysql://b753801544bc29:0ad83c51@us-cdbr-east-04.cleardb.com/heroku_bbff9bdf965d108")

    #   5.1. For each team you need to give the stadium name(venue) where that team have won the maximum match?
    df = pd.read_sql("select * from matches", engine)
    teams = df['winner'].unique()
    # print(teams)
    teams_option = []
    for team in teams:
        if team is None:
            continue
        team_dict = {'label': team, 'value': team}
        teams_option.append(team_dict)

    team = 'Kolkata Knight Riders'
    sql_Statement = "select venue from matches where winner='"+team+"'"
    df_venues = pd.read_sql(sql_Statement, engine)

    # bar chart for showing data
    fig = px.bar(x=df_venues['venue'].value_counts().values, y=df_venues['venue'].value_counts().index, labels={
        "x": "Number of Matches won",
        "y": "Venue Name",
    }, title='Matches Won by '+team+' at each venue ', barmode="group")
    # to show the venue with max matches won
    dict_venues = df_venues['venue'].value_counts().to_dict()
    keys_to_values = dict(zip(dict_venues.values(), dict_venues.keys()))
    venue_name = keys_to_values[max(keys_to_values.keys())]

    # 5.2. For anyone match, you need to show the total runs scored by each batsman in that match and how they dismissed.
    match_id = '335982'
    sql_query = "select * from ballbyball where id='"+match_id+"'"
    each_match_df = pd.read_sql(sql_query, engine)
    runs = each_match_df.groupby(['batsman'])['batsman_runs'].sum()
    runs.sort_values(ascending=False, inplace=True)

    fig2 = px.bar(x=runs.index, y=runs.values, labels={
        "x": "Batsman",
        "y": "Runs",
    }, title='Total runs made by each batsman in the match RCB vs KKR', color=runs.values, barmode="group")

    # to show how each player dismissed
    players = each_match_df['batsman'].unique()
    players_dismissed_kind = {}
    for player in players:
        sql_query = "select dismissal_kind from ballbyball where id='" + \
            match_id+"' and batsman='"+player+"'"
        each_player_df = pd.read_sql(sql_query, engine)
        dismissal_kind = each_player_df['dismissal_kind'].unique()
        if len(dismissal_kind) == 1 and dismissal_kind[0] == 'not_dismissed':
            players_dismissed_kind[player] = 'not_dismissed'
        elif dismissal_kind[0] != 'not_dismissed':
            players_dismissed_kind[player] = dismissal_kind[0]
        elif dismissal_kind[1] != 'not_dismissed':
            players_dismissed_kind[player] = dismissal_kind[1]

    fig3 = go.Figure(data=[go.Table(header=dict(values=['Player', 'Dismissed Type']),
                                    cells=dict(values=[list(players_dismissed_kind.keys()), list(players_dismissed_kind.values())]))
                           ])
    # fig3.update_layout(width=1000, height=600)

    # 5.3. For anyone match, you need to show the total wicktes taken by all bowlers in that match.
    wickets = each_match_df.groupby(['bowler'])['is_wicket'].sum()
    wickets.columns = ['bowler', 'total_wickets']
    wickets.sort_values(ascending=False, inplace=True)

    labels = [X for X in wickets.keys()]

    fig4 = px.pie(values=wickets.values, names=labels, labels={
        "values": "Wickets",
        "names": "Player",
    }, title='Total wicktes taken by all bowlers in that match')

    # 5.4. For year 2019, you need to show top 10 batsman(rank them according to their total runs scored).

    year = '2019'
    sql_query = "select matches.id,matches.date, ballbyball.batsman, ballbyball.batsman_runs from matches natural join ballbyball where matches.date like '"+year+"______'  "
    year_df = pd.read_sql(sql_query, engine)
    runs = year_df.groupby(['batsman'])['batsman_runs'].sum()
    runs.columns = ['batsman', 'total_runs']
    runs.sort_values(ascending=False, inplace=True)
    runs = runs.head(10)
    fig5 = px.bar(x=runs.index, y=runs.values, labels={
        "x": "Batsman",
        "y": "Runs",
    }, title="Top 10 batsmans in the year "+year, color=runs.values, barmode="group")

    # 5.5. For year 2019, you need to show top 10 bowlers(rank them according to their total wickets taken).
    sql_query = "select matches.id,matches.date, ballbyball.bowler, ballbyball.is_wicket from matches natural join ballbyball where matches.date like '"+year+"______'  "
    year_df = pd.read_sql(sql_query, engine)
    wickets = year_df.groupby(['bowler'])['is_wicket'].sum()
    wickets.columns = ['bowler', 'total_wickets']
    wickets.sort_values(ascending=False, inplace=True)
    wickets = wickets.head(10)

    fig6 = px.bar(x=wickets.index, y=wickets.values, labels={
        "x": "bowler",
        "y": "total_wickets",
    }, title="Top 10 bowlers in the year "+year, color=wickets.values, barmode="group")

    # 5.6. You need to show that does winning toss increases the chance of victory.

    df['toss_win_game_win'] = np.where(
        (df.toss_winner == df.winner), 'Yes', 'No')
    labels = ["Yes", 'No']
    values = df['toss_win_game_win'].value_counts()
    fig7 = px.pie(values=values, names=labels, labels={
        "values": "Matches",
        "names": "Matches won when toss won",
    }, title='Winning toss implies winning matches')

    # 5.7. For any 10 batsman, you need to show, against which bowler he got out most number of time.
    ball_df = pd.read_sql("select * from ballbyball", engine)

    batsmans = ball_df['batsman'].unique()
    ten_batsmans = batsmans[:10]

    def each_batsman(batsman, id):
        #     batsman = 'RT Ponting'
        sql_query = "select * from ballbyball where batsman ='"+batsman+"'"
        batsman_df = pd.read_sql(sql_query, engine)
        temp_df = batsman_df.groupby('bowler')['is_wicket'].agg('sum').reset_index(
        ).sort_values(by='is_wicket', ascending=False).reset_index(drop=True).head(10)
        fig8 = px.bar(x=temp_df['bowler'], y=temp_df['is_wicket'], labels={
            "x": "bowler",
            "y": "total_wickets",
        }, title=batsman+" out's by each bowler", color=temp_df['is_wicket'], barmode="group")
        dict_batsman = temp_df.head(1).value_counts().to_dict()
        name, wicket = list(dict_batsman.keys())[0]
        result = batsman+" has most outs against the bowler "+name
        return html.Div(id='graph_text'+str(id), className="componet_text", children=result), dcc.Graph(id='toss-graph'+str(id), figure=fig8, style={'height': '450px'})

    home = [
        html.Div(id='graph_container', className="container", children=[
            html.H1(id='graph_text-sess', className="text-center welcome_text",
                    children=' Hello, Welcome to IPL Visualizations')
        ]),
        html.Div(id='graph_container1', className="container", children=[
            html.P(id='graph_text-sess1', className="select_componet",
                   children=' Select a team to view the number of matches won at each venue')
        ]),
        dcc.Dropdown(
            id='iplTeam-dropdown',
            options=teams_option,
            placeholder="Select a Team",
            value='Kolkata Knight Riders'
        ),
        html.Div(id='graph_text', className="componet_text", children=team +
                 " won max number of matches at "+venue_name),
        dcc.Graph(
            className="component",
            id='venue-graph',
            style={'height': '65vh'}
        ),
        html.P(id='graph_text1', className="desc_text",
               children="The Bar Chart shows the number of matches won by a team at each venue. On selecting a team from above drop down, we will get the venue name where the team won maximum number of matches with a bar chart showing all venues where team played."),
        html.Div(
            id='grun_text', className="componet_text", children="Total runs made by each batsman in the match RCB vs KKR'"),

        dcc.Graph(
            className="component",
            id='matche-graph',
            figure=fig2,
            style={'height': '65vh'}
        ),
        html.P(id='graph_text2', className="desc_text",
               children="The Bar Chart shows the total runs scored by each batsman in the match RCB vs KKR. BB McCullum is the top scorer in the match with 158 runs. "),
        html.Div(
            id='gtable_text', className="componet_text", children="Dismissal kind of each batsman in the match RCB vs KKR"),
        dcc.Graph(
            className="component",
            id='matche-table',
            figure=fig3,
            style={'height': '65vh'}
        ),
        html.P(id='graph_text3', className="desc_text",
               children="The Table shows the dismissal kind of each batsman in the match RCB vs KKR. BB McCullum, Mohammand Hafeez and P Kumar is the not dismissed batsmans in the match."),
        html.Div(
            id='gb_text', className="componet_text", children="Total wicktes taken by all bowlers in the match RCB vs KKR"),
        dcc.Graph(
            className="component",
            id='bowler-graph',
            figure=fig4,
            style={'height': '65vh'}
        ),
        html.P(id='graph_text4', className="desc_text",
               children="The Pie Chart shows the total wicktes taken by each bowler in the match RCB vs KKR. SC Ganguly and AB Agarkar are the top bowlers in the match with 3 wickets."),
        html.H3(
            id='text10', className="h3_head-p", children="Top 10 players in the year 2019"),

        dbc.Row([dbc.Col([html.Div(
            id='gbat_text', className="componet_text", children="Top 10 batsmans in the year 2019"),
            dcc.Graph(
            className="component",
            id='batyear-graph',
            figure=fig5,
            style={'height': '450px'}
        ),
            html.P(id='graph_text5', className="desc_text",
                   children="The Bar Chart shows the total runs scored by each batsman in the year 2019 and rank's them according to their total runs scored . DA Warner is the top scorer in the year with 692 runs."),
        ],),
            dbc.Col([html.Div(
                id='gbowl_text', className="componet_text", children="Top 10 bowlers in the year 2019"),
                dcc.Graph(
                className="component",
                id='ballyear-graph',
                figure=fig6,
                style={'height': '450px'}
            ),
                html.P(id='graph_text6', className="desc_text",
                       children="The Bar Chart shows the total wicktes taken by each bowler in the year 2019 and rank's them according to their total wicktes scored. K Rabada is the top bowler in the year with 28 wickets."),

            ],)], justify="around"),
        # html.Div(
        #     id='gbat_text', className="componet_text", children="Top 10 batsmans in the year 2019"),
        # dcc.Graph(
        #     className="component",
        #     id='batyear-graph',
        #     figure=fig5,
        #     style={'height': '65vh'}
        # ),
        # html.Div(
        #     id='gbowl_text', className="componet_text", children="Top 10 bowlers in the year 2019"),
        # dcc.Graph(
        #     className="component",
        #     id='ballyear-graph',
        #     figure=fig6,
        #     style={'height': '65vh'}
        # ),
        html.Div(
            id='gwin_text', className="componet_text", children="Winning toss implies winning matches"),
        dcc.Graph(
            className="component",
            id='toss-graph',
            figure=fig7,
            style={'height': '65vh'}
        ),
        html.P(id='graph_text7', className="desc_text",
               children="The Pie Chart shows does winning toss increases the chance of victory?. Yes, it does. by a little. In the pie chart we clearly see the chances of winning toss increasing the chance of victory is 51.2%."),
        html.H3(
            id='text8', className="h3_head", children="The number of out's for ten batsmen against each bowler"),
        html.P(id='graph_text8', className="desc_text",
               children="For 10 batsman, we show against which bowler he got out most number of time. Each graph shows the number of out's for a batsman against each bowler and against who got out most number of time."),
        dbc.Row([dbc.Col([each_batsman(ten_batsmans[0], 10)[0], each_batsman(ten_batsmans[0], 10)[1]],),
                 dbc.Col([each_batsman(ten_batsmans[1], 11)[0], each_batsman(ten_batsmans[1], 11)[1]],)], justify="around"),
        dbc.Row([dbc.Col([each_batsman(ten_batsmans[2], 12)[0], each_batsman(ten_batsmans[2], 12)[1]],),
                 dbc.Col([each_batsman(ten_batsmans[3], 13)[0], each_batsman(ten_batsmans[3], 13)[1]],)], justify="around"),
        dbc.Row([dbc.Col([each_batsman(ten_batsmans[4], 14)[0], each_batsman(ten_batsmans[4], 14)[1]],),
                 dbc.Col([each_batsman(ten_batsmans[5], 15)[0], each_batsman(ten_batsmans[5], 15)[1]],)], justify="around"),
        dbc.Row([dbc.Col([each_batsman(ten_batsmans[6], 16)[0], each_batsman(ten_batsmans[6], 16)[1]],),
                 dbc.Col([each_batsman(ten_batsmans[7], 17)[0], each_batsman(ten_batsmans[7], 17)[1]],)], justify="around"),
        dbc.Row([dbc.Col([each_batsman(ten_batsmans[8], 18)[0], each_batsman(ten_batsmans[8], 18)[1]],),
                 dbc.Col([each_batsman(ten_batsmans[9], 19)[0], each_batsman(ten_batsmans[9], 19)[1]],)], justify="around"), ]

    # each_batsman(ten_batsmans[0], 10)[0],
    # each_batsman(ten_batsmans[0], 10)[1],
    # each_batsman(ten_batsmans[1], 11)[0],
    # each_batsman(ten_batsmans[1], 11)[1],

    # each_batsman(ten_batsmans[2], 12)[0],
    # each_batsman(ten_batsmans[2], 12)[1],

    # each_batsman(ten_batsmans[3], 13)[0],
    # each_batsman(ten_batsmans[3], 13)[1],

    # each_batsman(ten_batsmans[4], 14)[0],
    # each_batsman(ten_batsmans[4], 14)[1],

    # each_batsman(ten_batsmans[5], 15)[0],
    # each_batsman(ten_batsmans[5], 15)[1],

    # each_batsman(ten_batsmans[6], 16)[0],
    # each_batsman(ten_batsmans[6], 16)[1],

    # each_batsman(ten_batsmans[7], 17)[0],
    # each_batsman(ten_batsmans[7], 17)[1],

    # each_batsman(ten_batsmans[8], 18)[0],
    # each_batsman(ten_batsmans[8], 18)[1],

    # each_batsman(ten_batsmans[9], 19)[0],
    # each_batsman(ten_batsmans[9], 19)[1]]

    content = html.Div(id="page-content", children=home)

    app.index_string = html_layout
    app.layout = html.Div([dcc.Location(id="url"), content])

    @ app.callback(
        Output('venue-graph', 'figure'),
        Output('graph_text', 'children'),
        Output('graph_text-sess', 'children'),
        Input('iplTeam-dropdown', 'value')
    )
    def update_figure(team):
        sql_Statement = "select venue from matches where winner='"+team+"'"
        df_venues = pd.read_sql(sql_Statement, engine)
        fig = px.bar(x=df_venues['venue'].value_counts().values, y=df_venues['venue'].value_counts().index, labels={
            "x": "Number of Matches won",
            "y": "Venue Name",
        }, title='Matches Won by '+team+' at each venue ', color=df_venues['venue'].value_counts(), barmode="group")
        dict_venues = df_venues['venue'].value_counts().to_dict()
        keys_to_values = dict(zip(dict_venues.values(), dict_venues.keys()))
        venue_name = keys_to_values[max(keys_to_values.keys())]
        try:
            user_name = session.get('user_name', None)
            print("UserName:", user_name)
        except:
            user_name = None
        return [fig, team+' won max number of matches at '+venue_name, "Hello "+str(user_name)+", Welcome to IPL Visualizations"]

    return app
