# Fiction Recommendation via Writing Style

## Introduction

Between Genre tags, Authors, and the cover of each book, Writing Style tends to go overlooked. A story might have a certain arc with its story that the genre tags might not reflect. The story's characters might interact and speak in a certain way. Certain types of characters might be written with a kind of writing flow, but further still, the way in which one writes a story at all--the grammatical phrasings--tends to be missing from most analyses.

Between Genres, you might have a snappy-sounding piece of romance, and then an equally snappy-sounding work of mystery. Likewise, you might have a dour-sounding comedy, followed by a dour-sounding adventure. Furthermore, certain authors write similarly to other authors, some following in the footsteps of Douglas Adams, or of Stephen King. And even still, authors develop and change their writing style over time. Some people like a writer's earlier works and not their later works. But Genre and Author doesn't track this writing style.

This Recommendation engine seeks to define a series of features for a collection of written works in order to relate the writing style of a given work to a number of other works, and recommend the most closely related by writing style.


## Data

The original data was organized as a .json with links to a series of epub files in many separate folders, organized by first letter, then author name, then fiction, and came in the following format from FimFiction.net's unofficial FimFarchive:

| Indecies | Column | Description                       |
|----------|:------:|----------------------------------:|
| Story ID |archive| a path to the epub for the story |
| | title | the title of the story|
| | date_published| the date the story was published. This is sometimes blank|
| | date_updated| the date of the most recent update for the story|
| | description_html| The long description in HTML format|
| | num_chapters| how many chapters are in the story|
| | num_views| how many views the story has, not including individual chapter views|
| | num_dislikes| how many dislikes the story has|
| | num_likes | how many likes the story has|
| | num_words | the total number of words across chapters|
| | rating | the likes:dislikes ratio, rounded|
| | short_description| a shorter description, usually a sentence or two|
| | has_prequel | a simple dummy column for whether the story has a prequel or not|
| | has_cover_image| a simple dummy column for whether the story has a cover image or not|
| | completion_status| Complete, Incomplete, On Hiatus, Cancelled, later became dummy columns|
| | content_rating| Everyone, Teen, Mature, later became dummy columns|
| | author_name| Author of the story, by user. Does not necessarily mean the one who wrote the story|
| | author_num_followers| The number of followers the author has|
| | total_num_views| The total number of views, including separate chapter views|
| | tag_names| a list of tags for each story, not including series tags. Later became dummy columns|


A later table provided by CSV gave me a number of users joining on a given day, which I decided is a fairly good representation of how active the site is on a given day.

| Indecies | Column | Description                       |
|----------|:------:|----------------------------------:|
|Date| Daily Users| Number of users that joined on that day|
| | Total Users| Total number of users as of that day|


In order to perform my model's calculations, I used only these Columns. The other columns will become much more important after the recommendation.

| Indecies | Column | Description                       |
|----------|:------:|----------------------------------:|
| Story ID| title| the title of the story|
| | archive| the filepath to the story's epub file|
| | word_count| the total number of words in the story|


## Methods

Much of this section will resemble the previous fanfiction suggestion engine's methods, and then add on.

### Model 1

The first model made use of a TF-IDF vectorizor, by Scikit-Learn, but because this capstone was interested in writing style, the words themselves were ignored. Instead, each piece of story text was converted into a parts-of-speech tag by using ntlk's pos_tag() function (called 'POSparser'). The idea is to strip out the meaning of a sentence in order to only focus on the basic grammatical structures.

This method converted text like so:

- *Nopony could remember a time when it had rained so hard. The normally dry and dusty plains of Appleloosa and the surrounding area were flooded with the heavy rainfall.*

to

- NNP MD VB DT NN WRB PRP VBD VBN RB JJ . DT RB JJ CC JJ NNS IN NNP CC DT VBG NN VBD VBN IN DT JJ NN .


A second similar method converted text again by simplifying down all Nouns, Adjectives, Verbs, Adverbs, and Posessives, turning the sentence into something more like:

- NN MD VB JJ NN WRB NN VB VB RB JJ . JJ RB JJ CC JJ NN IN NN CC JJ VB NN VB VB IN JJ JJ NN .


A third, hierarchical method would have converted text yet further by making each phrase into a 'Noun Phrase' or 'Verb Phrase', which can be stacked on top of each other into consecutive tuples. Doing so would have redued the number of N-grams to worry about, likely 3, while also reducing the number of features the transformer would need to deal with, and the cosine similarity function.

However, with the first and second methods, the recommender was very, very slow, only capable of dealing with up to 4-5 grams using the TF-IDF before running far too long. However, it did give results, although those results were only somewhat useful, given the few n-grams they dealt with. Unfortunately, this highlighted a certain issue when my first significant result using the second method and 1000 stories was calculated.


