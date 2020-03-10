# Dhivehi-RBMT-and-ONMT
Comparing the performance of a rule-based machine translation system with OpenNMT's neural machine translation.

For information on how to run these tests for yourself, see section **Set-up and Testing**! To check-out how to get set-up with an RBMT for Dhivehi, go to the **RBMT** folder as seen above! The README will help you there.

## RBMT and ONMT

**3-Fold Cross-Valdiation** for NMT system taking into account word-error-rate, position-independent error rate, words in the target (reference), and the words in the prediction:

| Fold    | WER           | PER     | Words in target | Words in prediction |
| :---:   |    :----:     |     :---:  |  :---:          | :---:         |
**1**| 86.68%  | 40.49%        | 12970      |  9650           |
**2**| 90.69%  | 29.38%        | 12664      |  12070          |
**3**| 85.65%  | 48.29%        | 12292      |  7802           |

Generalized WER: 87.67%
Generalized PER: 39.32%

*Note: These are the models' scores on their respective validation sets.*

Although the second model has a slightly higher WER than the other two, it has a significantly lower PER. Due to the great difference in its WER and PER, that means that this model generates more of the correct words than the others but just in the wrong order. Due to the similarities in WER with the other models and the much smaller PER, we chose the second model to be the final model. In other words, we determined model two to be the best-performing of the three and ran it against the test set of data. This is the model you will see the results for in the "Final Evaluation" section!

**Final Evaluation** on the test data:

| System      | WER | PER     | Words in target | Words in perdiction |
| :---:       |    :----:   |     :---:     |  :---:             | :---:         |
**RBMT**| 94.77%      | 89.37%       | 12211   |  10125           |
**NMT**| 88.17%   | 32.02%        | 12211      |  10629          |

## Set-up with a Neural Machine Translation (NMT) system

If you only want to do testing on the files already in the repository and our models, then skip to **Testing pre-trained models**. If you are interested in performing some of the steps that we did, please read on.

#### Set-up

*Note: this guide assumes you are on linux.*

Create a virtual environment and install OpenNMT by running these commands:

```bash
virtualenv onmt_env
source onmt_env/bin/activate
pip install OpenNMT-tf[tensorflow_gpu]
```

Next, you should do is git clone this repository. Then, using a terminal, cd into the div-eng directory. You will find various files pertaining to corpora. You will be most-interested in div-text.txt, which is a collection of Dhivehi sentences from the Bible, eng-text.txt, a collection of English sentences from the KJV version of the Bible, and in div_UNN.txt with eng_UNN.txt, the Universal Declaration of Human Rights from the UNN. If you would like to add biblical text to the parallel corpus, you should go to Bible.com and search for the book and chapter you would like to add. Copy and paste (or write a script that collects biblical text) the texts into div-text.txt and the corresponding texts in eng-text.txt. You don't have to worry about separating sentences as of right now. After you do that, run:

```python3
python3 eng_parser.py
python3 div_parser.py
```

This will re-write the parsed_div-text.txt and parsed_eng-text.txt files. After performing this task, cp these files to the onmt folder. You could do this by cd'ing into the onmt folder, and then running (type in 'y' when it asks you if you want to overwrite a file):

```bash
cp ../div-eng/parsed* ./
```

After copying the parsed-text files to your onmt folder, run:

```bash
python3 k_split.py
```

This command will split-up the data into three-folds for cross-validation. Each set is split into its own folder, named "set" and then its number. Everytime you use this command, the three sets will be different (except sometimes) than before, because it randomly picks pieces of the data to form each subset. Now, you will have to generate the vocabulary in each set. Run these commands, starting from within the onmt folder:

```bash
cd set1
onmt-build-vocab --save_vocab div_vocab.txt div_train.txt
onmt-build-vocab --save_vocab eng_vocab.txt eng_train.txt
```

These commands will grab all of the words from the Dhivehi training corpus and the English training corpus and save them to lang_vocab.txt files. After performing these commands for set1, perform them for the remaining sets.

Next, you will have to look at the data.yaml file located within each set folder. You can keep all of it the same, but you can change the model_dir folder if you wish to save the trained model elsewhere. Now it is time to train the model!

From within each set folder, run:

```bash
mkdir run
onmt-main train_and_eval --model_type Transformer --auto_config --config data.yml
```

I recommend running training as a background process on different machines if possible. If it is not possible, then run training of the three sets as background processes. To run it as a background process, use this modified version of the command above:

```bash
nohup onmt-main train_and_eval --model_type Transformer --auto_config --config data.yml &
```

This will save any output from the training into nohup.txt files for each set. Also, you may want to let training run for at-least a day to see results similar to ours.

If you find that some of the commands do not work due to missing packages, run these commands:

```bash
pip install -r requirements/requirements_python2.txt
pip3 install -r requirements/requirements_python3.txt
```

After training for however long you desire, you can start translating! cd into each of the set folders and run:

```bash
onmt-main infer --auto_config --config data.yml --features_file div_val.txt > model_val_predictions.txt
```

Edit the model_val_predictions.txt file to only include the translations. Remove text having to do with Tensorflow and whatnot.

Now, we want to evaluate the performances of the models on their corresponding validation sets. To do this, from within the set folders we run:

```bash
../tools/apertium-eval-translator-line.pl -t model_val_predictions.txt -r eng_val.txt | tee wer_per_val.txt
```

If you take a look at wer_per_val.txt, you will see the WER, PER, and other information about the model's performance. WER is the word-error-rate, or basically how far the model was from being right about the translation. The PER is the position-independent error rate, or basically how many words did the model have right in the sentence regardless of order. After doing this evaluation on each of the models, pick the one with the lowest WER and PER, if possible. In our case, our WER's were very similar but one of our models (set2) had a significantly smaller PER. After picking this model, you can now run predictions on the final test data!

cd into the set of the model you chose to be the best. Now, run this command:

```bash
onmt-main infer --auto_config --config data.yml --features_file div_val.txt > model_test_predictions.txt
```

Remove any non-translation text from the beginning of the model_test_predictions file, and then run:

```bash
../tools/apertium-eval-translator-line.pl -t model_test_predictions.txt -r eng_test.txt | tee wer_per_test.txt
```

Lastly, take a look at the wer_per_test.txt file for information on the performance of the model!

#### Testing pre-trained models

If you just want to run translations using the models we trained, then please read on.

You'll want to download our models. Download all three folders from the shared google drive link below. Create "run" folders in each of the set folders. Then, take all of the files from the model_1 folder on google and move them into the set1/run folder. Do the same for model_2 with set2/run and model_3 with set3/run.

https://drive.google.com/drive/folders/1LYttbfWG6hK9jmdCrO4mSbCSzPZCLwud?usp=sharing

Now, you should create a virtual environment and install OpenNMT by running these commands:

```bash
virtualenv onmt_env
source onmt_env/bin/activate
pip install OpenNMT-tf[tensorflow_gpu]
```

cd into the set2 folder, and then run:

```bash
../tools/apertium-eval-translator-line.pl -t div_test_predictions.txt -r eng_test.txt | tee wer_per_test.txt
```

If you find that some of the command does not work, then cd to where the requirements folder is and run:

```bash
pip install -r requirements/requirements_python2.txt
pip3 install -r requirements/requirements_python3.txt
```

Check out the wer_per_test.txt file to see the performance of the model!

Our Ling073 page: https://wikis.swarthmore.edu/ling073/Dhivehi_and_English/Final_project#Dhivehi_RBMT_and_ONMT

To learn more about OpenNMT, visit: http://opennmt.net or http://opennmt.net/OpenNMT-tf/
