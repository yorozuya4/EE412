import re
import sys
from pyspark import SparkConf, SparkContext
conf=SparkConf()
sc=SparkContext(conf=conf)

lines=sc.textFile(sys.argv[1])
words=lines.flatMap(lambda l: re.split(r'[^\w]+', l))
alphabet_words=words.filter(lambda word: len(word)>0 and word[0].isalpha())
lower_case_pair=alphabet_words.map(lambda word: (word[0].lower(), word.lower()))
unique_words=lower_case_pair.distinct()
word_count=unique_words.countByKey()

for letter, count in sorted(word_count.items()):
    print(f"{letter}\t{count}")