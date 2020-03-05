import flask
import dash
import dash_html_components as html
import dash_core_components as dcc
from src.StoryRecommenderMini import recommend_stories
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
                        Fiction is simultaneously simple and difficult to recommend. When you read a good book, you can easily tell someone else that they might like it. If there's a genre you like, it's as easy as looking for a rating and through books you haven't read in order to decide what to read next. A 'prolific' reader, so to speak, may shortly run out of such books, but has other avenues of searching for them.'''),
html.Br(),
html.Div('''The difficulty arises when it comes to recommending a book via an algorithm. It's easy enough to pick the most popular books and show them off, or show off all the books related to a particular piece of fiction, but at some point, those connections might become exhausted, and the recommendation falls flat.'''),
html.Br(),
html.Div('''Certain people like certain genres, but certain genres have different styles. Kim Stanley Robinson certainly has a very different style of Science Fiction than Douglas Adams or Orson Scott Card.'''),
html.Br(),
html.Div('''But if you read all of an author's books, and like their work for their style, where do you go? Even then, some authors change their writing style over time, and a reader might enjoy their past or present style the most.'''),
html.Br(),
html.Div('''This recommender seeks to recommend by writing style instead of by genre or author or even topic, by pulling out grammatical 'tokens' and checking for a similarity between pieces of fiction.'''),
html.Br(),
html.Div('''For the purposes of this recommender I am using My Little Pony: Friendship is Magic fanfiction from the site 'FimFiction'--such fiction is both very familiar to me, and it's very easy to access both its writing and metadata. Furthermore, it has a very wide selection of authors across all different backgrounds, who have different inspirations and levels of writing skill. Lastly, it has approximately 2.5 Billion words across around 160,000 stories, which lends itself to a very good selection of sample data.
                    
                    
                    '''),
        ])
    elif tab == 'methods':
        return html.Div([
            html.H3('There are three methods, but this will focus on just one:'),
            html.Div('''
                       In a great deal of Natural Language Processing, what we care about most is the topic-oriented words. We want to find what phrases or terms are the most common so we can group passages together.'''),
html.Br(),
            html.Div('Instead, the recommender is interested in Parts of Speech and Stop Words.'), 
html.Br(),
            html.Div('Parts of Speech tags work like so:'),
            html.Div('- "Analyzer" is a Noun, so its tag is "NN"'),
            html.Div(' - "Swim" is a present verb, so its tag is "VB"'),
            html.Div(' - "Swam" is a past verb, so its tag is "VBD"'),
            html.Div(' - "The" is a determiner, so its tag is "DT"'),
            html.Div(' - etc.'),
   html.Br(),
            html.Div('Stop words are english words we usually don\'t care about, but in this case make the core of the entire recommender. Stop words include:'),
            html.Div(' - The, a, you, me, and, but, etc...'),
            html.Div(' - to, as, with, though, etc...'),
html.Br(),

            html.Div('Using Parts of Speech alone with simple n-grams creates about 30-35 choose n different combinations. Needless to say, at 3 grams, there are already 4060 different combinations to go through, and running a model on such parts of speech takes a very, very long time.'), 
html.Br(),
            html.Div('Using exclusively stop words does better, but it fails to understand that any given stop word can mean multiple pieces of grammar. For example:'),
            html.Div(' - I want to eat that brownie: This is a "to" infinitive.'),
            html.Div(' - I walk to the brownie shop: This is a prepositional "to".'),
            html.Div('This means that the recommender using only those stop words reads those pieces of grammar as the same! We don\'t want that.'),
html.Br(),
            html.Div('What this recommender does, is it takes a stop word, and looks backwards and forwards just one word in order to determine what sort of grammar a given phrase includes. For example, given the above two sentences, it would look for the following grammar tokens:'),
            html.Div(' - (anything) + "to" + (verb) and pull out the first sentence.'),
            html.Div('- (anything) + "to" + (Noun or DT) and pull out the second sentence.'),
    html.Br(),
            html.Div('Then, it records a frequency for every grammar token, and can then run a similarity function on each story, in order to determine which story shares its grammar, and thus, its writing style.'),
html.Br(),
            html.Div('This frequency finder is entirely scalable and the process is parallelizable.'),
html.Br(),
            html.Div('The similarity function is looking most for the most important grammatical features--that is, where the greatest stylistic choices appear--and so this recommender has an optional Threshold modification, which can set certain grammar feature frequencies below a certain point to 0 before running a cosine similarity.')
            
                     
                    
        ])
    
    elif tab == 'tools':
        return html.Div([
            html.Div('Currently this site only has one tool. It can take a story, and a number of recommendations, and return that number of recommendations with their similarity score.')
        
        ])

    elif tab == 'future':
        return html.Div([
            html.H3('Unimplemented Neural Network'),
            html.Div('''
                       In the near future, this recommender will plan to take in some number of  stories in order to recommend the stylistic features and tags of a future story, then run a similarity in order to find which style is most fitting. This creates a more time-conscious model, which, instead of just looking at a story and spitting out a similar one, looks for a pattern in the next story's features based on the previous story's.'''),
html.Br(),
html.Div('''The non-sequential neural network is mostly built--the biggest time-consumption has been gaining access to the bookshelf API for the MLP fanfiction site. Getting authorization had been delayed for reasons out of my control, and the API is rate limited to approximately 1 and 1/9th bookshelf per second. (1000 per 15 minutes). I can't use empty bookshelves, and I want to only use bookshelves with positive interest in the title. So far it has been almost a week, and I've gotten 50-60 thousand acceptable bookshelves, less than half of which contain 10 or more stories.

            
                     '''
                    )
            
            
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