import sys
import urllib
from BeautifulSoup import BeautifulSoup


def print_definition(word):
    url = "http://www.dictionary.com/browse/%s?s=t" % word.replace(' ', '-')

    html = urllib.urlopen(url).read()
    bs = BeautifulSoup(html)

    print '+ Definition of %s:' % word

    s = str(bs.findAll('div')[21])
    init = s.find('class="def-content"') + 30
    end = init + s[init:].find('/div') - 1
    s = s[init:end]

    s = s.replace('  ', '')
    s = s.replace('(', '')
    s = s.replace(')', '')

    if 'main-area' in s:
        print 'Could not find definition.\n'
        return

    if '<' not in s:
        print '%s\n' % s
    else:
        left = []
        right = []
        for i in range(len(s)):
            if s[i] == '<':
                left.append(i)
            elif s[i] == '>':
                right.append(i+1)

        final = s[:left[0]]
        for i in range(len(left) - 1):
            final += s[right[i]:left[i + 1]]
        final += s[right[len(right) - 1]:]

        print '%s\n' % final


def print_version():
    print "+ pydef V1.0 by Brendan McCloskey"


def print_help():
    print_version()
    print "+ COMMANDS\n---------"
    print "+ [-v] [--version]     : Print version"
    print "+ [-h] [--help]        : Print help"
    print "+ [<word>]             : Define <word>"


if len(sys.argv) == 0:
    print_help()
else:
    i = 1
    while i < len(sys.argv):
        if '-' in sys.argv[i]:
            if '-h' == sys.argv[i] or '--help' == sys.argv[i]: print_help()
            elif '-v' == sys.argv[i] or '--version' == sys.argv[i]: print_version()
        else:
            if '"' == sys.argv[i][0]:
                words = sys.argv[i][1:]
                while i < len(sys.argv) and '"' != sys.argv[i][len(sys.argv[i])-1]:
                    words.append(" " + sys.argv[i])
                    i += 1
                if len(words) != len(sys.argv[i]) - 1: words.append(" " + sys.argv[i][:-1])
                print_definition(words)
            else:
                print_definition(sys.argv[i])
        i += 1
