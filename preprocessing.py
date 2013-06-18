from sys import stdin, stdout
import json
import string
import re

class Cleaner:
    punctuation = dict((ord(char), None) for char in string.punctuation)
    exclude = [":)", ":-)", ":o)", ":]", ":3", ":c)", ":>", "=]", "8)", "=)",
    ":}", ":^)", ":-d", ":d", "8-d", "8d", "x-d", "xd", "X-d", "xd", "=-d",
    "=d", "=-3", "=3", ">:[", ":-(", ":(", ":-c", ":c", ":-<",  ":<", ":-[",
    ":[", ":{", "d:<", "d:", "d8", "d;", "d=", "dx", "v.v", "d-':", ":p", "rt"]
    regex = re.compile('[%s]' % re.escape(string.punctuation))

    @staticmethod
    def wash(s):
        s = s.strip()
        s = s.lower()
        words = s.split()
        newstring = []
        for word in words:
            if word not in Cleaner.exclude and not word.startswith('@'):
                newstring.append(word)
        s = ' '.join(newstring)
        s = Cleaner.regex.sub('', s)

        return s

if __name__ == '__main__':
    for line in stdin:
        try:
            # extract text only
            tweet = json.loads(line)
            s = tweet['text']

            s = Cleaner.wash(s)

            if s != '':
                print s
        except:
            continue