### Model 2

The second model dropped the use of Parts of Speech entirely, and relied instead on punctuation, stop words, and word/sentence length and diversity. Not only is this a better metric, but it's a much faster calculation than a conversion to parts of speech then TF-IDF.

For this model, a custom count vectorizer was put together using the following functions:

|Function| Role|
|--------|-----|
|sentencel_mean |The Mean sentence length |
|sentencel_std | The Standard Deviation sentence length |
|wordl_mean| The Mean word length|
|wordl_std| The Standard Deviation word length|
|lex_diversity| The lexical diversity, that is, number of unique words per (size) words|
|token_frequency| The times a token appeared per (size) words|

The lexical diversity was found as follows:

```python
    def lex_diversity(self,size):
        #Take the number of unique tokens times 'size' number of words and divide it by the number of words.
        return (len(set(self.text))*size)/len(self.text)
```

The token frequency was found as follows:

```python
    def token_frequency(self,wordy,size):
        # Find the frequency of a given word (or punctuation) per 'size' number of words
        # FreqDist is an iterable, and .N() returns all the unique items 
        return (self.fdist[wordy]*size)/self.fdist.N()
```

token frequency used an odd nltk iterable known as Fdist, which gives a count for every token, as well as a N() function, which gives the total combined count of all tokens, including punctuation.

The token frequency function was used in order to pull out frequencies for specific stop words and punctuation. Some authors use a lot of commas, some use many quotes, and others use lots of em-dashes.

Likewise, some authors use lots of 'and', and 'that' and 'which', or 'as' and 'ing' and 'maybe', and such.

Considered tokens were swear words and more 'inappropriate' language, but each story already has tags for such content, and it was not necessary. Paragraph mean and standard deviation length was considered too, but the epub reader didn't account for paragraphs as well as was necessary.

The full list of used punctuation tokens was:
- , : ; ... ! - -- ) " '

The full list of stop word tokens was:
- and but however said while as ing though with cause to this that why how if then there might maybe its/it's

### Model 3

The third model improved upon the above features by combining them both into one, focusing on a custom-made vectorizer. By combining parts of speech with stop words, certain grammatical structures become clear. This search can also be done by parts of speech to parts of speech, performing a less efficient n-gram searcher.

The 'token frequency' model became a new model in the following general format:

- (Note that ana and kata come from the greek terms referring to 'up' and 'down' respectively. 'pre' and 'post', although easier to understand, can be confused with 'POST' in requests, and I chose to make the change.)

|super_frequency| No Anterior | Negated Anterior | Full Anterior
|--------|-----|-----|-----|
|No Posterior|center_only|negate_ana_no_k|no_kata|
|Negated Posterior|negate_kata_no_a|negate_ana_kata|negate_kata|
|Full Posterior|no_ana|negate_ana|negate_none|

Depending on input, the model searches for an anterior or posterior to a given word based on the above table, and returns the frequency of that 1-3 gram.

Some examples include: 
* ("with",self.adjectives,self.adjectives,cancelvar='negk') => negate_kata where 'with' has an adjective before it and no adjective afterwards.
* (\["although","though"\],'_',self.adjectives) => no_ana where 'although' or 'though' has an adjective afterwards.
* (\["there","here"\],self.verbs) => no_kata where 'here' or 'there' with a verb beforehand.

The StyleFinder object isn't very well-compressed, and has 10 functions to deal with the separate cases, instead of 4. A further variant should be able to decrease it to 2 sub-functions and add further functionality for 4 and further grams.

An example of code would be:

```python
    def no_ana(self,word,kata,wak):
        #Takes word and kata, and returns a count of word, kata, given the story.
        counter = []
        for i in range(self.wordcount):
            try:
                if (self.uplow_switch(self.postagged[i][wak[1]],wak[1]) in word 
                and self.uplow_switch(self.postagged[i+1][wak[2]],wak[2]) in kata):
                    
                    counter.append(1)
                    
                else:
                    counter.append(0)
                    
            except IndexError:
                counter.append(0)

        return np.sum(counter)
```

Where uplow_switch is a function that determines whether to return a lowercase word or upercase depending on the 'wak'. 'wak' stands for 'word-ana-kata', which, based on the overarching super_frequency function, tells the sub-function whether it's dealing with regular words or the Part of Speech of a given word, ana-word, or kata-word.

The overarching function that uses this can perform parallelized, and a 32 CPU machine from AWS was able to run this for 2.36 billion words across 160k+ stories in approximately 8 hours.

### Recommendation by Similarity

