# tokens = ['the', 'cat', 'in', 'the', 'hat']
# tokens = [None, 'the']
# sequences = [['the', 'cat', 'runs'], ['the', 'dog', 'runs']]
# word_counts = {'cat': 3, 'dog': 2, 'mouse': 1, 'cow': 4}
# distribution = {'cat': 0.3, 'dog': 0.2, 'mouse': 0.1, 'cow': 0.4}

# from corpus import tokenize

"""for def train.counts"""


def get_ngrams(tokens, n):
    tokens = [None] * (n - 1) + tokens + [None] * (n - 1)
    sequences = []

    for i in range(len(tokens)):
        if i < len(tokens) - n + 1:
            n_gram = tokens[i: i + n]
            sequences.append(n_gram)

    return sequences


"""for def p_next"""


def normalize(word_counts):
    probabilities = {}
    total = 0
    for i in word_counts:
        total += word_counts[i]

    for i in word_counts:
        probabilities[i] = word_counts[i] / total
    return probabilities


"""for def generate"""


def sample(distribution):
    # print(distribution)
    """
    {'cat':0.3, 'dog':0.2, 'mouse':0.1,'cow':0.4} =>
        [['cat', 0.3], ['dog', 0.2], ['mouse', 0.1], ['cow', 0.4]]
    """

    import random
    list = []
    for i in distribution:
        lst = [i, distribution[i]]
        list.append(lst)

    """Generate a random float in [0, 1]
       Define which interval([0, 0.3] or
       [0.3, 0.3 + 0.2] or
       [0.3 + 0.2, 0.3 + 0.2 + 0.1] or
       [0.3 + 0.2 + 0.1, 0.3 + 0.2 + 0.1 + 0.4])
       the float falls in"""
    a = 0
    b = list[0][1]
    random_p = random.random()
    for j in range(0, len(distribution)):
        if a <= random_p <= b:
            return list[j][0]
            break
        else:
            if j < len(distribution) - 1:
                a += list[j][1]
                b = a + list[j + 1][1]


class LanguageModel:
    def __init__(self, n):
        self.n = n
        self.vocabulary = set()
        self.counts = {}

    def train(self, sequences):
        # print(sequences)

        """self.vocabulary"""
        self.vocabulary.add(None)
        for i in sequences:
            for j in i:
                self.vocabulary.add(j)

        if self.n == 1:
            for i in sequences:
                for j in i:
                    if j in self.counts:
                        self.counts[j] += 1
                    else:
                        self.counts[j] = 1

        else:
            """self.counts"""
            ngram_list = []
            for i in sequences:
                a = tuple(get_ngrams(i, self.n))
                ngram_list += a

            """
            ngram_list contain a list of n_gram.
            for each n_gram in the list, W1~Wn-1 is key, Wn and it's count is value.
            """

            for i in range(0, len(ngram_list)):
                value = {}

                key = tuple(ngram_list[i][0:-1])
                # print(key)
                value[ngram_list[i][-1]] = 1

                """if there are more than two [None, None] in ngram_list[0:n-1]
                than the value of key should be either more than two item,
                or one item's value more than 1."""

                # print(self.counts)
                if key in self.counts:
                    if i + 1 < len(ngram_list):
                        if ngram_list[i][-1] in self.counts[key]:
                            value[ngram_list[i][-1]] += 1
                            self.counts[key] = value
                        else:
                            self.counts[key][ngram_list[i][-1]] = 1
                else:
                    self.counts[key] = value
                    # print(self.counts)

    def p_next(self, tokens):
        # print('p_next:',tokens)
        if tuple(tokens) in self.counts:
            return normalize(self.counts[tuple(tokens)])
        else:
            return None

    def generate(self):
        import random
        if self.n == 1:
            next_token = sample(normalize(self.counts))
            while next_token in {',', '.', '!', '?'}:
                next_token = sample(normalize(self.counts))
            predict = [next_token]
            while next_token not in {'.', '!', '?'}:
                next_token = sample(normalize(self.counts))
                predict.append(next_token)
            # print(predict)
            return predict

        else:
            sentence_heads = random.choice(list(self.counts.keys()))
            while True:
                if sentence_heads[0] is not None:
                    sentence_heads = random.choice(list(self.counts.keys()))
                else:
                    break
            predict = list(sentence_heads)
            next_token = sample(self.p_next(sentence_heads))
            # print(next_token)
            while next_token is not None:
                predict.append(next_token)
                # print(predict)
                if self.n == 1:
                    sentence_heads = predict[-1]
                    a = sentence_heads.split()
                    next_token = sample(self.p_next(tuple(a)))
                else:
                    sentence_heads = predict[- self.n + 1:]
                    next_token = sample(self.p_next(sentence_heads))
            return predict
