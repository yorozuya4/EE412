import sys
##import time

##begin=time.time()

threshold=100

item_baskets=list()
with open(sys.argv[1],"r") as baskets:
    for basket in baskets:
        item_baskets.append(basket.strip().split())

item_integer=dict()
n=1
for basket in item_baskets:
    for item in basket:
        if item not in item_integer:
            item_integer[item]=n
            n+=1

index_to_item=dict()
for item,index in item_integer.items():
    index_to_item[index]=item

pair_counts=dict()
for basket in item_baskets:
    index=[item_integer[item] for item in basket]
    for i in range(len(index)):
        for j in range(i+1,len(index)):
            pair=tuple(sorted([index[i],index[j]]))
            if pair in pair_counts:
                pair_counts[pair]+=1
            else:
                pair_counts[pair]=1

frequent_pairs=dict()
for pair,count in pair_counts.items():
    if count>=threshold:
        frequent_pairs[pair]=count

triple_counts=dict()
for basket in item_baskets:
    index=list()
    for item in basket:
        index.append(item_integer[item])
    for i in range(len(index)):
        for j in range(i+1,len(index)):
            for k in range(j+1,len(index)):
                if tuple(sorted([index[i],index[j]])) in frequent_pairs and tuple(sorted([index[i],index[k]])) in frequent_pairs and tuple(sorted([index[j],index[k]])) in frequent_pairs:
                    triple=tuple(sorted([index[i],index[j],index[k]]))
                    if triple in triple_counts:
                        triple_counts[triple]+=1
                    else:
                        triple_counts[triple]=1

frequent_triples=dict()
for triple,k in triple_counts.items():
    if k>=threshold:
        frequent_triples[triple]=k

frequent_triples_list=list(frequent_triples.items())
frequent_triples_list=sorted(frequent_triples_list, key=lambda x: -x[1])

print(len(frequent_triples_list))
for (item1,item2,item3),n in frequent_triples_list[:10]:
    conf_12_3=n/frequent_pairs[(item1,item2)]
    conf_13_2=n/frequent_pairs[(item1,item3)]
    conf_23_1=n/frequent_pairs[(item2,item3)]
    print(f"{index_to_item[item1]}\t{index_to_item[item2]}\t{index_to_item[item3]}\t{n}\t{conf_12_3:.6f}\t{conf_13_2:.6f}\t{conf_23_1:.6f}")

##end=time.time()
##print(f"Total time: {(end-begin):.6f} seconds")