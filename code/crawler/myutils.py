import unicodedata
import re
import os

def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    value = unicode(re.sub('[-\s]+', '-', value))
    return value

def insert_doc(title, text, db):
    title = slugify(title)
    file = open(db + title + '.txt', 'w')
    file.write(text.encode('utf8'))
    file.close()

def concat_files(path, filename):
    try:
        os.remove(os.path.join(path, filename))
    except:
        print("input file doesn't exist. ignoring.")

    files = os.listdir(path)
    with open(os.path.join(path, filename), "w") as fo:
        print "outfile:" + filename
        for infile in files:
            print "input file:" + infile
            with open(os.path.join(path, infile)) as fin:
                for line in fin:
                    fo.write(line)
            os.remove(os.path.join(path, infile))