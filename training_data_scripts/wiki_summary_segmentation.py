import json, pprint

pp = pprint.PrettyPrinter(indent=4)
fname = '/home/sampanna/Downloads/wiki_86.json'

with open(fname) as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]

firstLine = json.loads(content[0])
print pp.pprint(firstLine)

text = firstLine['text']

tokens = text.split('\n\n')

print tokens[1]