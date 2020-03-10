# Translate from Dhivehi to English:

1. Go into the RBMT-div-eng directory:
2. Run the following:
```
  $ echo (Dhivehi) | apertium -d . div-eng
```

# Translate a file from Dhivehi to English 
```
  $ cat (filename) | apertium -d . div-eng
```

# How to calculate WER and PER 
```
  $ cat (filename) | apertium -d . div-eng > out.txt
  $ apertium-eval-translator.pl -r (source language translation) -t out.txt
```
