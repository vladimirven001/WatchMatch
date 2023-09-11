import time
import pandas as pd
from sklearn.metrics import jaccard_score
from sklearn.preprocessing import MultiLabelBinarizer

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


def watch_match(givenWatch):
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
    givenWatch = "a. lange & söhne,1815,236.049,1815 200th anniversary f. a. lange,a. lange & söhne caliber l051.1hours, minutes, small seconds,2015,platinum,sapphire,open,round,40.00 mm,8.80 mm,,black,silver,arabic numerals,alpha,yes, 200 units"
    watch_match(givenWatch)
    

