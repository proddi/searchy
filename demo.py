from searchy import Index
from searchy.tools import NgramWordTokenizer


text = "A week ago we reported a significant drop in index counts within the Google Search Console Index Status reports. At first, I thought it was just a reporting glitch, because it simply impacted virtually every site I looked at (and I have tons of sites that people have shared with me in my Google Search Console account)."


#-----------------------------------------------------------
#   MAIN
#-----------------------------------------------------------

def main(args):
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('terms' , nargs='*', default=["save"], help='search terms')
    options = parser.parse_args(args)

#    index = Index(tokenizer=WhitespaceTokenizer() | LowercaseFilter())
#    index = Index(tokenizer=RegexTokenizer() | LowercaseFilter() | StopFilter() | NGramTokenizer(minsize=2, maxsize=4))
    index = Index(tokenizer=NgramWordTokenizer())

    for i, name in enumerate(["F|A RECRUITING XP SAVE", "F|A SILENT RECRUITING XPS", "[!!!]Hirntot, 6 Map", "(HBC)HELLBASKET ETPro3.2.6", "F|A HARDCORE XPS", "*XP* kernwaffe.de NQ No1", text]):
        index.add(name="#%s: %s" % (i, name), data="server #%s - %s" % (i, name))

    print "="*60
    for data, score in index.query(name=" ".join(options.terms)):
        if score > .025:
            print "- result: %s (%d%%)" % (data, round(score*100))

    print "="*60
    print "index:", index.stats()


if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
