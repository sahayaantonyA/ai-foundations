from collections import defaultdict
from nltk.tokenize import word_tokenize
import re, math, random

class NGramModel:
    def __init__(self,gram: int, corpus_path: str):
        self.n = gram
        self.corpus_path = corpus_path
        self.ngram_count = defaultdict(int)
        self.context_count = defaultdict(int)
        self.vocob = set()
    
    def tokenization(self, corpus_path: str):
        tokens = []
        with open(file= corpus_path, mode= 'r', encoding= 'utf-8') as f:
            for line in f:
                processed_text = re.sub(r'[^a-z\s]','',line.lower())
                tokens.append(word_tokenize(processed_text))
        return tokens
    
    def train(self):
        sentences_tokens = self.tokenization(corpus_path= self.corpus_path)
        for sentence_tokens in sentences_tokens:
            tokens = ['<s>'] * (self.n-1) + sentence_tokens + ['<\s>']
            for i in range(len(tokens) - self.n + 1):
                ngram = tuple(tokens[i:i+self.n])
                context = tuple(tokens[i:i+self.n-1])
                self.ngram_count[ngram] += 1
                self.context_count[context] += 1
            self.vocob.update(tokens)

    def get_prob(self,word):
        context = word[:-1]
        return (self.ngram_count[word] + 1) / (self.context_count[context] + len(self.vocob))

    def compute_perplexity(self,test_corpus_path: str):
        total_log_prob = 0
        total_word_count = 0
        sentences_token = self.tokenization(corpus_path= test_corpus_path)
        for sentence_token in sentences_token:
            token = ['<s>'] * (self.n + 1) + sentence_token + ['</s>']
            sentence_prob = 0
            for i in range(len(token) - self.n + 1):
                ngram = tuple(token[i:i+self.n])
                prob = self.get_prob(word=ngram)
                sentence_prob += math.log(prob)
            total_log_prob += sentence_prob
            total_word_count += len(token)
        return math.exp(-total_log_prob / total_word_count)
    
    def generate_text(self, max_length=10):
        sentence = ["<s>"] * (self.n - 1)
        
        for _ in range(max_length):
            context = tuple(sentence[-(self.n-1):])  # Get the last (n-1) words
            possible_ngrams = {ngram: prob for ngram, prob in self.ngram_count.items() if ngram[:-1] == context}
            
            if not possible_ngrams:
                break  # No valid n-grams left
            
            next_word = random.choices(list(possible_ngrams.keys()), weights=list(possible_ngrams.values()))[0][-1]
            if next_word == "</s>":
                break
            
            sentence.append(next_word)
        
        return " ".join(sentence[self.n-1:]) 

while True:
    ngram_input = int(input("Enter the gram or 0 to exit: "))
    if ngram_input != 0:
        ngram = NGramModel(gram= ngram_input, corpus_path= r'C:\python_projects\ai-foundations\NLP\ex_corpus.txt')
        ngram.train()
        print(f"Model : {ngram_input} Gram")
        perplxity_score = ngram.compute_perplexity(test_corpus_path= r'C:\python_projects\ai-foundations\NLP\test_corpus.txt')
        print("Perplxity Score : ", perplxity_score)
        genertaed_sentence = ngram.generate_text().replace('<\s>','')
        print("Generated Sentence : ", genertaed_sentence)
        print('------------------')
    else:
        break
    