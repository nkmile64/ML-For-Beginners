# ##########################################
#            TASK COMMON TO NLP
# ##########################################

# [1] Tokenization: split the text into tokens (or words). Must take into account sentence delimiters and punctuation

# [2] Embeddings: convert your text data numerically so that words with similar meaning (or used together), cluster together.

# [3] Parsing & Part-of-Speech Tagging:

# [4] Word & Phrase Frequencies

# [5] N-grams: sequences of words of a set length (unigram, bigram, trigram etc)

# [6] Noun Phrase Extraction: used for identifying the subject or object of a sentence

# [7] Sentiment Analysis: how positive or negative a sentence is.
# Polarity from -1 (negative) to 1 (positive)
# Objectivity/Subjectivity from 0 (most objective) to 1 (most subjective)

# [8] Inflection: the singular or plural of a word

# [9] Lemmatization: the root for a set of words
# e.g. fly: flew,flies, flying

import random
from textblob import TextBlob
from textblob.np_extractors import ConllExtractor

extractor = ConllExtractor()


def main():
    print("Hello, I am Marvin, the friendly robot.")
    print("You can end this conversation at any time by typing 'bye'")
    print("After typing each answer, press [ENTER]")
    print("How are you today?")

    while True:
        # Wait for the user to enter some text
        user_input = input("> ")

        if user_input.lower() == "bye":
            # If they typed in 'bye', or even 'BYE', 'ByE' etc, break out of the loop
            break
        else:
            # Create a TextBlob based on the user input.
            user_input_blob = TextBlob(user_input, np_extractor=extractor)
            # Then extract the noun phrases.
            np = user_input_blob.noun_phrases
            response = ""

            if user_input_blob.polarity <= -0.5:
                response = "Oh dear, that sounds bad. "
            elif user_input_blob.polarity <= 0:
                response = "Hmm, that's not great. "
            elif user_input_blob.polarity <= 0.5:
                response = "Well, that sounds positive. "
            elif user_input_blob.polarity <= 1:
                response = "Wow, that sounds great. "

            if len(np) != 0:
                # There was at least one noun phrase detected, so ask
                # about that and pluralize it.
                response += f"Can you tell me more about {np[0].pluralize()}?"
            else:
                response += "Can you tell me more?"

            print(response)

    print("It was nice talking to you, goodbye!")


# Start the program
main()
