"""
This file splits the data into training, validation, and testing data sets.

Author: 6stix  
Date: May 2019
"""

import random
import math
import itertools

with open("parsed_div-text.txt", 'r') as f:
  div = f.read().split('\n')
with open("parsed_eng-text.txt", 'r') as f:
  eng = f.read().split('\n')

map_index = list(zip(div, eng))
random.shuffle(map_index)
div, eng = zip(*map_index)

test_break = math.ceil(0.8 * len(div))

div_test = div[test_break:]
eng_test = eng[test_break:]

div = div[:test_break]
eng = eng[:test_break]

# Separate data
bar1 = (0, math.ceil(0.25 * len(div)))
bar2 = (math.ceil(0.25 * len(div)), math.ceil(0.5 * len(div)))
bar3 = (math.ceil(0.75 * len(div)), len(div))

# Generate 3-folds (for k-fold cross-validation)
bars = [bar1, bar2, bar3]
combs = itertools.combinations(bars, 2)

dirs = ['set1', 'set2', 'set3']

for comb in combs:
  curr_dir = dirs.pop()
  c_1 = comb[0]
  c_2 = comb[1]
  div_train = div[c_1[0]:c_1[1]] + div[c_2[0]:c_2[1]]
  eng_train = eng[c_1[0]:c_1[1]] + eng[c_2[0]:c_2[1]]
 
  val_c = (0, 0)
  for bar in bars:
    if bar != c_1 and bar != c_2:
      val_c = bar
  
  div_val = div[val_c[0]:val_c[1]]
  eng_val = eng[val_c[0]:val_c[1]]

  with open(curr_dir + "/div_train.txt", 'w') as f:
    f.write("\n".join(div_train))
  with open(curr_dir + "/div_val.txt", 'w') as f:
    f.write("\n".join(div_val))
  with open(curr_dir + "/div_test.txt", 'w') as f:
    f.write("\n".join(div_test))
  with open(curr_dir + "/eng_train.txt", 'w') as f:
    f.write("\n".join(eng_train))
  with open(curr_dir + "/eng_val.txt", 'w') as f:
    f.write("\n".join(eng_val))
  with open(curr_dir + "/eng_test.txt", 'w') as f:
    f.write("\n".join(eng_test))
