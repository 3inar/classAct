if __name__ == '__main__':
    from sys import stdin
    import string
    import re

    regex = re.compile('[%s]' % re.escape(string.punctuation))
    for line in stdin:
        line = line.strip()
        line = line.lower()
        line = regex.sub('', line)
        print line
