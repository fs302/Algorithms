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
