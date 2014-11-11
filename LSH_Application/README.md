> Your task is to quickly find the number of pairs of sentences that are at the word-level edit distance at most 1. Two sentences S1 and S2 they are at edit distance 1 if S1 can be transformed to S2 by: adding, removing or substituting a single word.

 For example, consider the following sentences where each letter represents a word:
* S1: A B C D
* S2: A B X D
* S3: A B C
* S4: A B X C
 Then pairs the following pairs of sentences are at word edit distance 1 or less: (S1, S2), (S1, S3), (S2, S4), (S3, S4).


# sort and map, list and count duplicate pair
python sort-and-map.py sentences.txt sentences-sorted-mapped.txt dup_list.txt dup_count.txt

rm -r -f files
mkdir files

# divide
python divide-into-files-by-len.py files/ sentences-sorted-mapped.txt

# count pairs
python count-same-len.py files/ pair_list.txt 
python count-next-len.py files/ nn_pair_list.txt
cat pair_list.txt nn_pair_list.txt > merge_pair_list.txt

# solve duplicate
python calculate-with-dup.py dup_count.txt merge_pair_list.txt
