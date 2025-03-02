class UnigramModel:
    def __init__(self,corpus_path: str):
        self.corpus_path = corpus_path
    
    def get_tokenized_sentences(self):
        with open(file= self.corpus_path, mode= 'r', encoding= 'utf-8') as f:
            return [sentance.strip().lower().split() for sentance in f]        
        
    def get_words_count(self,tokenized_sentences: list[list[str]]):
        words_count = {}
        for sentence in tokenized_sentences:
            for i in range(len(sentence)):
                w1 = sentence[i]
                if w1 not in words_count:
                    words_count[w1] = 0
                words_count[w1] += 1
        return words_count
    
    def compute_probs(self,words_count: dict):
        return {w1: count/ sum(words_count.values()) for w1, count in words_count.items()}
    
    def generate_next_word(self):
        return max(self.probs,key= self.probs.get)
    
    def build(self):
        tokenized_sentences = self.get_tokenized_sentences()
        words_count = self.get_words_count(tokenized_sentences= tokenized_sentences)
        self.probs = self.compute_probs(words_count= words_count)
        print("Probabilities of All Unigrams: : ",self.probs)
        print("Maxium Probability : ", max(self.probs,key= self.probs.get))
        
model = UnigramModel(corpus_path= 'ex_corpus.txt')
model.build()
print("Predicted Next Word: ", model.generate_next_word())


# in ex_corpus file have a sentences are

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