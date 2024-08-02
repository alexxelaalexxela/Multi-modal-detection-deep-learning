

from gingerit.gingerit import GingerIt


text = '''Social media has changed the world. The USA's top doctor said it can cause mental health problems in young people. Dr Vivek Murthy want mental health warnings on social media sites. He said youngsters see too much sexs and violence online. He want warnings that say social media can harm mental health.In Dr Murthy's recent warting, he said: "The mantal health crisis among young people is an emergency." He said young people spend too much time online. He said teenagers "who spend more than three hour a day on social media [could] double the risk of anxiety and depression".'''


parser = GingerIt()
text = "This is an exmple of a text with some erors."
result = parser.parse(text)

print(f"Corrected text: {result['result']}")
for correction in result['corrections']:
    print(f"Error: {correction['text']}")
    print(f"Suggestions: {correction['correct']}")
