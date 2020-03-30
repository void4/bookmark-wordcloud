import sys
from json import loads
from collections import defaultdict

bms = defaultdict(list)

with open(sys.argv[1]) as f:
	s = f.read()
	j = loads(s)
	
	for cat in j.get("children", []):
		for b in cat.get("children", []):
			if isinstance(b, dict) and "uri" in b and "dateAdded" in b and "lastModified" in b and "title" in b:
				#print(b)
				bms[b.get("uri", "")].append(b.get("title", ""))
				print(b.get("title", None))



print(len(bms))


from collections import Counter
from urllib.parse import urlparse
from tldextract import extract

allowed_schemes = "http https".split()

uris = []
for uri in bms.keys():
	ext = extract(uri)
	cleaned = ext.registered_domain
	uris.append(cleaned)

c = Counter(uris)

print(c.most_common(1000))


from wordcloud import WordCloud

#text = " ".join(" ".join(v) for v in bms.values())
text = " ".join([w.split(".")[0] for w in c.keys()])
wordcloud = WordCloud(width=1920, height=1080).generate(text)
print(wordcloud, dir(wordcloud))
img = wordcloud.to_image()
from time import time

img.save(str(int(time()*1000))+".png")
#img.show()
