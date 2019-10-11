# NLP Toolkit
Library containing state-of-the-art models for Natural Language Processing tasks  
*Note this repo is continually being updated (see [To do list](#to-do-list)) 

## Contents
Tasks:  
1. [Classification](#1-classification)
2. [Automatic Speech Recognition](#2-automatic-speech-recognition)
3. [Text Summarization](#3-text-summarization)
4. [Machine Translation](#4-machine-translation)
5. [Natural Language Generation](#5-natural-language-generation)
6. [Punctuation Restoration](#6-punctuation-restoration)  
7. [Named Entity Recognition](#7-named-entity-recognition)
  
[Benchmark Results](#benchmark-results)  
[References](#references)

## Pre-requisites
torch==1.2.0 ; spacy==2.1.8 ; torchtext==0.4.0 ; seqeval==0.0.12  
For chinese support in Translation: jieba==0.39  
For ASR: librosa==0.7.0 ; soundfile==0.10.2  

** Pre-trained models (XLNet, BERT, GPT-2) are courtesy of huggingface (https://github.com/huggingface/pytorch-transformers)

## Package Installation
```bash
git clone https://github.com/plkmo/NLP_Toolkit.git
cd NLP_Toolkit
python setup.py install

pip uninstall nlptoolkit # to uninstall if required since this repo is still currently in active development
```
Alternatively, you can just use it as a non-packaged repo after git clone.

## 1) Classification
The goal of classification is to segregate documents into appropriate classes based on their text content. Currently, the classification toolkit uses the following models:
1. Text-based Graph Convolution Networks (GCN)
2. Bidirectional Encoder Representations from Transformers (BERT)
3. XLNet

### Format of datasets files
The training data (default: train.csv) should be formatted into two columns 'text' and 'label' respectively, with rows being the documents index. 'text' contains the raw text and 'label' contains the corresponding label (integers 0, 1, 2... depending on the number of classes)

The infer data (default: infer.csv) should be formatted into at least one column 'text' being the raw text and rows being the documents index. Optional column 'label' can be added and --train_test_split argument set to 1 to use infer.csv as the test set for model verification.

### Running the model
Run classify.py with arguments below.

```bash
classify.py [-h] 
	[--train_data TRAIN_DATA (default: "./data/train.csv")] 
	[--infer_data INFER_DATA (default: "./data/infer.csv")]            
	[--max_vocab_len MAX_VOCAB_LEN (default: 7000)]  
	[--hidden_size_1 HIDDEN_SIZE_1 (default: 330)]
	[--hidden_size_2 HIDDEN_SIZE_2 (default: 130)]
	[--tokens_length TOKENS_LENGTH (default: 200)] 
	[--num_classes NUM_CLASSES (default: 2)]
	[--train_test_split TRAIN_TEST_SPLIT (default: 0)]
	[--test_ratio TEST_RATIO (default: 0.1)] 
	[--batch_size BATCH_SIZE (default: 32)]      
	[--gradient_acc_steps GRADIENT_ACC_STEPS (default: 1)]
	[--max_norm MAX_NORM (default: 1)] 
	[--num_epochs NUM_EPOCHS (default: 1700)] 
	[--lr LR default=0.0031]
	[--model_no MODEL_NO (default: 0 (0: Graph Convolution Network 	(GCN), 1: BERT, 2: XLNet))] 
	[--train TRAIN (default:1)]  
	[--infer INFER (default: 0 (Infer input sentence labels from 	trained model))]
```
The script outputs a results.csv file containing the indexes of the documents in infer.csv and their corresponding predicted labels.

Or if used as a package:
```bash
from nlptoolkit.utils.config import Config
from nlptoolkit.classification.models.BERT.trainer import train_and_fit
from nlptoolkit.classification.models.infer import infer_from_trained

config = Config(task='classification') # loads default argument parameters as above
config.train_data = './data/train.csv' # sets training data path
config.infer_data = './data/infer.csv' # sets infer data path
config.lr = 0.007 # change learning rate
train_and_fit(config) # starts training with configured parameters
inferer = infer_from_trained(config) # initiate infer object, which loads the model for inference, after training model
inferer.infer_from_input()
inferer.infer_from_file(in_file="./data/input.txt", out_file="./data/output.txt")
```

## 2) Automatic Speech Recognition
Automatic Speech Recognition (ASR) aims to convert audio signals into text. This library contains the following models for ASR: 
1. Speech-Transformer
2. Listen-Attend-Spell (LAS)

### Format of dataset files
The folder containing the dataset should have the following structure: folder/speaker/chapter
Within the chapter subdirectory, the audio files (in .flac format) are named speaker-chapter-file_id (file_id In running order)
The transcript .txt file for the files within the chapter should be located in the chapter subdirectory. In the transcript file, each row should consist of the speaker-chapter-file_id (space) transcript.

### Running the model
Run speech.py with arguments below

```bash
speech.py [-h] 
	[--folder FOLDER (default: train-clean-5")] 
	[--level LEVEL (default: word")]   
	[--use_lg_mels USE_LG_MELS (default: 1)]
	[--use_conv USE_CONV (default: 1)]
	[--n_mels N_MELS (default: 80)]
	[--n_mfcc N_MFCC (default: 13)]
	[--n_fft N_FFT (default: 25)]
	[--hop_length HOP_LENGTH (default: 10)]
	[--max_frame_len MAX_FRAME_LEN (default: 1000)]
	[--d_model D_MODEL (default: 64)]
	[--ff_dim FF_DIM (default: 128)]
	[--num NUM (default: 6)]
	[--n_heads N_HEADS(default: 4)]
	[--batch_size BATCH_SIZE (default: 30)]
	[--num_epochs NUM_EPOCHS (default: 8000)] 
	[--lr LR default=0.003]    
	[--gradient_acc_steps GRADIENT_ACC_STEPS (default: 4)]
	[--max_norm MAX_NORM (default: 1)] 
	[--model_no MODEL_NO (default: 0 (0: Transformer, 1: LAS))]  
	[--train TRAIN (default:1)]  
	[--infer INFER (default: 0 (Infer input sentence labels from 	trained model))]

```


## 3) Text Summarization
Text summarization aims to distil a paragraph chunk into a few sentences that capture the essential information. This library contains the following models for text summarization: 
1. Convolutional Transformer 
2. Seq2Seq (LAS architecture)

### Format of dataset files
One .csv file for each text/summary pair. Within the text/summary .csv file, text is followed by summary, with summary points annotated by @highlights (summary) 

### Running the model
Run summarize.py with arguments below

```bash
summarize.py [-h] 
	[--data_path DATA_PATH] 
	[--level LEVEL (default: bpe")]   
	[--bpe_word_ratio BPE_WORD_RATIO (default: 0.7)]
	[--bpe_vocab_size BPE_VOCAB_SIZE (default: 7000)]
	[--max_features_length MAX_FEATURES_LENGTH (default: 200)]
	[--d_model D_MODEL (default: 128)]
	[--ff_dim FF_DIM (default: 128)]
	[--num NUM (default: 6)]
	[--n_heads N_HEADS(default: 4)]
	[--LAS_embed_dim LAS_EMBED_DIM (default: 128)]
	[--LAS_hidden_size LAS_HIDDEN_SIZE (default: 128)]
	[--batch_size BATCH_SIZE (default: 30)]
	[--num_epochs NUM_EPOCHS (default: 8000)] 
	[--lr LR default=0.003]    
	[--gradient_acc_steps GRADIENT_ACC_STEPS (default: 4)]
	[--max_norm MAX_NORM (default: 1)] 
	[--model_no MODEL_NO (default: 0 (0: Transformer, 1: LAS))]  
	[--train TRAIN (default:1)]  
	[--infer INFER (default: 0 (Infer input sentence labels from 	trained model))]

```

## 4) Machine Translation
The goal of machine translation is to translate text from one form of language to another. This library contains the following models to accomplish this:
1. Transformer

Currently supports translation between: English (en), French (fr), Chinese (zh)

### Format of dataset files
A source .txt file with each line containing the text/sentence to be translated, and a target .txt file with each line containing the corresponding translated text/sentence

### Running the model
Run translate.py with arguments below

```bash
translate.py [-h]  
	[--src_path SRC_PATH]
	[--trg_path TRG_PATH] 
	[--src_lang SRC_LANG] 
	[--trg_lang TRG_LANG] 
	[--batch_size BATCH_SIZE (default: 50)]
	[--d_model D_MODEL (default: 512)]
	[--ff_dim FF_DIM (default: 2048)]
	[--num NUM (default: 6)]
	[--n_heads N_HEADS(default: 8)]
	[--max_encoder_len MAX_ENCODER_LEN (default: 80)]
	[--max_decoder_len MAX_DECODER_LEN (default: 80)]	
	[--num_epochs NUM_EPOCHS (default: 500)] 
	[--lr LR default=0.0001]    
	[--gradient_acc_steps GRADIENT_ACC_STEPS (default: 1)]
	[--max_norm MAX_NORM (default: 1)] 
	[--model_no MODEL_NO (default: 0 (0: Transformer))]  
	[--train TRAIN (default:1)]  
	[--evaluate EVALUATE (default:0)]
	[--infer INFER (default: 0)]
	
```

## 5) Natural Language Generation
Natural Language generation (NLG) aims to generate text based on past context. For instance, a chatbot can generate text replies based on the context of chat history. We currently have the following models for NLG:
1. Generative Pre-trained Transformer (GPT/GPT-2)

### Format of dataset files
1. Generate free text from GPT/GPT-2 pre-trained models

### Running the model
Run generate.py

```bash
generate.py
```

## 6) Punctuation Restoration
Given unpunctuated (and perhaps un-capitalized) text, punctuation restoration aims to restore the punctuation of the text for easier readability. Applications include punctuating raw transcripts from audio speech data etc.

### Format of dataset files
Currently only supports TED talk transcripts format, whereby punctuated text is annotated by "<transcripts>" (ignore the ") tags. Eg. "<transcript>" "<punctuated text>" "</transcript>". The "<punctuated text>" is preprocessed and then used for training.

### Running the model
Run punctuate.py

```bash
punctuate.py [-h] 
	[--data_path DATA_PATH] 
	[--level LEVEL (default: bpe")]   
	[--bpe_word_ratio BPE_WORD_RATIO (default: 0.7)]
	[--bpe_vocab_size BPE_VOCAB_SIZE (default: 7000)]
	[--batch_size BATCH_SIZE (default: 32)]
	[--d_model D_MODEL (default: 512)]
	[--ff_dim FF_DIM (default: 2048)]
	[--num NUM (default: 6)]
	[--n_heads N_HEADS(default: 8)]
	[--max_encoder_len MAX_ENCODER_LEN (default: 80)]
	[--max_decoder_len MAX_DECODER_LEN (default: 80)]	
	[--LAS_embed_dim LAS_EMBED_DIM (default: 512)]
	[--LAS_hidden_size LAS_HIDDEN_SIZE (default: 512)]
	[--num_epochs NUM_EPOCHS (default: 500)] 
	[--lr LR default=0.0005]    
	[--gradient_acc_steps GRADIENT_ACC_STEPS (default: 2)]
	[--max_norm MAX_NORM (default: 1.0)] 
	[--T_max T_MAX (default: 5000)] 
	[--model_no MODEL_NO (default: 0 (0: Transformer))]  
	[--train TRAIN (default:1)]  
	[--infer INFER (default: 0 (Infer input sentence labels from 	trained model))]


```

## 7) Named Entity Recognition
In Named entity recognition (NER), the task is to recognise entities such as persons, organisations. Current models for this task: BERT

### Format of dataset files

### Running the model
Run ner.py

```bash
ner.py [-h] 
	[--train_path TRAIN_PATH] 
	[--test_path TEST_PATH]
	[--num_classes NUM_CLASSES]
	[--batch_size BATCH_SIZE]
	[--tokens_length TOKENS_LENGTH]
	[--max_steps MAX_STEPS]
	[--warmup_steps WARMUP_STEPS]
	[--weight_decay WEIGHT_DECAY]
	[--adam_epsilon ADAM_EPSILON]
	[--gradient_acc_steps GRADIENT_ACC_STEPS]
	[--num_epochs NUM_EPOCHS]
	[--lr LR]
	[--model_no MODEL_NO]
	[--model_type MODEL_TYPE]
	[--train TRAIN (default:1)]  
	[--evaluate EVALUATE (default:0)]
```

Or if used as a package:
```bash
from nlptoolkit.utils.config import Config
from nlptoolkit.ner.trainer import train_and_fit
from nlptoolkit.ner.infer import infer_from_trained

config = Config(task='ner') # loads default argument parameters as above
config.train_path = './data/ner/conll2003/eng.train.txt' # sets training data path
config.test_path = './data/ner/conll2003/eng.testa.txt' # sets test data path
config.lr = 0.007 # change learning rate
train_and_fit(config) # starts training with configured parameters
inferer = infer_from_trained(config) # initiate infer object, which loads the model for inference, after training model
inferer.infer_from_input()
inferer.infer_from_file(in_file="./data/input.txt", out_file="./data/output.txt")
```

# Benchmark Results

## 1) Classification (IMDB dataset : 25000 train, 25000 test data points)

### Fine-tuned XLNet English Model (12-layer, 768-hidden, 12-heads, 110M parameters)  
![](https://github.com/plkmo/NLP_Toolkit/blob/master/results/imdb/classification/loss_vs_epoch_2.png) 

![](https://github.com/plkmo/NLP_Toolkit/blob/master/results/imdb/classification/accuracy_vs_epoch_2.png) 

### Fine-tuned BERT English Model (12-layer, 768-hidden, 12-heads, 110M parameters)  
![](https://github.com/plkmo/NLP_Toolkit/blob/master/results/imdb/classification/loss_vs_epoch_1.png) 

![](https://github.com/plkmo/NLP_Toolkit/blob/master/results/imdb/classification/accuracy_vs_epoch_1.png) 

## 7) Named Entity Recognition (Conll2003 dataset)

### Fine-tuned BERT English Model (uncased, 12-layer, 768-hidden, 12-heads, 110M parameters)  

![](https://github.com/plkmo/NLP_Toolkit/blob/master/results/conll2003/ner/test_loss_vs_epoch_0.png) 

![](https://github.com/plkmo/NLP_Toolkit/blob/master/results/conll2003/ner/test_Accuracy_vs_epoch_0.png) 


# References
1. Attention Is All You Need, Vaswani et al, https://arxiv.org/abs/1706.03762
2. Graph Convolutional Networks for Text Classification, Liang Yao et al, https://arxiv.org/abs/1809.05679
3. Speech-Transformer: A No-Recurrence Sequence-To-Sequence Model For Speech Recognition, Linhao Dong et al, https://ieeexplore.ieee.org/document/8462506
4. Listen,Attend and Spell, William Chan et al, https://arxiv.org/abs/1508.01211

# To do list
- Include package usage info for translation, ASR, pos, summarization, punctuation_restoration, generation
- Include benchmark results for all tasks
- Include more models for punctuation restoration, translation, NER
- Include demo for trained models for ASR, punctuation restoration, NER, summarization, translation, classification

