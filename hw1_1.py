import sys
##import time

##begin=time.time()

from pyspark import SparkConf, SparkContext
conf=SparkConf()
sc=SparkContext(conf=conf)

def potential_pair(friends):
    key_pairs=[]
    n=len(friends)
    for i in range(n):
        for j in range(i+1,n):
            key_pair=tuple(sorted((friends[i],friends[j])))
            key_pairs.append((key_pair,1))
    return key_pairs

def direct_pair(user,friends):
    key_pairs=[]
    for friend in friends:
        key_pair=tuple(sorted((user,friend)))
        key_pairs.append(key_pair)
    return key_pairs

raw_line=sc.textFile(sys.argv[1])
line=raw_line.map(lambda line: line.split("\t"))
real_friends=line.filter(lambda x: len(x)>1)
user_friends=real_friends.map(lambda x: (x[0], x[1].split(",")))
potential_pairs=user_friends.flatMap(lambda x: potential_pair(x[1]))
direct_pairs=user_friends.flatMap(lambda x: direct_pair(x[0],x[1])).collect()
direct_pairs=set(direct_pairs)
mutual_pairs=potential_pairs.filter(lambda x: x[0] not in direct_pairs)
mutual_friends=mutual_pairs.reduceByKey(lambda x,y: x+y)

results=mutual_friends.sortBy(lambda x: (-x[1],x[0][0],x[0][1]))
top_ten=results.take(10)
for ((user1,user2), count) in top_ten:
    print(f"{user1}\t{user2}\t{count}")

sc.stop()

##end=time.time()
##print(f"Total time: {(end-begin):.6f} seconds")