import random

# List of classic Magic 8-Ball responses
responses = [
    "It is certain.",
    "It is decidedly so.",
    "Without a doubt.",
    "Yes definitely.",
    "You may rely on it.",
    "As I see it, yes.",
    "Most likely.",
    "Outlook good.",
    "Yes.",
    "Signs point to yes.",
    "Reply hazy, try again.",
    "Ask again later.",
    "Better not tell you now.",
    "Cannot predict now.",
    "Concentrate and ask again.",
    "Don't count on it.",
    "My reply is no.",
    "My sources say no.",
    "Outlook not so good.",
    "Very doubtful."
]

print("🎱 Welcome to the Magic 8-Ball! 🎱")
print("Ask me a yes/no question, and I'll gaze into the future.")
print("Type 'quit' to exit.\n")

while True:
    question = input("Your question: ").strip()
    
    if question.lower() == "quit":
        print("Goodbye! May the odds be ever in your favor. 🎱")
        break
    
    if question == "":
        print("You must ask a question to get an answer!")
        continue
    
    # Optional: Encourage questions ending with ?
    if not question.endswith("?"):
        print("(Tip: Questions usually end with a '?')")
    
    # Shake the 8-Ball...
    print("Shaking the Magic 8-Ball...")
    
    # Get a random response
    answer = random.choice(responses)
    
    print(f"Magic 8-Ball says: {answer}\n")