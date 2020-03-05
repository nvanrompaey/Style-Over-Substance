# Style Over Substance - Recommending Fiction by Writing Style

## Table of contents
- [Introduction](#Introduction)
- [Data](#Data)
- [Method](#Method)
  + [Unimplemented Functionality](#Unimplemented-Functionality)
  + [K-Means Clustering](#Clustering)
- [Results](#Results)
- [Tools](#Tools)

See 'TechnicalReadme.md' for an expanded look at each model and the acquired data.

## Introduction

Fiction is simultaneously simple and difficult to recommend. When you read a good book, you can easily tell someone else that they might like it. If there's a genre you like, it's as easy as looking for a rating and through books you haven't read in order to decide what to read next. A 'prolific' reader, so to speak, may shortly run out of such books, but has other avenues of searching for them.

The difficulty arises when it comes to recommending a book via an algorithm. It's easy enough to pick the most popular books and show them off, or show off all the books related to a particular piece of fiction, but at some point, those connections might become exhausted, and the recommendation falls flat.

Certain people like certain genres, but certain genres have different styles. Kim Stanley Robinson certainly has a very different style of Science Fiction than Douglas Adams or Orson Scott Card.

But if you read all of an author's books, and like their work for their style, where do you go? Even then, some authors change their writing style over time, and a reader might enjoy their past or present style the most.

**This recommender seeks to recommend by writing style instead of by genre or author or even topic, by pulling out grammatical 'tokens' and checking for a similarity between pieces of fiction.**

For the purposes of this recommender I will be using My Little Pony: Friendship is Magic fanfiction from the site 'FimFiction'--such fiction is both very familiar to me, and it's very easy to access both its writing and metadata. Furthermore, it has a very wide selection of authors across all different backgrounds, who have different inspirations and levels of writing skill. Lastly, it has approximately 2.5 Billion words across around 160,000 stories, which lends itself to a very good selection of sample data.

## Data

All of the metadata had already been collected by a third party, and all the stories as of December 2019 had been put into epub files and stored in a hierarchical archive--each metadata item contained an archive path to the epub in question. The Metadata is largely based on what's visible in the following image:

![Facebook Buys Ponyville](https://github.com/nvanrompaey/Style-Over-Substance/blob/master/img/FacebookBuysPonyville.png "FBP1")

In the upper left we have:
- The content rating, 'E' for Everyone, is in the corner 
- Below is the series: MLP:FIM, in purple
- To its right are the blue Genre tags
- To its right are the green Character tags

In the upper right we have:
- The number of upvotes and downvotes
- To its right is the number of comments on the story
- To its right is the number of views the story has received in total

At the bottom we have:
- The bottom left, whether the story is complete
- The bottom right, the number of words in the story in total

And the middle contains the image and description, along with each chapter.

The author is above this part of the page. Unfortunately, this doesn't tell us anything about writing style, but it does allow us to measure whether a story has the same tags as another or not, or whether the author is the same.

## Method

In a great deal of Natural Language Processing, what we care about most is the topic-oriented words. We want to find what phrases or terms are the most common so we can group passages together.

Instead, the recommender is interested in Parts of Speech and Stop Words. 

Parts of Speech tags work like so:
   - "Analyzer" is a Noun, so its tag is 'NN'
   - "Swim" is a present verb, so its tag is 'VB'
   - "Swam" is a past verb, so its tag is 'VBD'
   - "The" is a determiner, so its tag is 'DT'
   - etc.
   
Stop words are english words we usually don't care about, but in this case make the core of the entire recommender. Stop words include:
   - The, a, you, me, and, but, etc...
   - to, as, with, though, etc...


Using Parts of Speech alone with simple n-grams creates about 30-35 choose n different combinations. Needless to say, at 3 grams, there are already 4060 different combinations to go through, and running a model on such parts of speech takes a very, very long time. 

Using exclusively stop words does better, but it fails to understand that any given stop word can mean multiple pieces of grammar. For example:
- I want to eat that brownie: This is a 'to' infinitive.
- I walk to the brownie shop: This is a prepositional 'to'.
This means that the recommender using only those stop words reads those pieces of grammar as the same! We don't want that.

What this recommender does, is it takes a stop word, and looks backwards and forwards just one word in order to determine what sort of grammar a given phrase includes. For example, given the above two sentences, it would look for the following **grammar tokens**:
- **(anything) + 'to' + (verb)** and pull out the first sentence.
- **(anything) + 'to' + (Noun or DT)** and pull out the second sentence.

**Then, it records a frequency for every grammar token, and can then run a similarity function on each story, in order to determine which story shares its grammar, and thus, its writing style.**

**This frequency finder is entirely scalable and the process is parallelizable.**

See below for an example of what it might look for:

![Fiction Style Comparison](https://github.com/nvanrompaey/Style-Over-Substance/blob/master/img/Grammargraph.png)

The similarity function is looking most for the most important grammatical features--that is, where the greatest stylistic choices appear--and so this recommender has an optional Threshold modification, which can set certain grammar feature frequencies below a certain point to 0 before running a cosine similarity.

### Clustering

In order to run some exploratory tests, K-means Clustering was used to attempt to find a set of patterns. Unfortunately, the Clustering failed to find any strong patterns, and any attempts past 20 clustering nodes turned back very, very slow. This is simply because there are so, so many varied writing styles that creating clusters that don't contain a great deal of overlap is very difficult. This means the writing can't simply be classified, and needs to be ran based on an array of features instead of a single, or a few, values.

### Unimplimented Functionality

In the near future, this recommender will plan to take in some number of  stories in order to recommend the stylistic features and tags of a future story, then run a similarity in order to find which style is most fitting. This creates a more time-conscious model, which, instead of just looking at a story and spitting out a similar one, looks for a pattern in the next story's features based on the previous story's.

The non-sequential neural network is mostly built--the biggest time-consumption has been gaining access to the bookshelf API for the MLP fanfiction site. Getting authorization had been delayed for reasons out of my control, and the API is rate limited to approximately 1 and 1/9th bookshelf per second. (1000 per 15 minutes). I can't use empty bookshelves, and I want to only use bookshelves with positive interest in the title. So far it has been almost a week, and I've gotten 50-60 thousand acceptable bookshelves, less than half of which contain 10 or more stories.


## Results

This recommender, without its genre/author blocking, returns the best 'bad' results possible: It fairly consistently returns stories from the same author, and stories that are *sequels* or *prequels* of a given input story.

Given that I've been looking for a new good read from this site, I can say that the recommender has definitely given me some recommendations that I've never considered before, and am currently enjoying.

But that's not enough proof. Here's an example:
- **A passage from the input fiction**:
![Facebookfic1](https://github.com/nvanrompaey/Style-Over-Substance/blob/master/img/Facebookfic1.png)
- **A passage from the output fiction recommendation**:
![Daringfic1](https://github.com/nvanrompaey/Style-Over-Substance/blob/master/img/Daringfic1.png)

But that's just one example. How about:
- **A passage from the input fiction**:
![Facebookfic2](https://github.com/nvanrompaey/Style-Over-Substance/blob/master/img/Facebookfic2.png)
- **A passage from the output fiction recommendation**:
![Daringfic2](https://github.com/nvanrompaey/Style-Over-Substance/blob/master/img/Daringfic2.png)

And as an example of a piece of fiction that doesn't match well with these:
- **A passage from a randomly chosen piece of fiction**:
![Hourfic1](https://github.com/nvanrompaey/Style-Over-Substance/blob/master/img/HourofTwilightfic1.png)

So, it works fairly well! There's still room for improving the features by expanding and adjusting the grammar tokens, but overall, the style is what was sought, and it appears to recommend fairly well based on that grammar-like stylization.

## Tools

Below is a simple table containing each file and its purpose.

|File| Role|
|--------|-----|
|dashapp.py| A simple naive application using Dash (based on Plotly and Flask), that returns a story recommendation after an input story|
|src/DataCleaning.py|Contains a variety of functions that cleans the story metadata|
|src/Epubfinder.py|Contains a variety of functions for handling epub files. Used sparingly|
|src/FicArrayMaker.py|Application that pulls from an S3 bucket, assumes epub format, and runs each piece of text through the 'MassStylesMini and StyleFinder' classes.|
|src/MassStyles.py|Calls on the StyleFinder class a certain number of times to pull out grammar features for a series of fictions, and return an array|
|src/MassStylesMini.py|Identical to MassStyles.py, but operates on only a single fiction.|
|src/StoryRecommender.py|Creates a cosine similarity matrix across all stories for speedy recommendation (requires 40GB ram)|
|src/StoryRecommenderMini.py|Given a story, recommends a story by running a similarity function on it with all other stories.|
|src/StyleFinder.py|Class that takes text and has functions for sentence and word length metrics, lexical diversity, and grammar token frequency|
|src/SuggestionEngine.py|Depreciated and unused, contains older functions for testing and the initial 2 models.|
|src/SuperMove.py|Depreciated and unused, creates a 7GB table containing every fic, for use with the full MassStyles.py|
