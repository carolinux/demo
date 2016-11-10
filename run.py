import os
import sys

from graph.users import Users


def main(input_batch, input_stream, outfiles):
    users = Users()
    i = 0
    with open(input_batch, 'r') as f:
        f.readline() # to skip header
        for line in f:
            vals = line.strip().split(",")
            date_str = vals[0] # TODO: Is the input sorted?
            id1 = int(vals[1])
            id2 = int(vals[2])
            users.add_transaction(id1, id2)
            i += 1
            if i%100000 ==0:
                print "Now at {}th transaction".format(i)

    with open(input_stream, 'r') as f, open(outfiles[0], 'w') as of1, open(outfiles[1],'w') as of2, open(outfiles[2], 'w') as of3:
        f.readline() # to skip header
        for line in f:
            vals = line.strip().split(",")
            id1 = int(vals[1])
            id2 = int(vals[2])
            trust_msg1 = users.get_trust_level_of_transaction(id1, id2, degree_of_trust=1)
            trust_msg2 = users.get_trust_level_of_transaction(id1, id2, degree_of_trust=2)
            trust_msg3 = users.get_trust_level_of_transaction(id1, id2, degree_of_trust=4)
            of1.write(trust_msg1+"\n")
            of2.write(trust_msg2+"\n")
            of3.write(trust_msg3+"\n")
            #print trust_msg1, trust_msg2, trust_msg3
            users.add_transaction(id1, id2)
    

if __name__ == '__main__':
    input_batch = sys.argv[1]
    input_stream = sys.argv[2]
    out1 = sys.argv[3]
    out2 = sys.argv[4]
    out3 = sys.argv[5]
    main(input_batch, input_stream, outfiles=[out1, out2, out3])
