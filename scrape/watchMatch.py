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
    
def watch_match(givenWatch):
    # Combine descriptors into a single column
    df['CombinedDescriptors'] = df.apply(lambda row: [row[col] for col in df.columns], axis=1)

    # Convert descriptors to binary indicators
    mlb = MultiLabelBinarizer()
    descriptor_matrix = mlb.fit_transform(df['CombinedDescriptors'])

    # Convert the given watch descriptors to binary
    given_watch_binary = mlb.transform([list(givenWatch.values())])

    # Calculate Jaccard similarity between the given watch and each row
    similarities = jaccard_score(given_watch_binary, descriptor_matrix, average=None)

    # Find the index of the row with the highest similarity
    best_match_index = similarities.argmax()

    # Get the best matching row
    best_match_row = df.loc[best_match_index]

    print("Best Matching Row:")
    print(best_match_row)