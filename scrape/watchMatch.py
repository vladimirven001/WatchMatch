import time
import pandas as pd
from sklearn.metrics import jaccard_score
from sklearn.preprocessing import MultiLabelBinarizer

try:
    df = pd.read_csv('watches.csv')
except:
    df = pd.DataFrame(columns = ["brand","family","reference","name","movement","produced","limited","caseMaterial",
                                    "caseGlass","caseBack","caseShape","caseDiameter","caseHeight","caseLugWidth","dialColor",
                                    "dialMaterial","dialIndexes","dialHands"])
    
try:
    dfCombined = pd.read_csv('watchesCombined.csv')
except:
    dfCombined = pd.DataFrame(columns = ["brand","family","reference","name","movement","produced","limited","caseMaterial",
                                    "caseGlass","caseBack","caseShape","caseDiameter","caseHeight","caseLugWidth","dialColor",
                                    "dialMaterial","dialIndexes","dialHands","combinedDescriptors"])

def combined_descriptors():
    # Combine descriptors into a single column
    df['combinedDescriptors'] = df.apply(lambda row: [str(row[col]) for col in df.columns], axis=1)
    print(df['combinedDescriptors'])
    df.to_csv('watchesCombined.csv', index=False)

# Define a custom Jaccard similarity function
def jaccard_similarity(a, b):
    intersection = sum(min(x, y) for x, y in zip(a, b))
    union = sum(max(x, y) for x, y in zip(a, b))
    return intersection / union if union > 0 else 0.0

def watch_match(givenWatch):
    # Convert descriptors to binary indicators
    mlb = MultiLabelBinarizer()
    descriptor_matrix = mlb.fit_transform(str(dfCombined['combinedDescriptors']))
    given_watch_binary = mlb.transform([list(givenWatch)])  

    # Calculate Jaccard similarity between the given watch and each row
    similarities = [jaccard_similarity(given_watch_binary[0], row) for row in descriptor_matrix]

    # Find the index of the row with the highest similarity
    best_match_index = similarities.index(max(similarities))

    # Get the best matching row
    best_match_row = dfCombined.loc[best_match_index]

    print("Best Matching Row:")
    print(best_match_row)

if __name__ == "__main__":
    givenWatch = "a. lange & söhne,1815,236.049,1815 200th anniversary f. a. lange,a. lange & söhne caliber l051.1hours, minutes, small seconds,2015,platinum,sapphire,open,round,40.00 mm,8.80 mm,,black,silver,arabic numerals,alpha,yes, 200 units"
    watch_match(givenWatch)
    

