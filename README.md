# NLP Toolkit
Library containing state-of-the-art models for Natural Language Processing tasks

## Tasks
1. Classification
2. Automatic Speech Recognition
3. Text Summarization
4. Machine Translation

## 1) Classification
The goal of classification is to segregate documents into appropriate classes based on their text content. Currently, the classification toolkit uses text-based Graph Convolution Networks (GCN) and Bidirectional Encoder Representations from Transformers (BERT).

### Format of datasets files
The training data (default: train.csv) should be formatted into two columns �text� and �label� respectively, with rows being the documents index. �text� contains the raw text and �label� contains the corresponding label (integers 0, 1, 2� depending on the number of classes)

The infer data (default: infer.csv) should be formatted into at least one column �text� being the raw text and rows being the documents index. Optional column �label� can be added and --train_test_split argument set to 1 to use infer.csv as the test set for model verification.

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
```
The script outputs a results.csv file containing the indexes of the documents in infer.csv and their corresponding predicted labels.

## 2) Automatic Speech Recognition
Automatic Speech Recognition (ASR) aims to convert audio signals into text. This library contains the following models for ASR: Speech-Transformer, Listen-Attend-Spell (LAS).

### Format of dataset files
The folder containing the dataset should have the following structure: folder/speaker/chapter
Within the chapter subdirectory, the audio files (in .flac format) are named speaker-chapter-file_id (file_id In running order)
The transcript .txt file for the files within the chapter should be located in the chapter subdirectory. In the transcript file, each row should consist of the speaker-chapter-file_id (space) transcript.

### Running the model
Run speech.py with arguments below

```bash
speech.py [-h] 
	[--folder FOLDER (default: train-clean-5")] 
	[--level LEVEL (default: �word")]   
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
```


## 3) Summarization
Text summarization aims to distill a paragraph chunk into a few sentences that capture the essential information. This library contains the following models for text summarization: Convolutional Transformer, Seq2Seq (LAS architecture)

### Format of dataset files
One .csv file for each text/summary pair. Within the text/summary .csv file, text is followed by summary, with summary points annotated by @highlights (summary) 

### Running the model
Run summarize.py with arguments below

```bash
summarize.py [-h] 
	[--data_path DATA_PATH] 
	[--level LEVEL (default: �bpe")]   
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
```

## 4) Machine Translation
The goal of machine translation is to translate text from one form of language to another. This library contains the Transformer model to accomplish this.

### Format of dataset files
A source .txt file with each line containing the text/sentence to be translated, and a target .txt file with each line containing the corresponding translated text/sentence

### Running the model
Run translate.py with arguments below

```bash
translate.py [-h] 
	[--src_path SRC_PATH]
	[--trg_path TRG_PATH] 
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
```

