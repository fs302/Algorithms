# Understand BERT - Bidirectional Encoder Representations from Transformers

BERT is a pre-train model published by researchers at Google AI Language team. It suggests we divide language understanding task into two phases: pre-training and fine-tune, while BERT do the hard things to provide a word embedding that understand language deeply, what you need is to apply downstream task-specific learning with little computational resources.

![BERT](./BERT-framework.jpg)

## How to train BERT(Pre-train)

In order to learn the context of words. BERT uses two training strategies: Masked LM and ext Sentence Prediction.When training the BERT model, Masked LM and Next Sentence Prediction are trained together, with the goal of minimizing the combined loss function of the two strategies.

### Masked Language Model(MLM)

Before feeding word sequences into BERT, 15% of the words in each sequence are replaced with a [MASK] token.The model then attempts to predict the original value of the masked words, based on the context provided by the other, non-masked, words in the sequence.

### Next Sentence Prediction(NSP)

The model receives pairs of sentences as input and learns to predict if the second sentence in the pair is the subsequent sentence in the original document.

## How to use BERT(Fine-tuning)

By adding a small layer to the core model, we can apply BERT to a wide variety of language tasks. For example, Sentiment Analysis, Question Answering and Name Entity Recognition.