class TrigramModel:
    def __init__(self, corpus_path: str):
        self.corpus_path = corpus_path

    def tokenization(self):
        with open(file= self.corpus_path, mode= 'r', encoding= 'utf-8') as file:
            return [line.lower().strip().split() for line in file if line.strip()]    
        
    def get_words_count(self, sentences_tokens: list[list[str]]):
        trigram_count = {}
        for sentence_tokens in sentences_tokens:
            for i in range(len(sentence_tokens) - 2):
                w1, w2, w3 = sentence_tokens[i], sentence_tokens[i+1], sentence_tokens[i+2]
                if w1 not in trigram_count:
                    trigram_count[w1] = {}
                if w2 not in trigram_count[w1]:
                    trigram_count[w1][w2] = {}
                if w3 not in trigram_count[w1][w2]:
                    trigram_count[w1][w2][w3] = 0
                trigram_count[w1][w2][w3] += 1
        return trigram_count
    
    def compute_probs(self, trigram_counts: dict):
        return {w1: {w2: {w3: count / sum(trigram_counts[w1][w2].values())  for w3, count in trigram_counts[w1][w2].items()} for w2 in trigram_counts[w1]}for w1 in trigram_counts}

    def generate_next_word(self, input_query: str):
        input_query = input_query.lower().strip().split()
        if input_query.__len__() >= 2:
            last_two_words = input_query[-2:]
            if last_two_words[-2] in self.trigram_probs and  last_two_words[-1] in self.trigram_probs[last_two_words[-2]]:
                for _ in range(10):
                    if last_two_words[-2] in self.trigram_probs and last_two_words[-1] in self.trigram_probs[last_two_words[-2]]:
                        next_word = max(self.trigram_probs[last_two_words[-2]][last_two_words[-1]], key=self.trigram_probs[last_two_words[-2]][last_two_words[-1]].get)
                        input_query.append(next_word)
                        last_two_words = input_query[-2:]
                for word in input_query:
                    import time
                    print(word, end=' ', flush= True)
                    time.sleep(0.5)
                print()
            else:
                print(f"Sorry, I couldn't find predictions for '{last_two_words[0]}' and '{last_two_words[1]}'. Try another word!") 

        else:
            print("Need at least two words!")

    def build(self):
        tokens = self.tokenization()
        words_count = self.get_words_count(sentences_tokens= tokens)
        self.trigram_probs = self.compute_probs(trigram_counts= words_count)

model = TrigramModel(corpus_path= 'ex_corpus.txt')
model.build()

while True:
    query = input('You: ')
    if query.lower() != 'exit':
        model.generate_next_word(input_query= query)
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