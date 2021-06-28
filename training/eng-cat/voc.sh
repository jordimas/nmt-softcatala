VOCSIZE=100000
python3 ../sentencepiece-tokenizer.py -v $VOCSIZE
onmt-build-vocab --from_vocab en_m.vocab --from_format sentencepiece --save_vocab src-vocab.txt.token
onmt-build-vocab --from_vocab ca_m.vocab --from_format sentencepiece --save_vocab tgt-vocab.txt.token
