if __name__ == '__main__':
    from sys import stdin

    l = []
    for line in stdin:
        l.append(line)

    unique = set(l)

    for line in unique:
        print line
