from optparse import OptionParser

class TestClass:

    def __init__(self):
        pass

    def opt_arg(self):
        parser = OptionParser(usage="usage: %prog [options] filename",
                          version="%prog 1.0")
        parser.add_option("-b", "--boolean",
                          action="store_true",
                          dest="flag",
                          default=False,
                          help="some flag to test")
        parser.add_option("-w", "--word",
                          action="store", # optional because action defaults to "store"
                          dest="word",
                          default="Hello",
                          help="Just a simple string",)
        (options, args) = parser.parse_args()

        #if len(args) != 2:
        #    parser.error("wrong number of arguments")

        print options
        print args

if __name__ == '__main__':

    test = TestClass()
    test.opt_arg()
