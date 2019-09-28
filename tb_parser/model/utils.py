import torch as T
import torch.nn as NN
import torch.nn.functional as F
from torch.autograd import Variable

import re

# Helper functions

def variable(*args_, **kwargs):
    v = Variable(*args_, **kwargs)
    return v.cuda() if T.cuda.is_available() else v

def var_to_numpy(v):
    return (v.cpu() if T.cuda.is_available() else v).data.numpy()

def zerovar(*size):
    return variable(T.zeros(*size))

# Same thing as original implementation
# represents a bidirectional mapping from strings to ints
class Vocab(object):
    def __init__(self, w2i):
        self.w2i = dict(w2i)
        self.i2w = {i:w for w, i in w2i.items()}

    @classmethod
    def from_list(cls, words):
        return Vocab({w: i for i, w in enumerate(words)})

    @classmethod
    def from_file(cls, filename):
        words = []
        f = open(filename)
        for l in f:
            l = l.strip()
            w, c = l.split()
            words.append(w)
        f.close()
        return Vocab.from_list(words)

    def size(self):
        return len(self.w2i.keys())

# format:
# John left . ||| SHIFT SHIFT REDUCE_L SHIFT REDUCE_R
def read_oracle(fname, vw, va):
    with open(fname) as f:
        for line in f:
            line = line.strip()
            ssent, sacts = re.split(r' \|\|\| ', line)
            sent = [vw.w2i[x] for x in ssent.split()]
            acts = [va.w2i[x] for x in sacts.split()]
            sent.reverse()
            acts.reverse()
            yield sent, acts


