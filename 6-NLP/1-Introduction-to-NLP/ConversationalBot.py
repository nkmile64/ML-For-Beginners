# This bot will have one ability only: to keep the conversation
# going with random responses that might work in almost
# any trivial conversation.
import random

# List containing the random responses (you can add your or translate them
# into your own language too)
random_responses = [
    "That is quite interesting, please tell me more.",
    "I see. Do go on.",
    "Why do you say that?",
    "Funny weather we've been having, isn't it?",
    "Let's change the subject.",
    "Did you catch the game last night?",
]

# 1. Print instructions advising the user how to interact with the bot.
print("------------------------------------------------------------")
print("Hello, I am Marvin, the simple robot.")
print("You can end this conversation at any type by typing 'bye'")
print("After typing each answer, press [ENTER]")
print("How are you today:")
print("------------------------------------------------------------")

# 2. Start a loop
while True:
    # 2.1 Accept user input
    user_input = input("> ")
    #  2.2 If user has asked to exit, then exit
    if user_input.lower() == "bye":
        break
    else:
        # 2.3 Process user input and determine response (a random choice
        # from a list of possible generic responses)
        response = random.choices(random_responses)[0]
    # 2.4 Print response
    print(response)
# 3. Loop back to step 2

print("It was nice talking to you, goodbye!")
