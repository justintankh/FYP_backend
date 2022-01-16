from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from bs4 import BeautifulSoup
import requests
from google_images_search import GoogleImagesSearch
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
import string
import ast
import re
import unidecode
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
recommender_dir = './api/recommender_files/'


def gis_url(query):
    # API key and CX
    gis = GoogleImagesSearch(
        'AIzaSyDavRxKC9Jcs6YRYWE0nJTe1ylyrlrtfY0', '47d748b4b3354fccc')
    gis.search(search_params={'q': query, 'num': 1})
    return gis.results()[0].url


def product_information_via_barcode(barcode):
    # Loading of ingredients contained in DB
    cleaned_recipe_df = pd.read_csv(
        recommender_dir + "test_all_recipe_full.csv")
    cleaned_recipe_df['ingredients_parsed'] = cleaned_recipe_df['ingredients_parsed'].apply(
        lambda x: str(x))
    all_ingredients = cleaned_recipe_df.ingredients_parsed.tolist()
    all_ingredients = ' '.join(all_ingredients)
    all_ingredients = list(set(all_ingredients.split()))

    URL = "https://world.openfoodfacts.org/product/{}".format(barcode)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    # If barcodes does not exist
    if (soup.find("h1", property="food:name") == None):
        print("\x1b[31m\"Barcode '{}' not found.\"\x1b[0m".format(barcode))
        return False, '', ''

    # Parsing
    title = soup.find("h1", property="food:name").text

    # Cases without category, fallback on title as category
    categories_list = [x.strip() for x in title.replace(
        '-', ' ').replace(',', ' ').split(' ')]

    if soup.find(id="field_categories_value") != None:
        categories_scrapped = soup.find(id="field_categories_value").text
        categories_list = [x.strip() for x in categories_scrapped.split(',')]

    print("\x1b[31m\"title:\"\x1b[0m", title)
    print("\x1b[31m\"categories_list:\"\x1b[0m", categories_list)

    # test ingredients
    categories_string = ' '.join(categories_list)
    print("\x1b[31m\"categories_string:\"\x1b[0m", categories_string)
    categories_string = remove_sub_dups(categories_string)
    print("\x1b[31m\"remove_sub_dups:\"\x1b[0m", categories_string)

    try:
        ingredients_parsed = ingredient_parser(categories_string)
    except:
        ingredients_parsed = ingredient_parser([categories_string])

    ingredients_parsed = list(set(ingredients_parsed.split()))
    print("\x1b[31m\"ingredients_parsed:\"\x1b[0m", ingredients_parsed)

    # check for food group to match in ingredient database
    category_parsed = [x for x in ingredients_parsed if x in all_ingredients]
    print("\x1b[31m\"category_parsed:\"\x1b[0m", category_parsed)

    # Retrieve recommendation & results
    recs, transform_results = RecSys(' '.join(category_parsed))
    (categories, categories_score) = zip(*transform_results.items())
    categories = ','.join(categories)
    categories_score = ','.join(str(e) for e in categories_score)

    return title, categories, categories_score

###################################################
############## Recommender functions ##############
###################################################


