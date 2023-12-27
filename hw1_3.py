import sys
##import time
import math
import numpy as np

##begin=time.time()

threshold=0.9
rows=20
bands=6
sig_len=rows*bands

def extract_shingles(article):
    cleaned_article=""
    for char in article:
        if char.isalpha() or char.isspace():
            cleaned_article+=char
    cleaned_article=" ".join(cleaned_article.split()).lower()
    shingles_set=set()
    for i in range(len(cleaned_article)-2):
        shingle=cleaned_article[i:i+3]
        shingles_set.add(shingle)
    return shingles_set

def jaccard(s1,s2):
    set1=set(s1)
    set2=set(s2)
    intersection=len(set1.intersection(set2))
    union=len(set1.union(set2))
    return intersection/union

id_list=list()
unique_shingles=set()
all_shingles=list()
with open(sys.argv[1],'r') as articles:
    for article in articles:
        id,document=article.split(" ",1)
        id_list.append(id)
        shingles=extract_shingles(document)
        all_shingles.append(shingles)
        unique_shingles=unique_shingles.union(shingles)

shingle_index=dict()
for index,shingle in enumerate(unique_shingles):
    shingle_index[shingle]=index

C=len(unique_shingles)
while True:
    if all(C%i for i in range(2,int(math.sqrt(C))+1)):
        break
    else:
        C+=1

col=len(id_list)
A=np.random.randint(0,C,sig_len)
B=np.random.randint(0,C,sig_len)
signatures=np.full((col,sig_len),10**100)
for idx in range(len(all_shingles)):
    for shingle in all_shingles[idx]:
        x=shingle_index[shingle]
        hash_value=(A*x+B)%C
        signatures[idx]=np.minimum(signatures[idx],hash_value)

candidates=set()
hash_tables=list()
for i in range(bands):
    hash_tables.append(dict())

for idx in range(len(signatures)):
    for band in range(bands):
        band_list=list()
        for r in range(band*rows,(band+1)*rows):
            band_list.append(signatures[idx][r])
        band_data=tuple(band_list)

        hash_val=0
        for x in band_data:
            value=(A[band]*x+B[band])%C
            hash_val+=value
        if hash_val not in hash_tables[band]:
            hash_tables[band][hash_val]=list()
        hash_tables[band][hash_val].append(idx)

for table in hash_tables:
    for bucket in table.values():
        if len(bucket)>1:
            for i in range(len(bucket)):
                for j in range(i+1,len(bucket)):
                    candidates.add((bucket[i],bucket[j]))

results=list()
for i,j in candidates:
    jaccard_sim=jaccard(all_shingles[i],all_shingles[j])
    if jaccard_sim>=threshold:
        results.append((i,j))

for i,j in results:
    print(f"{id_list[i]}\t{id_list[j]}")

##end=time.time()
##print(f"Total time: {(end-begin):.6f} seconds")