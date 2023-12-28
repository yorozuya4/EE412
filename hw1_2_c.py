import sys
import time

threshold = 100

begin = time.time()

# Reading the baskets file and populating the item_baskets list
with open(sys.argv[1], "r") as baskets:
    item_baskets = [basket.strip().split() for basket in baskets]

# Generating item_integer and index_to_item dictionaries
item_integer = {item: idx + 1 for idx, item in enumerate(set(item for basket in item_baskets for item in basket))}
index_to_item = {idx: item for item, idx in item_integer.items()}

# Counting pairs
pair_counts = {}
for basket in item_baskets:
    indexed_basket = [item_integer[item] for item in basket]
    for i in range(len(indexed_basket)):
        for j in range(i + 1, len(indexed_basket)):
            pair = tuple(sorted([indexed_basket[i], indexed_basket[j]]))
            pair_counts[pair] = pair_counts.get(pair, 0) + 1

# Identifying frequent pairs
frequent_pairs = {pair: count for pair, count in pair_counts.items() if count >= threshold}

# Counting triples
triple_counts = {}
for basket in item_baskets:
    indexed_basket = [item_integer[item] for item in basket]
    for i in range(len(indexed_basket)):
        for j in range(i + 1, len(indexed_basket)):
            for k in range(j + 1, len(indexed_basket)):
                triple = tuple(sorted([indexed_basket[i], indexed_basket[j], indexed_basket[k]]))
                if all(tuple(sorted(pair)) in frequent_pairs for pair in [(triple[0], triple[1]), (triple[0], triple[2]), (triple[1], triple[2])]):
                    triple_counts[triple] = triple_counts.get(triple, 0) + 1

# Identifying frequent triples
frequent_triples = {triple: k for triple, k in triple_counts.items() if k >= threshold}

# Sorting and displaying top ten results
top_ten_frequent_triples = sorted(frequent_triples.items(), key=lambda x: -x[1])[:10]
for (item1, item2, item3), count in top_ten_frequent_triples:
    conf_12_3 = count / frequent_pairs[(item1, item2)]
    conf_13_2 = count / frequent_pairs[(item1, item3)]
    conf_23_1 = count / frequent_pairs[(item2, item3)]
    print(f"{index_to_item[item1]}\t{index_to_item[item2]}\t{index_to_item[item3]}\t{count}\t{conf_12_3:.6f}\t{conf_13_2:.6f}\t{conf_23_1:.6f}")

end = time.time()
print(f"Total time: {(end - begin):.6f} seconds")
