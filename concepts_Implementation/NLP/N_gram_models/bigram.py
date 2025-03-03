class BigramModel:
    def __init__(self, corpus_path: str):
        self.corpus_path = corpus_path

    def tokenization(self):
        with open(file= self.corpus_path, mode= 'r', encoding= 'utf-8') as file:
            return [line.lower().strip().split() for line in file if line.strip()]    
    
    def get_words_count(self,sentences_tokens: list[list[str]]):
        from collections import Counter
        unique_word_count = Counter(word for sentence in sentences_tokens for word in sentence)
        bigram_count = {}
        for sentence_tokens in sentences_tokens:
            for i in range(len(sentence_tokens) - 1):
                w1,w2 = sentence_tokens[i], sentence_tokens[i+1]
                if w1 not in bigram_count:
                    bigram_count[w1] = {}
                if w2 not in bigram_count[w1]:
                    bigram_count[w1][w2] = 0
                bigram_count[w1][w2] += 1
        return unique_word_count, bigram_count
    
    def compute_probs(self, unique_word_count: dict, bigram_counts: dict):
        return {w1 : {w2 : count/unique_word_count[w1] for w2, count in w2_count.items()} for w1, w2_count in bigram_counts.items()}

    def generate_next_words(self,input_query: str):
        import time
        input_query = input_query.lower().strip().split()
        last_word = input_query[-1]
        if last_word in self.bigram_probs:
            for _ in range(10):
                if last_word in self.bigram_probs:
                    next_word = max(self.bigram_probs[input_query[-1]], key= self.bigram_probs[input_query[-1]].get)
                    input_query.append(next_word)
                    last_word = next_word
            for word in input_query:
                print(word, end=' ', flush= True)
                time.sleep(0.5)
            print()
        else:
            print(f"Sorry, I couldn't find predictions for '{last_word}'. Try another word!") 

    def build(self):
        sentences = self.tokenization()
        unique_word_count, bigram_counts = self.get_words_count(sentences_tokens= sentences)
        self.bigram_probs = self.compute_probs(unique_word_count= unique_word_count, bigram_counts= bigram_counts)
        print("Bigram Probs: ", self.bigram_probs)

model = BigramModel(corpus_path= 'ex_corpus.txt')
model.build()

while True:
    query = input('You: ')
    if query.lower() != 'exit':
        model.generate_next_words(input_query= query)
    else:
        break


# in ex_corpus.txt file contains the following sentences:

'''
The cat sat on the mat.
Dogs are great companions.
I love to play with my dog.
Cats are independent animals.
Pets bring joy to families.
The sun is shining brightly today.
I enjoy reading books in the park.
The weather is nice for a walk.
She loves to cook delicious meals.
He plays soccer every weekend.

'''