def ingredient_parser(ingreds):
    measures = ['teaspoon', 't', 'tsp.', 'tablespoon', 'T', 'tbl.', 'tb', 'tbsp.', 'fluid ounce', 'fl oz', 'gill', 'cup',
                'c', 'pint', 'p', 'pt', 'fl pt', 'quart', 'q', 'qt', 'fl qt', 'gallon', 'g', 'gal', 'ml', 'milliliter',
                'millilitre', 'cc', 'mL', 'l', 'liter', 'litre', 'L', 'dl', 'deciliter', 'decilitre', 'dL', 'bulb', 'level',
                'heaped', 'rounded', 'whole', 'pinch', 'medium', 'slice', 'pound', 'lb', '#', 'ounce', 'oz', 'mg',
                'milligram', 'milligramme', 'g', 'gram', 'gramme', 'kg', 'kilogram', 'kilogramme', 'x', 'of', 'mm',
                'millimetre', 'millimeter', 'cm', 'centimeter', 'centimetre', 'm', 'meter', 'metre', 'inch', 'in',
                'milli', 'centi', 'deci', 'hecto', 'kilo']

    list_of_stop_words = list(stopwords.words('english'))
    measures = measures + list_of_stop_words

    if isinstance(ingreds, list):
        ingredients = ingreds
    else:
        ingredients = ast.literal_eval(ingreds)

    translator = str.maketrans('', '', string.punctuation)
    lemmatizer = WordNetLemmatizer()
    ingred_list = []
    for i in ingredients:
        i.translate(translator)
        items = re.split(' |-', i)
        items = [word.lower() for word in items]
        # remove accents
        # ''.join((c for c in unicodedata.normalize('NFD', items) if unicodedata.category(c) != 'Mn'))
        items = [unidecode.unidecode(word) for word in items]
        # Lemmatize words so we can compare words to measuring words
        items = [lemmatizer.lemmatize(word) for word in items]
        # Gets rid of measuring words/phrases, e.g. heaped teaspoon
        items = [word for word in items if word not in measures]
        # Get rid of common easy words
        items = [re.sub("[^0-9a-zA-Z]+", "", word) for word in items]
        items = [word for word in items if word.isalpha()]

        if items:
            ingred_list.append(' '.join(items))
    ingred_list = " ".join(ingred_list)
    return ingred_list

# Top-N recomendations order by score


def get_recommendations(N, scores):
    # load in recipe dataset
    df_recipes = pd.read_csv(recommender_dir + "test_all_recipe_full.csv")
    # order the scores with and filter to get the highest N scores
    top = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:N]
    # create dataframe to load in recommendations
    recommendation = pd.DataFrame(
        columns=['recipe', 'ingredients', 'score', 'url'])
    count = 0
    for i in top:
        recommendation.at[count, 'recipe'] = title_parser(
            df_recipes['recipe_name'][i])
        recommendation.at[count, 'ingredients'] = ingredient_parser_final(
            df_recipes['ingredients'][i])
        recommendation.at[count, 'url'] = df_recipes['recipe_urls'][i]
        recommendation.at[count, 'score'] = "{:.3f}".format(float(scores[i]))
        count += 1
    return recommendation

# neaten the ingredients being outputted


def ingredient_parser_final(ingredient):
    if isinstance(ingredient, list):
        ingredients = ingredient
    else:
        ingredients = ast.literal_eval(ingredient)

    ingredients = ','.join(ingredients)
    ingredients = unidecode.unidecode(ingredients)
    return ingredients


def title_parser(title):
    title = unidecode.unidecode(title)
    return title


def RecSys(ingredients, N=5):

    # load in tdidf model and encodings
    with open(recommender_dir + "tfidf1_encodings.pkl", 'rb') as f:
        tfidf_encodings = pickle.load(f)

    with open(recommender_dir + "tfidf1.pkl", "rb") as f:
        tfidf = pickle.load(f)

    # parse the ingredients using my ingredient_parser
    try:
        ingredients_parsed = ingredient_parser(ingredients)
    except:
        ingredients_parsed = ingredient_parser([ingredients])

    # use our pretrained tfidf model to encode our input ingredients
    ingredients_tfidf = tfidf.transform([ingredients_parsed])
    ingredients_parsed = ingredients_parsed.split()
#     # Dictionary of ingredient : transform_score
    print('len(Key):', len(ingredients_parsed),
          ' key(Value):', len(ingredients_tfidf.data))
    transform_results = {ingredients_parsed[i]: ingredients_tfidf.data[i] for i in range(
        len(ingredients_parsed))}

    # calculate cosine similarity between actual recipe ingreds and test ingreds
    cos_sim = map(lambda x: cosine_similarity(
        ingredients_tfidf, x), tfidf_encodings)
    scores = list(cos_sim)

    # Filter top N recommendations
    recommendations = get_recommendations(N, scores)
    return recommendations, transform_results


def remove_sub_dups(string):
    temp = []
    string = sorted(string.split(), key=len)
    string_ingredients = ' '.join(string)
    for item in string:
        if item in string_ingredients:
            string_ingredients = string_ingredients.replace(item, '')
            temp.append(item)
    return ' '.join(temp)
