wget https://www.softcatala.org/pub/softcatala/opennmt/training-sets/eng-cat/eng-cat.zip
unzip eng-cat.zip
head -n 2000000 /home/jordi/sc/OpenNMT/datasets/UNPC/unpc-en.txt > unpc-en.txt
head -n 2000000 /home/jordi/sc/OpenNMT/datasets/UNPC/unpc-ca.txt > unpc-ca.txt
