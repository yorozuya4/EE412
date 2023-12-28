import sys
import time

def main(file_path, threshold):
    item_baskets = []
    with open(file_path, 'r') as baskets:
        item_baskets = [basket.strip().split() for basket in baskets]

    item_int = {}
    item_counts_array = []
    for basket in item_baskets:
        for item in basket:
            if item not in item_int:
                item_int[item] = len(item_int) + 1
                item_counts_array.append(0)
            item_counts_array[item_int[item] - 1] += 1

    frequent_items_table = [0] * len(item_int)
    freq_item_n = 1
    for idx, count in enumerate(item_counts_array):
        if count >= threshold:
            frequent_items_table[idx] = freq_item_n
            freq_item_n += 1

    triangle = [0] * ((freq_item_n - 1) * (freq_item_n - 2) // 2)
    for basket in item_baskets:
        freq_item_in_basket = [frequent_items_table[item_int[item] - 1] for item in basket if frequent_items_table[item_int[item] - 1] != 0]
        for x in range(len(freq_item_in_basket)):
            for y in range(x + 1, len(freq_item_in_basket)):
                i, j = sorted((freq_item_in_basket[x], freq_item_in_basket[y]))
                k = (i - 1) * (freq_item_n - i // 2) + j - i - 1
                triangle[int(k)] += 1

    print(freq_item_n - 1)
    freq_pair_n = sum(1 for count in triangle if count >= threshold)
    print(freq_pair_n)

    sorted_list = sorted(((k, count) for k, count in enumerate(triangle) if count >= threshold), key=lambda x: -x[1])
    top_ten_results = dict(sorted_list[:10])

    for k, count in top_ten_results.items():
        i = 1
        while k >= (i - 1) * (freq_item_n - i / 2):
            i += 1
        i -= 1
        j = k + i - (i - 1) * (freq_item_n - i / 2) + 1
        item1 = next(item for item, idx in item_int.items() if frequent_items_table[idx - 1] == i)
        item2 = next(item for item, idx in item_int.items() if frequent_items_table[idx - 1] == j)
        count1 = item_counts_array[item_int[item1] - 1]
        count2 = item_counts_array[item_int[item2] - 1]
        conf_1_2 = count / count1
        conf_2_1 = count / count2
        print(f'{item1}\t{item2}\t{count}\t{conf_1_2:.6f}\t{conf_2_1:.6f}')

if __name__ == "__main__":
    begin = time.time()
    if len(sys.argv) != 3:
        print("Usage: script.py <file> <threshold>")
        sys.exit(1)
    main(sys.argv[1], int(sys.argv[2]))
    end = time.time()
    print(f"Total time: {(end - begin):.6f} seconds")