Following this vectorization, and a normalizer function, someone can input a story in order to find the cosine similarity between it and all other stories, and return a number of style-related stories. In an ideal world, we'd have the full cosine similarity matrix already available, pull out the row, and do a simple argsort, but it would approach 40GB of data, given 160K+ items. For the purposes of this capstone, the cosine similarity matrix will be split according to a series of particular tags concerning rating.

### Further Unimplimented Functionality
(Data to be gathered in the following weeks)

Unfortunately, I did not have the option of using further API data, such as bookshelf data, in order to implement the second half of this recommendation engine.

The second half of this recommendation engine uses bookshelf data--that is, user data concerning stories they've picked up. The reason for the addition of this data is that it adds a user-user element to the item-item element already set up. Combined, the two elements can be turned into a user-user-item-item recommendation.

Bookshelves from the site this recommender is pulling story data from have a length anywhere from one to thousands of stories. In order to get a good spread of predictions, bookshelves need to be split into segments of 10. Smaller bookshelves likely belong to two sorts of users--new users and users who only add the things they absolutely feel should be added. They could also, however, belong to those who visit the site infrequently. Larger bookshelves might belong to a frequent reader, or someone who collects lots of stories they even passingly enjoy. Therefore, the splits need to be relevant to the number of stories in the bookshelf.

Each bookshelf should have 20 or more stories. Each bookshelf will be drawn from 20 times, in segments of 10. All stories will be gathered in Date-Added-To-Bookshelf order.

A bookshelf of 20 stories will be drawn as follows: \[ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 \]x2, \[ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 \]x2...

A bookshelf of 30 stories will be drawn as follows: \[ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 \], \[ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 \], \[ 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 \]...

A bookshelf of 120 stories will be drawn as follows: \[ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 \], \[ 5, 6, 7, 8, 9, 10, 11, 12, 13, 14 \]...

This is to account for both newer users and older users who favorite fewer things, while counting the bookshelves of those who favorite tons of things less.

The data will then be organized as such:

For given 10-story splits, { id#: \[ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 \] }:
Target: Story 0
Features: Story 1-9

Each story will then be split into sub-features based on the following data:
- Tags (Genre, Content Rating, Character)
- Rating Metrics (Number of Views given daily number of joined users, like/dislike ratio, likes per daily number of joined users.)
- Number of Words
- Method 3 Style-Featurization
For a total of approximately 400 sub-features per book. 400 will be target data. 3600 will be feature data.

Following the split, this data will use a non-sequential Keras neural network, which will use 3600 incoming features in order to predict 400 following features. In order to recommend, the features will be sent through a weighted cosine similarity on genre-tag split matrices in order to more quickly come with a style-accurate recommendation.

## Limitations

The Bookshelf API was unavailable to this recommender for the majority of its creation, and so this recommender could only do style recommendations by direct similarity. Although the neural network is ready for implementation, the data has yet to be gathered in full, and any results from the neural network will be skewed and incomplete.

The features of the style matrix are related to patterns seen in the text itself. In order to make a better representation of grammar as a whole, this model would need to account for many more structures in more than 2-3 grams. Despite this, many grammar structures *are* capable of being found through 2-3 grams. Further study and featurization would be required in order to capture the multitude of available grammar.

Lastly, it's very hard to tell whether recommendation will be good withough appropriate samples. The features do a good job of picking out grammatical features, but the overarching story style is much harder to capture through NLP and POS. A machine that can perform an overarching story analysis would be incredible, and is simply beyond the scope of this project. Grammar Structures on a smaller scale might be clustered around different areas, or might be stuck in dialogue instead of the story itself, and so other metrics-finding functions would be necessary in order to capture these.

## Applications (Uses)

Tracking stories by style has a great many applications in book recommendation. The use of grammatical phrasing in order to track style means that not only is a story being tracked for its writing style, but its grammatical complexity, too. With some tinkering, the featurization could change to account for national or international reading-skill rates, and given a collection of books, could recommend a story by reading level in addition to genre, content rating, and author. Some people are old enough to enjoy more mature books, but don't have the reading level required. By classifying stories by grammatical complexity, a new feature for book recommendation becomes available.

Further still, the initial purposes of this project appear to work. It's very hard to tell whether a story will be enjoyed without watching the recommendation, especially given the lack of the unimplemented functionality, but the traits that are called upon by similarity still appear in the text. One can see the flow of the passages tend to match fairly well. A high amount of quotes in a story tells us the story is dialogue-heavy. Likewise, an emphasis on gerunds in a variety of different use cases will be captured by the model. The lexical diversity will also predict a sense of how complex the story is in writing. Some of these features may need to be weighted in order to capture the most relevant parts of each similarity.

## Applications (Web)

This recommender also includes a simple tool in which someone can plug in the title for a story and a number, and will be given back that number of stories, ranked by style-similarity.
- Inputs: Story Title, Number
- Outputs: Number * Other Story Titles

