'''
Original implementation (dynet)
https://github.com/clab/dynet_tutorial_examples/blob/master/tutorial_parser.ipynb

Reference implementation (pytorch)
https://gist.github.com/BarclayII/380c24afec20963617c82c43590b78f2

The code structure and variable names are similar for better reference.
'''
import torch as T
import torch.nn as NN
import torch.nn.functional as F
from torch.autograd import Variable
from torch.utils.data import DataLoader
import torch.optim as optim


import argparse
import numpy as np
import numpy.random as RNG
import re
from model.transition_parser import TransitionParser
from model.utils import Vocab, read_oracle

# def eprint(*args, **kwargs):
#     print(*args, file=sys.stderr, **kwargs)
# Argument parsing

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Transition-based Dependency Parser (chris dyer 2015 version)')
    parser.add_argument("--word_dim",help="dimension of word embedding",type=int,default=64)
    parser.add_argument("--lstm_dim",help="dimension of LSTM hidden state",type=int,default=64)
    parser.add_argument("--action_dim",help="dimension of action layer",type=int,default=32)
    parser.add_argument("--cuda",help="use cuda",action="store_true")
    parser.add_argument("--vocab_file_path",help="",type=str)
    parser.add_argument("--train_file_path",help="",type=str)
    parser.add_argument("--dev_file_path",help="",type=str)
    parser.add_argument('--epoch', type=int, default=50, help='maximum epoch number')
    parser.add_argument('--drop_out', type=float, default=0.55, help='dropout ratio')
    parser.add_argument('--char_dim', type=int, default=30, help='dimension of char embedding')
    parser.add_argument('--char_layers', type=int, default=1, help='number of char level layers')
    parser.add_argument('--word_layers', type=int, default=1, help='number of word level layers')
    parser.add_argument('--lr', type=float, default=1e-5, help='initial learning rate')
    parser.add_argument('--lr_decay', type=float, default=0.05, help='decay ratio of learning rate')
    parser.add_argument('--fine_tune', action='store_false', help='fine tune the diction of word embedding or not')
    parser.add_argument('--load_check_point', default='', help='path previous checkpoint that want to be loaded')
    parser.add_argument('--load_opt', action='store_true', help='also load optimizer from the checkpoint')
    parser.add_argument('--update', choices=['sgd', 'adam'], default='sgd', help='optimizer choice')
    parser.add_argument('--momentum', type=float, default=0.9, help='momentum for sgd')
    parser.add_argument('--clip_grad', type=float, default=5.0, help='clip grad at')
    parser.add_argument('--lambda0', type=float, default=1, help='lambda0')
    parser.add_argument('--patience', type=int, default=15, help='patience for early stop')
    args = parser.parse_args()

    # actions the parser can take
    acts = ['SHIFT', 'REDUCE_L', 'REDUCE_R']
    vocab_acts = Vocab.from_list(acts)
    SHIFT = vocab_acts.w2i['SHIFT']
    REDUCE_L = vocab_acts.w2i['REDUCE_L']
    REDUCE_R = vocab_acts.w2i['REDUCE_R']
    NUM_ACTIONS = vocab_acts.size()

    vocab_words = Vocab.from_file(args.vocab_file_path)
    training_set = list(read_oracle(args.train_file_path, vocab_words, vocab_acts))
    validation_set = list(read_oracle(args.dev_file_path, vocab_words, vocab_acts))

    # # CUDA for PyTorch
    # use_cuda = T.cuda.is_available()
    # device = T.device("cuda:0" if use_cuda else "cpu")

    #generators
    training_generator = DataLoader(training_set, batch_size=4,shuffle=True, num_workers=4)
    validation_generator = DataLoader(validation_set, batch_size=4,shuffle=True, num_workers=4)

    model = TransitionParser(vocab_words, args.lstm_dim, args.word_dim, args.cuda, vocab_acts)
    #self, vocab, lstm_dim, word_dim, is_cuda, num_actions
    if args.cuda:
        model.cuda()

    if args.update == 'sgd':
        optimizer = optim.SGD(model.parameters(), lr=args.lr, momentum=args.momentum)
    elif args.update == 'adam':
        optimizer = optim.Adam(model.parameters(), lr=args.lr)

    train=training_set
    dev=validation_set

    instances_processed = 0
    validation_losses = []

    min_loss=100
    for epoch in range(args.epoch):
        if epoch % 5 == 0:
            print(min_loss)

        RNG.shuffle(train)
        words = 0
        total_loss = 0.
        for (s, a) in train:
            e = instances_processed // len(train)
            # if instances_processed % 1000 == 0:
            #     model.eval()
            #     dev_words = 0
            #     dev_loss = 0.
            #     for (ds, da) in dev:
            #         loss = model.forward(ds, da)
            #         dev_words += len(ds)
            #         if loss is not None:
            #             if args.cuda:
            #                 dev_loss += loss.cpu().data.numpy()
            #             else:
            #                 dev_loss += loss.data.numpy()
            #     print ('[valid] epoch %d: per-word loss: %.6f' %
            #            (e, dev_loss / dev_words))
            #     validation_losses.append(dev_loss)

            # if instances_processed % 100 == 0 and words > 0:
            if words>0:
                min_loss=min(min_loss, total_loss / words)
                # print ('epoch %d: per-word loss: %.6f' % (e, total_loss / words))
                words = 0
                total_loss = 0.

            model.train()
            loss = model.forward(s, a)
            words += len(s)
            instances_processed += 1

            if loss is not None:
                if args.cuda:
                    total_loss += loss.cpu().data.numpy()
                else:
                    total_loss += loss.data.numpy()
                loss.backward()
                NN.utils.clip_grad_norm_(model.parameters(), args.clip_grad)
                optimizer.step()

    # s = 'Parsing in Austin is fun .'
    # UNK = vocab_words.w2i['<unk>']
    # toks = [vocab_words.w2i[x] if x in vocab_words.w2i else UNK for x in s.split()]
    # toks.reverse()
    # model.forward(toks, None)