import sys
import time
import math
import numpy as np

begin = time.time()

threshold = 0.9
rows = 20
bands = 6
sig_len = rows * bands

def extract_shingles(article):
    cleaned_article = ''.join(char.lower() for char in article if char.isalpha() or char.isspace())
    return {''.join(cleaned_article[i:i+3]) for i in range(len(cleaned_article)-2)}

def jaccard(s1, s2):
    intersection = len(s1 & s2)
    union = len(s1 | s2)
    return intersection / union

id_list = []
unique_shingles = set()
all_shingles = []
with open(sys.argv[1], 'r') as articles:
    for article in articles:
        id, document = article.split(" ", 1)
        id_list.append(id)
        shingles = extract_shingles(document)
        all_shingles.append(shingles)
        unique_shingles |= shingles

shingle_index = {shingle: idx for idx, shingle in enumerate(unique_shingles)}

C = next(C for C in range(len(unique_shingles), sys.maxsize) if all(C % i for i in range(2, int(math.sqrt(C)) + 1)))

col = len(id_list)
A = np.random.randint(0, C, sig_len)
B = np.random.randint(0, C, sig_len)
signatures = np.full((col, sig_len), float('inf'))
for idx, shingles in enumerate(all_shingles):
    for shingle in shingles:
        x = shingle_index[shingle]
        hash_values = (A * x + B) % C
        signatures[idx] = np.minimum(signatures[idx], hash_values)

candidates = set()
hash_tables = [{} for _ in range(bands)]
for idx, signature in enumerate(signatures):
    for band in range(bands):
        band_data = tuple(signature[band * rows : (band + 1) * rows])
        hash_val = sum((A[band] * x + B[band]) % C for x in band_data)
        hash_tables[band].setdefault(hash_val, []).append(idx)

for table in hash_tables:
    for bucket in table.values():
        if len(bucket) > 1:
            candidates.update((min(pair), max(pair)) for pair in itertools.combinations(bucket, 2))

results = [(id_list[i], id_list[j]) for i, j in candidates if jaccard(all_shingles[i], all_shingles[j]) >= threshold]

for i, j in results:
    print(f"{i}\t{j}")

end = time.time()
print(f"Total time: {(end - begin):.6f} seconds")
