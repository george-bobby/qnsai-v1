import numpy as np
import nltk as nlp


class SubjectiveTest:

    def __init__(self, data, noOfQues):
        self.question_pattern = [
            "Explain in detail ",
            "Define ",
            "Write a short note on ",
            "What do you mean by "
        ]

        self.grammar = r"""
            CHUNK: {<NN>+<IN|DT>*<NN>+}
            {<NN>+<IN|DT>*<NNP>+}
            {<NNP>+<NNS>*}
        """
        self.summary = data
        self.noOfQues = noOfQues

    @staticmethod
    def word_tokenizer(sequence):
        word_tokens = list()
        for sent in nlp.sent_tokenize(sequence):
            for w in nlp.word_tokenize(sent):
                word_tokens.append(w)
        return word_tokens

    @staticmethod
    def create_vector(answer_tokens, tokens):
        return np.array([1 if tok in answer_tokens else 0 for tok in tokens])

    @staticmethod
    def cosine_similarity_score(vector1, vector2):
        def vector_value(vector):
            return np.sqrt(np.sum(np.square(vector)))
        v1 = vector_value(vector1)
        v2 = vector_value(vector2)
        if v1 == 0 or v2 == 0:  # Handle the case where vectors have zero magnitude
            return 0
        return (np.dot(vector1, vector2) / (v1 * v2)) * 100

    def generate_test(self):
        sentences = nlp.sent_tokenize(self.summary)
        print(f"Sentences: {sentences}")  # Debugging statement

        cp = nlp.RegexpParser(self.grammar)
        question_answer_dict = dict()

        for sentence in sentences:
            tagged_words = nlp.pos_tag(nlp.word_tokenize(sentence))
            print(f"Tagged words: {tagged_words}")  # Debugging statement

            tree = cp.parse(tagged_words)
            print(f"Parsed tree: {tree}")  # Debugging statement

            for subtree in tree.subtrees():
                if subtree.label() == "CHUNK":
                    temp = " ".join([sub[0] for sub in subtree])
                    temp = temp.strip().upper()
                    if temp not in question_answer_dict:
                        if len(nlp.word_tokenize(sentence)) > 20:
                            question_answer_dict[temp] = sentence
                    else:
                        question_answer_dict[temp] += sentence

        # Debugging statement
        print(f"Question-Answer Dictionary: {question_answer_dict}")

        keyword_list = list(question_answer_dict.keys())
        print(f"Keyword List: {keyword_list}")  # Debugging statement

        if len(keyword_list) == 0:
            raise ValueError(
                "No valid keywords found, cannot generate questions")

        question_answer = list()
        for _ in range(int(self.noOfQues)):
            if len(keyword_list) == 0:
                raise ValueError("Not enough keywords to generate questions")
            rand_num = np.random.randint(0, len(keyword_list))
            selected_key = keyword_list[rand_num]
            answer = question_answer_dict[selected_key]
            # Ensure rand_num is within valid range
            rand_num %= len(self.question_pattern)
            question = self.question_pattern[rand_num] + selected_key + "."
            question_answer.append({"Question": question, "Answer": answer})

        que = []
        ans = []
        while len(que) < int(self.noOfQues):
            if len(question_answer) == 0:
                raise ValueError(
                    "Not enough question-answer pairs to satisfy the requested number")
            rand_num = np.random.randint(0, len(question_answer))
            if question_answer[rand_num]["Question"] not in que:
                que.append(question_answer[rand_num]["Question"])
                ans.append(question_answer[rand_num]["Answer"])

        return que, ans


# ===================================================================================================

# import numpy as np
# import nltk as nlp

# class SubjectiveTest:

#     def __init__(self, data, noOfQues):

#         self.question_pattern = [
#             "Explain in detail ",
#             "Define ",
#             "Write a short note on ",
#             "What do you mean by "
#         ]

#         self.grammar = r"""
#             CHUNK: {<NN>+<IN|DT>*<NN>+}
#             {<NN>+<IN|DT>*<NNP>+}
#             {<NNP>+<NNS>*}
#         """
#         self.summary = data
#         self.noOfQues = noOfQues

#     @staticmethod
#     def word_tokenizer(sequence):
#         word_tokens = list()
#         for sent in nlp.sent_tokenize(sequence):
#             for w in nlp.word_tokenize(sent):
#                 word_tokens.append(w)
#         return word_tokens

#     def create_vector(answer_tokens, tokens):
#         return np.array([1 if tok in answer_tokens else 0 for tok in tokens])

#     def cosine_similarity_score(vector1, vector2):
#         def vector_value(vector):
#             return np.sqrt(np.sum(np.square(vector)))
#         v1 = vector_value(vector1)
#         v2 = vector_value(vector2)
#         v1_v2 = np.dot(vector1, vector2)
#         return (v1_v2 / (v1 * v2)) * 100

#     def generate_test(self):
#         sentences = nlp.sent_tokenize(self.summary)
#         cp = nlp.RegexpParser(self.grammar)
#         question_answer_dict = dict()
#         for sentence in sentences:
#             tagged_words = nlp.pos_tag(nlp.word_tokenize(sentence))
#             tree = cp.parse(tagged_words)
#             for subtree in tree.subtrees():
#                 if subtree.label() == "CHUNK":
#                     temp = ""
#                     for sub in subtree:
#                         temp += sub[0]
#                         temp += " "
#                     temp = temp.strip()
#                     temp = temp.upper()
#                     if temp not in question_answer_dict:
#                         if len(nlp.word_tokenize(sentence)) > 20:
#                             question_answer_dict[temp] = sentence
#                     else:
#                         question_answer_dict[temp] += sentence
#         keyword_list = list(question_answer_dict.keys())
#         question_answer = list()
#         for _ in range(int(self.noOfQues)):
#             rand_num = np.random.randint(0, len(keyword_list))
#             selected_key = keyword_list[rand_num]
#             answer = question_answer_dict[selected_key]
#             rand_num %= 4
#             question = self.question_pattern[rand_num] + selected_key + "."
#             question_answer.append({"Question": question, "Answer": answer})
#         que = list()
#         ans = list()
#         while len(que) < int(self.noOfQues):
#             rand_num = np.random.randint(0, len(question_answer))
#             if question_answer[rand_num]["Question"] not in que:
#                 que.append(question_answer[rand_num]["Question"])
#                 ans.append(question_answer[rand_num]["Answer"])
#             else:
#                 continue
#         return que, ans
