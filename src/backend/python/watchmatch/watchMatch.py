import math
import pandas as pd

from sklearn.metrics import jaccard_score
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

from flask import Flask

try:
    df = pd.read_csv('./src/backend/ressources/watches.csv')
except:
    df = pd.DataFrame(columns = ["brand","family","reference","name","movement","produced","caseMaterial",
                                    "caseGlass","caseBack","caseShape","caseDiameter","caseHeight","caseLugWidth","dialColor",
                                    "dialMaterial","dialIndexes","dialHands", "image", "price"])

pd.set_option('display.max_colwidth', 240)

def watch_match_cosine(given_watch, filters):
    # Combine all attributes into a single string per watch
    df['watch_attributes'] = df.apply(lambda x: ', '.join(str(val) for val in x), axis=1)

    # Extract the attribute strings from the DataFrame
    watch_attributes = df['watch_attributes'].tolist()

    # Initialize CountVectorizer
    vectorizer = CountVectorizer(token_pattern=r"(?u)\b\w+\b")

    # Fit and transform the data
    vectorized_data = vectorizer.fit_transform(watch_attributes)

    # Vectorize the given watch
    vectorized_given_watch = vectorizer.transform([given_watch])

    # Calculate cosine similarity between the given watch and all watches in the dataset
    similarities = cosine_similarity(vectorized_given_watch, vectorized_data)

    # Find the indices of the closest matches
    closest_match_indices = similarities.argsort()[0][::-1]

    # Keep track of included brands
    included_brands = set()

    # Get the details of the closest matches (one per brand)
    results = []
    for idx in closest_match_indices:
        watch = df.iloc[idx]
        brand = watch['brand']
        price = watch['price']
        minPrice = 0
        if filters["minPrice"] != "":
            minPrice = float(filters["minPrice"])
        maxPrice = math.inf
        if filters["maxPrice"] != "":
            maxPrice = float(filters["maxPrice"])
        if (brand not in included_brands 
            and brand not in filters["excludedBrands"] 
            and (price is not None and float(price) > minPrice) 
            and (price is not None and float(price) < maxPrice) 
            and watch[['caseMaterial']] not in filters["excludedCaseMaterials"] 
            and watch[['dialColor']] not in filters["excludedDialColors"]):
            included_brands.add(brand)
            results.append(watch[['brand', 'family', 'reference', 'name', 'price', 'image']])
        if len(results) >= 11:
            break

    print("\n")
    print("One Watch Per Brand (First 10 Matches):")
    for i in range(len(results)):
        if i != 0:
            print(results[i])
            print("\n")

def watch_match_jaccard(givenWatch):
    # Combine descriptors into a single column
    df['CombinedDescriptors'] = df.apply(lambda row: [str(row[col]) for col in df.columns], axis=1)

    # Convert descriptors to binary indicators
    mlb = MultiLabelBinarizer()
    descriptor_matrix = mlb.fit_transform(df['CombinedDescriptors'])
    given_watch_binary = mlb.transform([list(givenWatch)])  
   
    # Define a custom Jaccard similarity function
    
    def jaccard_similarity(a, b):
        intersection = sum(min(x, y) for x, y in zip(a, b))
        union = sum(max(x, y) for x, y in zip(a, b))
        return intersection / union if union > 0 else 0.0

    # Calculate Jaccard similarity between the given watch and each row
    similarities = [jaccard_similarity(given_watch_binary[0], row) for row in descriptor_matrix]

    # Find the index of the row with the highest similarity
    best_match_index = similarities.index(max(similarities))

    # Get the best matching row
    best_match_row = df.loc[best_match_index]

    print("Best Matching Row:")
    print(best_match_row)

if __name__ == "__main__":
    given_watch = "a. lange & söhne,1815,730.032(aka: 730032f, 730032),1815 tourbillon pink gold,a. lange & söhne caliber l102.1hours, minutes, small seconds | tourbillon escapement,2014,pink gold,sapphire,open,,39.50 mm,11.10 mm,20.00 mm,silver,silver,arabic numerals,alpha,https://cdn.watchbase.com/watch/lg/a-lange-sohne/1815/730-032-9f.jpg,160800.0,no"
    filters = {"excludedBrands":[],"minPrice":"","maxPrice":"1500","excludedCaseMaterials":[],"excludedDialColors":[]}
    watch_match_cosine(given_watch, filters)
    

