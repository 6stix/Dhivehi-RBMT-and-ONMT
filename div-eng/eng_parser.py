"""
This script tokenizes an English corpus consisting of mostly Biblical text. It separates punctuation!

Author: 6stix
Date: May 2019
"""

# If you add more books to the corpus, please add them in here!
books = ["GENESIS", "EXODUS", "RUTH", "SAMOne", "SAMTwo", "PRO", "JONAH", "MARK", "LUKE", "JOHN", "ARTICLE"]

data = ""
with open('eng-text.txt', 'r') as f:
  data = f.read()

### Commas (,)
data = data.replace(",", " ,")
data = data.replace("  ,", " ,")

### Periods (.)
data = data.replace(".", " .")
data = data.replace("  .", " .")

### Question-marks (?)
data = data.replace("?", " ?")
data = data.replace("  ?", " ?")

### Exclamation marks (!)
data = data.replace("!", " !")
data = data.replace("  !", " !")

### Extra marks
### I should've done this from the start, lol
marks = [";", ":", "-", "_", "(", ")", "[", "]", "\\", "/", "{", "}"]
for mark in marks:
  data = data.replace(mark, " " + mark)
  data = data.replace("  " + mark, " " + mark)

### Space between English-style quotes (“)
data = data.replace('“', ' “ ')
data = data.replace('  “', ' “')
data = data.replace('“  ', '“ ')

### Space between English-style quotes (”)
data = data.replace('”', ' ” ')
data = data.replace('  ”', ' ”')
data = data.replace('”  ', '” ')

### Space between English-style quote (")
marks = ["\"", "\'"]
for mark in marks:
  data = data.replace(mark, ' ' + mark + ' ')
  data = data.replace('  ' + mark, ' ' + mark)
  data = data.replace(mark + '  ', mark + ' ')

nums = []
for i in range(50):
  data = data.replace(" " + str(i), "\n" + str(i)) #+ " ")

for i in range(10):
  data = data.replace("\n\n", "\n")

### Fix spacing for book nums
for book in books:
  data = data.replace(book + "\n", book + " ")

str_50 = []
for i in range(50):
  str_50.append(str(i))

base = 1
cp_data = data.split("\n")
lent = len(cp_data)
i = 0
while i < lent - 1:
  line = cp_data[i]
  """
  try:
    next_int = int(next_first[:2])
  
  except:
    try:
      next_int = int(next_first[:1])

    except:
      cp_data[i] = cp_data[i] + " " + cp_data.pop(i+1)
      lent = lent - 1
      i = i - 1

    continue
  """
  first = line.split()[0]
  noped = False

  if first in books:
    base = 1

  else: # a line without a book name
    next_line = cp_data[i+1]

    try:
      next_first = next_line.split()[0]
    except:
      break
    
    chapter_done = False
    if next_first in books:
      chapter_done = True

    if next_first[:2] in str_50:
      next_int = int(next_first[:2])

    elif chapter_done == True:
      noped = True

    else:
      try:
        next_int = int(next_first[:1])
      except: # line does not begin on an integer
        cp_data[i] = cp_data[i] + " " + cp_data.pop(i+1)
        lent = lent - 1
        i = i - 1
        noped = True

    if noped != True:
      # if proper
      if next_int == base + 1:
        base += 1

      # if parsing screwed-up
      else:
        cp_data[i] = cp_data[i] + " " + cp_data.pop(i+1)
        lent = lent - 1
        i = i - 1

  i += 1

for i,line in enumerate(cp_data): #.split('\n')):
  if line[:2] in str_50:
    cp_data[i] = cp_data[i][2:]
  elif line[:1] in str_50:
    cp_data[i] = cp_data[i][1:]
  else:
    pass


### Check number of lines per book
count = 0
for line in cp_data:
  try:
    curr = line.split()[0]
  except:
    print("count:", count)
    break

  if curr not in books:
    count += 1

  else:
    print("count:", count)
    count = 0


lent = len(cp_data)
i = 0
book_counter = 0
while i < lent - 1:
  curr = cp_data[i]
  if curr.split()[0] in books:
    print("book:", cp_data[i], "book_counter:", book_counter)
    book_counter += 1
    cp_data.pop(i)
    i = i - 1
    lent = lent - 1

  i += 1

with open("parsed_eng-text.txt", 'w') as f:
  f.write("\n".join(cp_data))
