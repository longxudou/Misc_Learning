import torch as T
import torch.nn as NN
import torch.nn.functional as F
from torch.autograd import Variable


class StackRNN(object):
    def __init__(self,
                 cell,
                 initial_state,
                 get_output,
                 p_empty_embedding=None):
        self.cell = cell
        self.s = [(initial_state, None)]
        self.empty = None
        self.get_output = get_output
        if p_empty_embedding is not None:
            self.empty = p_empty_embedding

    #stack.push(comp_rep, (comp_rep, head_tok))
    #buffer_.push(tok_embedding, (tok_embedding, self.vocab.i2w[tok]))
    #cell input: Inputs: input, (h_0, c_0)
    #cell output: Outputs: h_1, c_1
    def push(self, expr, extra=None):
        self.s.append((self.cell(expr, self.s[-1][0]), extra))


    def pop(self):
        return self.s.pop()[1] # return "extra" (i.e., whatever the caller wants or None)

    def embedding(self):
        # work around since inital_state.output() is None
        return self.get_output(self.s[-1][0]) if len(self.s) > 1 else self.empty

    def __len__(self):
        return len(self.s) - 1


