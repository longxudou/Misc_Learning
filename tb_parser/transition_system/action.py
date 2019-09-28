# actions the parser can take
acts = ['SHIFT', 'REDUCE_L', 'REDUCE_R']
vocab_acts = Vocab.from_list(acts)
SHIFT = vocab_acts.w2i['SHIFT']
REDUCE_L = vocab_acts.w2i['REDUCE_L']
REDUCE_R = vocab_acts.w2i['REDUCE_R']
NUM_ACTIONS = vocab_acts.size()