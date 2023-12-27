import sys
##import time

##begin=time.time()

threshold=100

item_baskets=list()
with open(sys.argv[1],'r') as baskets:
    for basket in baskets:
        item_baskets.append(basket.strip().split())

item_int=dict()
item_counts_array=list()
n=1
for basket in item_baskets:
    for item in basket:
        if item not in item_int:
            item_int[item]=n
            item_counts_array.append(0)
            n+=1
        item_counts_array[item_int[item]-1]+=1

frequent_items_table=[0]*len(item_int)
m=1
for idx,count in enumerate(item_counts_array):
    if count>=threshold:
        frequent_items_table[idx]=m
        m+=1
freq_item_n=m-1

triangle=[0]*int((m-1)*(m-2)/2)

for basket in item_baskets:
    freq_item_in_basket=list()
    for item in basket:
        if frequent_items_table[item_int[item]-1]!=0:
            freq_item_in_basket.append(frequent_items_table[item_int[item]-1])
    for x in range(len(freq_item_in_basket)):
        for y in range(x+1,len(freq_item_in_basket)):
            n=freq_item_n
            i,j=freq_item_in_basket[x],freq_item_in_basket[y]
            if not i<j:
                i,j=(j,i)
            k=int((i-1)*(n-(i/2))+j-i-1)
            triangle[k]+=1

print(freq_item_n)
freq_pair_n=0
for count in triangle:
    if count>=threshold:
        freq_pair_n+=1
print(freq_pair_n)

sorted_list=list()
for k,count in enumerate(triangle):
    if count>=threshold:
        sorted_list.append((k,count))

sorted_list=sorted(sorted_list, key=lambda x: -x[1])
top_ten_results=dict()
for k,count in sorted_list[:10]:
    top_ten_results[k]=count

for k,count in top_ten_results.items():
    n=freq_item_n
    i=1
    while k>=(i-1)*(n-i/2):
        i+=1
    i-=1
    j=k+i-(i-1)*(n-i/2)+1
    item1=next(item for item,idx in item_int.items() if frequent_items_table[idx-1]==i)
    item2=next(item for item,idx in item_int.items() if frequent_items_table[idx-1]==j)
    count1=item_counts_array[item_int[item1]-1]
    count2=item_counts_array[item_int[item2]-1]
    conf_1_2=count/count1
    conf_2_1=count/count2
    print(f'{item1}\t{item2}\t{count}\t{conf_1_2:.6f}\t{conf_2_1:.6f}')

##end=time.time()
##print(f"Total time: {(end-begin):.6f} seconds")