def laplace_avg(count, total, dimension=2, smoothing=1):
    avg = (float(count) + smoothing)/(total + dimension*smoothing)
    return avg

def wordcount(linebuffer):
    res = {}
    for line in linebuffer:
        words = line.split()
        for word in words:
            word = word.strip()
            try:
                res[word] = res[word] + 1
            except KeyError:
                res[word] = 1
    return res

class SpamFilter:
    def __init__(self, d = {}, prior_spam = 0.5):
        self.conditionals = d
        self.prior_spam = prior_spam

    def train(self, spamfile, hamfile):
        with open(spamfile, 'r') as f:
            spamlines = f.readlines()
        with open(hamfile, 'r') as f:
            hamlines = f.readlines()

        # calculate prior probability of spam
        # = no. spam messages/total no. messages
        prior_spam = laplace_avg(len(spamlines), len(spamlines) + len(hamlines))

        # all of the rest of this is about  calculating p(word | spam) and p(word | ham) 
        # = in-class wordcount / total wordcount
        spamcounts = wordcount(spamlines)
        hamcounts = wordcount(hamlines)

        # calculate total wordcounts
        SPAMWORDS = sum(spamcounts.values())
        HAMWORDS = sum(hamcounts.values())

        # get size of dictionary (used for laplace smoothing)
        conditionals = {}
        for word in spamcounts:
            conditionals[word] = {}
        for word in hamcounts:
            conditionals[word] = {}
        NUMWORDS = len(conditionals)

        # calculate spammyness and hammyness of all words
        for word in conditionals:
            ham = hamcounts.get(word, 0)
            spam = spamcounts.get(word, 0)
            conditionals[word]["ham"] = laplace_avg(ham, HAMWORDS, NUMWORDS)
            conditionals[word]["spam"] = laplace_avg(spam, SPAMWORDS, NUMWORDS)

        self.conditionals = conditionals
        self.prior_spam = prior_spam

    def spam(self, message):
        tokens = message.split()
        ham = []
        spam = []

        for token in tokens:
            try:
                vals = self.conditionals[token]
            except KeyError:
                continue
            ham.append(vals["ham"])
            spam.append(vals["spam"])

            n = self.prior_spam*reduce(lambda x, y: x*y, spam)
            p = (1 - self.prior_spam)*reduce(lambda x, y: x*y, ham)

        try:
            return n/(n + p)
        except UnboundLocalError:
            return self.prior_spam
        
    def ham(self, message):
        return (1 - self.spam(message))

# HOWTO:
if __name__ == '__main__':
    sf = SpamFilter()
    sf.train('../trainingdata/negatives', '../trainingdata/positives')

    testmessage = "i'm really annoyed with this shit"
    neg = sf.spam(testmessage)
    print "message:", testmessage, "--- negative:", (neg > 0.5)

    testmessage = "i'm very pleased with the current affairs"
    neg = sf.spam(testmessage)
    print "message:", testmessage, "--- negative:", (neg > 0.5)
