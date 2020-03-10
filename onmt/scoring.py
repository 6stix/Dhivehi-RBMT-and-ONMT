from jiwer import wer
import nltk

with open("model_20000_ish_test.txt", 'r') as f:
  predictions = f.read().strip().split('\n')
with open("eng_test.txt", 'r') as f:
  truth = f.read().split('\n')

wer_count = 0
for i in range(len(predictions)):
  print("i:", i)
  curr_wer = wer(truth[i], predictions[i])
  wer_count += curr_wer
  print("WER:", curr_wer)

print("\n", wer_count)
print("Average WER:", wer_count / len(predictions))

list_of_references = []
for true in truth:
  list_of_references.append(true)

hypotheses = predictions[:]

c_bleu = nltk.translate.bleu_score.corpus_bleu(list_of_references, hypotheses)
print("CORPUS BLEU SCORE:", c_bleu)

print("SENTENCE 1 BLEU SCORE:", nltk.translate.bleu_score.sentence_bleu(truth[0], [predictions[0]]))

print("truth[0]:\n", truth[0], "\npred[0]:\n", predictions[0])
