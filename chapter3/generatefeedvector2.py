import feedparser
import re

# Returns title and dictionary of word counts for an RSS feed
def getwordcounts(url):
  # Parse the feed
  d=feedparser.parse(url)
  entries_wc={}

  # Loop over all the entries
  for e in d.entries:
    if 'summary' in e: summary=e.summary
    else: summary=e.description

    entries_wc[e.title] = {}

    # Extract a list of words
    words=getwords(e.title+' '+summary)
    for word in words:
      entries_wc[e.title].setdefault(word,0)
      entries_wc[e.title][word]+=1
  return d.feed.title,entries_wc

def getwords(html):
  # Remove all the HTML tags
  txt=re.compile(r'<[^>]+>').sub('',html)

  # Split words by all non-alpha characters
  words=re.compile(r'[^A-Z^a-z]+').split(txt)

  # Convert to lowercase
  return [word.lower() for word in words if word!='']


# word count appears in blogs
apcount={}
wordcounts={}
feedlist=[line for line in file('feedlist.txt')]
for feedurl in feedlist:
  try:
    title,entries_wc=getwordcounts(feedurl)
    for entry,wc in entries_wc.items():
      wordcounts["%s:%s" % (title,entry)]=wc
      for word,count in wc.items():
        apcount.setdefault(word,0)
        if count>1:
          apcount[word]+=1
  except:
    print 'Failed to parse feed %s' % feedurl.strip()

wordlist=[]
for w,bc in apcount.items():
  frac=float(bc)/len(feedlist)
  # only consider the words between 10% - 50%
  # not considering the words like 'the', and 'film-flam'
  if frac>0.1 and frac<0.5:
    wordlist.append(w)

out=file('blogdata2.txt','w')
out.write('Blog')
for word in wordlist: out.write('\t%s' % word)
out.write('\n')
for blog,wc in wordcounts.items():
  print blog
  try:
    out.write(blog)
    for word in wordlist:
      if word in wc: out.write('\t%d' % wc[word])
      else: out.write('\t0')
    out.write('\n')
  except:
    pass
