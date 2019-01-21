file_new = "G:/URECA/new_vocab"
file_old = "G:/URECA/textsum/CWD/data/corpus_vocab"


file1 = open(file_new, "r")
file2 = open(file_old, "r")

Dict1 = file1.readlines()
Dict2 = file2.readlines()

DF = [ x for x in Dict1 if x not in Dict2 ]
print(DF)