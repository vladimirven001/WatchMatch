import time
import pandas as pd
from sklearn.metrics import jaccard_score
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

try:
    df = pd.read_csv('watches.csv')
except:
    df = pd.DataFrame(columns = ["brand","family","reference","name","movement","produced","caseMaterial",
                                    "caseGlass","caseBack","caseShape","caseDiameter","caseHeight","caseLugWidth","dialColor",
                                    "dialMaterial","dialIndexes","dialHands"])
    
# def watch_match(givenWatch):
#     # Combine descriptors into a single column
#     df['CombinedDescriptors'] = df.apply(lambda row: [str(row[col]) for col in df.columns], axis=1)

#     # Convert descriptors to binary indicators
#     mlb = MultiLabelBinarizer()
#     descriptor_matrix = mlb.fit_transform(df['CombinedDescriptors'])
#     print(descriptor_matrix)

#     # Convert the given watch descriptors to binary
#     given_watch_binary = mlb.transform([list(givenWatch)])
#     print(given_watch_binary)

#     # Calculate Jaccard similarity between the given watch and each row
#     similarities = jaccard_score(given_watch_binary, descriptor_matrix, average=None)

#     # Find the index of the row with the highest similarity
#     best_match_index = similarities.argmax()

#     # Get the best matching row
#     best_match_row = df.loc[best_match_index]

#     print("Best Matching Row:")
#     print(best_match_row)

def watch_match_cosine(given_watch):
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
        if brand not in included_brands:
            print(brand)
            included_brands.add(brand)
            results.append(watch[['brand', 'family', 'reference', 'name']])
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
    given_watch = "a. lange & söhne,1815,236.049,1815 200th anniversary f. a. lange,a. lange & söhne caliber l051.1hours, minutes, small seconds,2015,platinum,sapphire,open,round,40.00 mm,8.80 mm,,black,silver,arabic numerals,alpha,yes, 200 units"
    # watch_match_jaccard(given_watch)
    watch_match_cosine(given_watch)
    

