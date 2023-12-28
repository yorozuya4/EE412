import sys
from pyspark import SparkConf, SparkContext

def main(file_path):
    conf = SparkConf()
    with SparkContext(conf=conf) as sc:
        raw_line = sc.textFile(file_path)
        line = raw_line.map(lambda line: line.split("\t"))
        real_friends = line.filter(lambda x: len(x) > 1)
        user_friends = real_friends.map(lambda x: (x[0], x[1].split(",")))

        # Create direct_pairs using a broadcast variable
        direct_pairs = user_friends.flatMap(lambda x: [tuple(sorted((x[0], friend))) for friend in x[1]]).collect()
        broadcast_direct_pairs = sc.broadcast(set(direct_pairs))

        def potential_pair(friends):
            return [tuple(sorted((friends[i], friends[j]))) for i in range(len(friends)) for j in range(i + 1, len(friends))]

        potential_pairs = user_friends.flatMap(lambda x: potential_pair(x[1]))
        mutual_pairs = potential_pairs.filter(lambda x: x not in broadcast_direct_pairs.value)
        mutual_friends = mutual_pairs.reduceByKey(lambda x, y: x + y)

        results = mutual_friends.sortBy(lambda x: (-x[1], x[0][0], x[0][1]))
        top_ten = results.take(10)
        for ((user1, user2), count) in top_ten:
            print(f"{user1}\t{user2}\t{count}")

begin = time.time()
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: script.py <file>")
        sys.exit(1)
    main(sys.argv[1])
end = time.time()

print(f"Total time: {(end - begin):.6f} seconds")
