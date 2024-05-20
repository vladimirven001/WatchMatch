import pandas as pd
import numpy as np
from sklearn.metrics import jaccard_score
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

def watch_match_cosine_search(given_watch):
    # Load the dataset
    try:
        df = pd.read_csv('./ressources/watches.csv')
    except:
        df = pd.DataFrame(columns = ["brand","family","reference","name","movement","produced","caseMaterial",
                                        "caseGlass","caseBack","caseShape","caseDiameter","caseHeight","caseLugWidth","dialColor",
                                    "dialMaterial","dialIndexes","dialHands", "image", "price"])
    
    # Remove NaN values from the dataset
    df = df.replace([np.nan, -np.inf], 0)

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

    # Keep only top 20 indices
    top_indices = closest_match_indices[:100]

    # Get the details of the closest matches (one per brand)
    results = [df.iloc[idx].to_dict() for idx in top_indices]

    # Capitalize the brand names
    for result in results:
        result['brand'] = result['brand'].capitalize()
        result['family'] = result['family'].capitalize()

    return results

def watch_match_jaccard(givenWatch):
    # Load the dataset
    try:
        df = pd.read_csv('./ressources/watches.csv')
    except:
        df = pd.DataFrame(columns = ["brand","family","reference","name","movement","produced","caseMaterial",
                                        "caseGlass","caseBack","caseShape","caseDiameter","caseHeight","caseLugWidth","dialColor",
                                    "dialMaterial","dialIndexes","dialHands", "image", "price"])
        
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
    
def search(given_watch):
    return watch_match_cosine_search(given_watch)

if __name__ == "__main__":
    print(search("a langhe & sohne"))