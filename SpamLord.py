"""
This program was adapted from the Stanford NLP class SpamLord homework assignment.
Please do not make this code or the data public.
This version has no patterns, but has two patterns suggested in comments.
"""
import sys
import os
import re
import pprint

"""
TODO
For Part 1 of our assignment, add to these two lists of patterns to match
examples of obscured email addresses and phone numbers in the text.
For optional Part 3, you may need to add other lists of patterns.
"""
# email .edu patterns

# each regular expression pattern should have exactly two sets of parentheses.
#   the first parenthesis should be around the someone part
#   the second parenthesis should be around the somewhere part
#   in an email address whose standard form is someone@somewhere.edu
epatterns = []
epatterns.append('([A-Za-z.]+)@([A-Za-z.]+)\.edu')
epatterns.append('([A-Za-z.]+) @ ([A-Za-z.]+)\.edu')
epatterns.append('([A-Za-z.]+)  @  ([A-Za-z.]+)\.edu')  #dabo
epatterns.append('([A-Za-z.]+)@([A-Za-z.]+)\.EDU')   #cheriton
epatterns.append('([A-Za-z.]+) AT ([A-Za-z.]+) DOT edu') #subh
epatterns.append('([A-Za-z.]+)\s<at symbol>\s([A-Za-z.]+)\.edu')    #manning
epatterns.append('([A-Za-z.]+)&#x40;([A-Za-z.]+)\.edu')         #levoy
epatterns.append('([A-Za-z.]+)<del>@([A-Za-z.]+)\.edu')   #latombe
epatterns.append('([A-Za-z.]+) WHERE ([A-Za-z.]+) DOM edu')       #engler
epatterns.append('([A-Za-z.]+) [at]+ ([A-Za-z.]+)\.edu')  #lam increases fp by 2 jure n plotkin

#epatterns.append('([A-Za-z.]+) [at]+ ([A-Za-z.]+)\.edu\s[A-Za-z.]+\s\d+')
#epatterns.append('([A-Za-z.]+) at ([A-Za-z;]+)edu')   #jks
#epatterns.append('([A-Za-z\-]+)\-@\-([A-Za-z\-]+)\.\-e\-d\-u')   #dlwh
#epatterns.append('([A-Za-z.]+) [at]+ ([A-Za-z.]+) [dt]+ com')
#epatterns.append('([A-Za-z.]+) at ([A-Za-z.]+) standford edu')   #pal
#epatterns.append('([A-Za-z.]+) at ([A-Za-z.\s]+) dot edu') #hager,serafim,pal

# phone patterns
# each regular expression pattern should have exactly three sets of parentheses.
#   the first parenthesis should be around the area code part XXX
#   the second parenthesis should be around the exchange part YYY
#   the third parenthesis should be around the number part ZZZZ
#   in a phone number whose standard form is XXX-YYY-ZZZZ
ppatterns = []
ppatterns.append('(\d{3})-(\d{3})-(\d{4})')
ppatterns.append('(?:[(])([0-9]{3})(?:[)])([0-9]{3})-([0-9]{4})')  #tim
ppatterns.append('(?:[(])([0-9]{3})(?:[)])[ ]*([0-9]{3})-([0-9]{4})')   #bgirod
ppatterns.append('(?:[[])([0-9]{3})(?:[]])\s([0-9]{3})-([0-9]{4})')    #nass
ppatterns.append('(\d{3}) (\d{3}) (\d{4})')    #pal
ppatterns.append('(\d{3}) ([0-9]{3})-([0-9]{4})')    #shoham

""" 
This function takes in a filename along with the file object and
scans its contents against regex patterns. It returns a list of
(filename, type, value) tuples where type is either an 'e' or a 'p'
for e-mail or phone, and value is the formatted phone number or e-mail.
The canonical formats are:
     (name, 'p', '###-###-#####')
     (name, 'e', 'someone@something')
If the numbers you submit are formatted differently they will not
match the gold answers

TODO
For Part 3, if you have added other lists, you may should add
additional for loops that match the patterns in those lists
and produce correctly formatted results to append to the res list.
"""
def process_file(name, f):
    # note that debug info should be printed to stderr
    # sys.stderr.write('[process_file]\tprocessing file: %s\n' % (path))
    res = []
    for line in f:
        for epat in epatterns:
            # each epat has 2 sets of parentheses so each match will have 2 items in a list
            matches = re.findall(epat,line)
            for m in matches:
                # string formatting operator % takes elements of list m
                #   and inserts them in place of each %s in the result string
                email = '%s@%s.edu' % m
                res.append((name,'e',email))

        for ppat in ppatterns:
            # each ppat has 3 sets of parentheses so each match will have 3 items in a list
            matches = re.findall(ppat,line)
            for m in matches:
                phone = '%s-%s-%s' % m
                res.append((name,'p',phone))
    return res

"""
You should not edit this function.
"""
def process_dir(data_path):
    # get candidates
    guess_list = []
    for fname in os.listdir(data_path):
        if fname[0] == '.':
            continue
        path = os.path.join(data_path,fname)
        f = open(path,'r', encoding='latin-1')
        f_guesses = process_file(fname, f)
        guess_list.extend(f_guesses)
    return guess_list

"""
You should not edit this function.
Given a path to a tsv file of gold e-mails and phone numbers
this function returns a list of tuples of the canonical form:
(filename, type, value)
"""
def get_gold(gold_path):
    # get gold answers
    gold_list = []
    f_gold = open(gold_path,'r')
    for line in f_gold:
        gold_list.append(tuple(line.strip().split('\t')))
    return gold_list

"""
You should not edit this function.
Given a list of guessed contacts and gold contacts, this function
computes the intersection and set differences, to compute the true
positives, false positives and false negatives.  Importantly, it
converts all of the values to lower case before comparing
"""
def score(guess_list, gold_list):
    guess_list = [(fname, _type, value.lower()) for (fname, _type, value) in guess_list]
    gold_list = [(fname, _type, value.lower()) for (fname, _type, value) in gold_list]
    guess_set = set(guess_list)
    gold_set = set(gold_list)

    tp = guess_set.intersection(gold_set)
    fp = guess_set - gold_set
    fn = gold_set - guess_set

    pp = pprint.PrettyPrinter()
    #print 'Guesses (%d): ' % len(guess_set)
    #pp.pprint(guess_set)
    #print 'Gold (%d): ' % len(gold_set)
    #pp.pprint(gold_set)
    print ('True Positives (%d): ' % len(tp))
    pp.pprint(tp)
    print ('False Positives (%d): ' % len(fp))
    pp.pprint(fp)
    print ('False Negatives (%d): ' % len(fn))
    pp.pprint(fn)
    print ('Summary: tp=%d, fp=%d, fn=%d' % (len(tp),len(fp),len(fn)))

"""
You should not edit this function.
It takes in the string path to the data directory and the gold file
"""
def main(data_path, gold_path):
    guess_list = process_dir(data_path)
    gold_list =  get_gold(gold_path)
    score(guess_list, gold_list)

"""
commandline interface takes a directory name and gold file.
It then processes each file within that directory and extracts any
matching e-mails or phone numbers and compares them to the gold file
"""
if __name__ == '__main__':
    if (len(sys.argv) != 3):
        print ('usage:\tSpamLord.py <data_dir> <gold_file>')
        sys.exit(0)
    main(sys.argv[1],sys.argv[2])
