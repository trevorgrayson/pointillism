import argparse
from os.path import expanduser
from graphviz import Source


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file')

    args = parser.parse_args()

    theme = ''

    try: 
        with open(expanduser('~/.point/default.theme'), 'r') as fp:
            theme = fp.read()
    except IOError:
        pass

    with open(args.file, 'r') as fp:

        data = next(fp)
        data += theme
        
        data += fp.read()

        dot = Source(data)
        # dot.format = 'png'

        print(dot.source)
