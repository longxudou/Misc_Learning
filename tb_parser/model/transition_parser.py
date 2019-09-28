import torch as T
import torch.nn as NN
import torch.nn.functional as F
from torch.autograd import Variable
from .stack_rnn import StackRNN
from .utils import variable, Vocab, zerovar, var_to_numpy


class TransitionParser(NN.Module):
    def __init__(self, vocab, lstm_dim, word_dim, is_cuda, vocab_acts):
        super(TransitionParser, self).__init__()

        self.vocab = vocab
        self.lstm_dim = lstm_dim
        self.word_dim = word_dim
        self.is_cuda = is_cuda

        self.vocab_acts = vocab_acts
        self.num_actions = vocab_acts.size()

        # syntactic composition
        self.p_comp = NN.Linear(lstm_dim * 2, lstm_dim)
        # parser state to hidden
        self.p_s2h = NN.Linear(lstm_dim * 2, lstm_dim)
        # hidden to action
        self.p_act = NN.Linear(lstm_dim, self.num_actions)

        # layers, in-dim, out-dim, model
        self.buff_rnn_cell = NN.LSTMCell(word_dim, lstm_dim)
        self.stack_rnn_cell = NN.LSTMCell(word_dim, lstm_dim)
        self.pempty_buffer_emb = NN.Parameter(T.randn(1, lstm_dim))
        self.WORDS_LOOKUP = NN.Embedding(vocab.size(), word_dim)

    def _rnn_get_output(self, state):
        return state[0]

    # Returns an expression of the loss for the sequence of actions.
    # (that is, the oracle_actions if present or the predicted sequence otherwise)
    def forward(self, tokens, oracle_actions=None):
        tokens = variable(T.LongTensor(tokens))
        # I think DyNet implementation is doing single-sample SGD.
        def _valid_actions(stack, buffer_):
            valid_actions= []
            if len(buffer_) > 0:
                valid_actions += [self.vocab_acts.w2i['SHIFT']]
            if len(stack) >= 2:
                valid_actions += [self.vocab_acts.w2i['REDUCE_L'], self.vocab_acts.w2i['REDUCE_R']]
            return valid_actions

        if oracle_actions:
            oracle_actions = list(oracle_actions)

        # Since we are using LSTMCell here we should specify initial state
        # manually.
        buffer_initial = (zerovar(1, self.lstm_dim), zerovar(1, self.lstm_dim))
        stack_initial = (zerovar(1, self.lstm_dim), zerovar(1, self.lstm_dim))
        buffer_ = StackRNN(self.buff_rnn_cell, buffer_initial,
                           self._rnn_get_output, self.pempty_buffer_emb)
        stack = StackRNN(self.stack_rnn_cell, stack_initial,
                         self._rnn_get_output)

        # We will keep track of all the losses we accumulate during parsing.
        # If some decision is unambiguous because it's the only thing valid given
        # the parser state, we will not model it. We only model what is ambiguous.
        losses = []

        # push the tokens onto the buffer (tokens is in reverse order)
        tok_embeddings = self.WORDS_LOOKUP(tokens.unsqueeze(0))[0] # batch dim
        for i in range(tok_embeddings.size()[0]):
            tok_embedding = tok_embeddings[i].unsqueeze(0)
            if self.is_cuda:
                tok = tokens.cpu().data.numpy()[i]
            else:
                tok = tokens.data.numpy()[i]
            buffer_.push(tok_embedding, (tok_embedding, self.vocab.i2w[tok]))

        # compute probability of each of the actions and choose an action
        # either from the oracle or if there is no oracle, based on the model
        while not (len(stack) == 1 and len(buffer_) == 0):
            valid_actions = _valid_actions(stack, buffer_)
            log_probs = None
            action = valid_actions[0]
            if len(valid_actions) > 1:
                p_t = T.cat([buffer_.embedding(), stack.embedding()], 1)
                h = T.tanh(self.p_s2h(p_t))
                logits = self.p_act(h)[0][T.LongTensor(valid_actions)]
                valid_action_tbl = {a: i for i, a in enumerate(valid_actions)}
                log_probs = F.log_softmax(logits, dim=0)

                if oracle_actions is None:
                    action_idx = T.max(log_probs, 0)[1].item()
                    action = valid_actions[action_idx]

            if oracle_actions is not None:
                action = oracle_actions.pop()

            if log_probs is not None:
                # append the action-specific loss
                losses.append(log_probs[valid_action_tbl[action]].unsqueeze(0))

            # execute the action to update the parser state
            if action == self.vocab_acts.w2i['SHIFT']:
                tok_embedding, token = buffer_.pop()
                stack.push(tok_embedding, (tok_embedding, token))

            # one of the REDUCE actions
            else:
                right = stack.pop() # pop a stack state
                left = stack.pop() # pop another stack state

                # figure out which is the head and which is the modifier
                head, modifier = ((left, right) if action == self.vocab_acts.w2i['REDUCE_R']
                                  else (right, left))

                # compute composed representation
                head_rep, head_tok = head
                mod_rep, mod_tok = modifier
                comp_rep = T.cat([head_rep, mod_rep], 1)
                comp_rep = T.tanh(self.p_comp(comp_rep))

                stack.push(comp_rep, (comp_rep, head_tok))
                if oracle_actions is None:
                    print ('%s --> %s' % (head_tok, mod_tok))

        # the head of the tree that remains at the top of the stack is the root
        if oracle_actions is None:
            head = stack.pop()[1]
            print ('ROOT --> %s' % head)
        _loss = -T.sum(T.cat(losses)) if len(losses) > 0 else None
        return _loss