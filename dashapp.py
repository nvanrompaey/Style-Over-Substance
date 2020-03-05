import flask
import dash
import dash_html_components as html
import dash_core_components as dcc
from StoryRecommenderMini import recommend_stories
from dash.dependencies import Input, Output


# Presentation Application only. Not for optimal use.
server = flask.Flask(__name__)

colors = {
            'background':'#264d73',
            'maintext':'#d9d9d9'
         }

exs = ['Fictest.css']

app = dash.Dash(__name__,external_stylesheets = exs)






app.layout = html.Div([html.H1('Recommending Fiction via Writing Style'),
                       html.Br(),
                       html.Br(),
                       dcc.Input(id='storyinput', value='storytitle', type='text'),
                       html.Button('Submit Story', id='button'),
                       dcc.Slider(
                                    id = 'quantityinput',
                                    min=1,
                                    max=5,
                                    marks={i: '{} Recommendations'.format(i) for i in range(6)},
                                    value=5,
                                ),  
                       html.Div(id='recommendations'),
                       html.Br(),
                       html.Br(),
                       
                    dcc.Tabs(id="tabs", value='ovv', children=[
                        dcc.Tab(label='Overview', value='ovv'),
                        dcc.Tab(label='Methods', value='methods'),
                        dcc.Tab(label='Tools',value='tools'),
                        dcc.Tab(label='Future Goals',value='future'),

                    ]),
    html.Div(id='tabs-content'),

])

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'ovv':
        return html.Div([
            html.H3('Why Writing Style?'),
            html.Div('''
                        Genre, Author, and Themes offer up an excellent way to search for stories: Many people love mysteries, and find it easy to search for a mystery. If someone likes a particular author, it's easy to look up books the author has already written. If someone has particular themes in mind, there are often ways to find a story tagged with those particular ideas, like a gothic horror vs a sci-fi horror piece.
                    
                    
                    '''),
        ])
    elif tab == 'methods':
        return html.Div([
            html.H3('This is where we talk about the specific ways of going about the stylization.')
        ])
    
    elif tab == 'tools':
        return html.Div([
            html.H3('This is a description of the tools below the page.')
        
        ])

    elif tab == 'future':
        return html.Div([
            html.H3('And here be my future goals.')
            
            
        ])
    
@app.callback(
    Output(component_id='recommendations', component_property='children'),
    [Input(component_id='button',component_property='n_clicks')],
    [dash.dependencies.State(component_id='storyinput', component_property='value'),
     dash.dependencies.State(component_id='quantityinput',component_property='value')]
)

def update_output_div(n_clicks,value,value2):
    return recommend_stories(value,value2)






if __name__ == '__main__':
    app.run_server(debug=True)