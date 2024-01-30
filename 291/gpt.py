from openai import OpenAI

key = ""
with open("./GPT_KEY.txt") as f:
    key = f.read()

client = OpenAI(api_key=key)

comments = [
    "Great coffe",
    "That coffe is tasty",
    "Where did u buy this?",
    "What a great drink",
]

response = client.completions.create(
    model="gpt-3.5-turbo-instruct",
    prompt=f"Write a short comment that is related to those comments :{comments}",
)
print(response.choices[0].text)
