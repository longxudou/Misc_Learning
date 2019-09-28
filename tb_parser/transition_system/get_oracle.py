from typing import Dict, List, Tuple
import logging
from overrides import overrides

from allennlp.common.file_utils import cached_path
from allennlp.data.dataset_readers.dataset_reader import DatasetReader
from allennlp.data.fields import AdjacencyField, MetadataField, SequenceLabelField
from allennlp.data.fields import Field, TextField
from allennlp.data.token_indexers import SingleIdTokenIndexer, TokenIndexer
from allennlp.data.tokenizers import Token
from allennlp.data.instance import Instance

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name

# FIELDS = ["id", "form", "lemma", "pos", "head", "deprel", "top", "pred", "frame"]
FIELDS = ["id", "form", "lemma", "pos", "top", "pred", "frame"]


def parse_sentence(sentence_blob: str) -> Tuple[List[Dict[str, str]], List[Tuple[int, int]], List[str]]:
    """
    Parses a chunk of text in the SemEval SDP format.

    Each word in the sentence is returned as a dictionary with the following
    format:
    'id': '1',
    'form': 'Pierre',
    'lemma': 'Pierre',
    'pos': 'NNP',
    'head': '2',   # Note that this is the `syntactic` head.
    'deprel': 'nn',
    'top': '-',
    'pred': '+',
    'frame': 'named:x-c'

    'pred':the pred column is a simplification of the corresponding field in earlier CoNLL tasks,
     indicating whether or not this token represents a predicate, i.e. a node with outgoing dependency edges.

    Along with a list of arcs and their corresponding tags. Note that
    in semantic dependency parsing words can have more than one head
    (it is not a tree), meaning that the list of arcs and tags are
    not tied to the length of the sentence.
    """
    annotated_sentence = []
    arc_indices = []
    arc_tags = []
    predicates = []

    lines = [line.split("\t") for line in sentence_blob.split("\n")
             if line and not line.strip().startswith("#")]
    for line_idx, line in enumerate(lines):
        annotated_token = {k: v for k, v in zip(FIELDS, line)}
        if annotated_token['pred'] == "+":
            predicates.append(line_idx)
        annotated_sentence.append(annotated_token)

    for line_idx, line in enumerate(lines):
        for predicate_idx, arg in enumerate(line[len(FIELDS):]):
            if arg != "_":
                arc_indices.append((line_idx, predicates[predicate_idx]))
                arc_tags.append(arg)
    return annotated_sentence, arc_indices, arc_tags


def lazy_parse(text: str):
    for sentence in text.split("\n\n"):
        if sentence:
            yield parse_sentence(sentence)


@DatasetReader.register("sdp_2015_tb")
class SemanticDependenciesDatasetReader(DatasetReader):
    """
    Reads a file in the SemEval 2015 Task 18 (Broad-coverage Semantic Dependency Parsing)
    format.

    Parameters
    ----------
    token_indexers : ``Dict[str, TokenIndexer]``, optional (default=``{"tokens": SingleIdTokenIndexer()}``)
        The token indexers to be applied to the words TextField.
    """

    def __init__(self,
                 token_indexers: Dict[str, TokenIndexer] = None,
                 lemma_indexers: Dict[str, TokenIndexer] = None,
                 lazy: bool = False) -> None:
        super().__init__(lazy)
        self._token_indexers = token_indexers or {'tokens': SingleIdTokenIndexer()}
        self._lemma_indexers = None
        if lemma_indexers is not None and len(lemma_indexers) > 0:
            self._lemma_indexers = lemma_indexers

    @overrides
    def _read(self, file_path: str):
        # if `file_path` is a URL, redirect to the cache
        file_path = cached_path(file_path)

        logger.info("Reading semantic dependency parsing data from: %s", file_path)

        with open(file_path, encoding='utf8') as sdp_file:
            for annotated_sentence, directed_arc_indices, arc_tags in lazy_parse(sdp_file.read()):
                # If there are no arc indices, skip this instance.
                if not directed_arc_indices:
                    continue

                gold_actions = get_oracle_actions(annotated_sentence, directed_arc_indices, arc_tags)

                tokens = [word["form"] for word in annotated_sentence]
                lemmas = None
                if self._lemma_indexers is not None:
                    lemmas = [word["lemma"] for word in annotated_sentence]
                pos_tags = [word["pos"] for word in annotated_sentence]
                yield self.text_to_instance(tokens, lemmas, pos_tags, directed_arc_indices, arc_tags, gold_actions)

    @overrides
    def text_to_instance(self,  # type: ignore
                         tokens: List[str],
                         lemmas: List[str] = None,
                         pos_tags: List[str] = None,
                         arc_indices: List[Tuple[int, int]] = None,
                         arc_tags: List[str] = None,
                         gold_actions: List[str] = None) -> Instance:
        # pylint: disable=arguments-differ
        fields: Dict[str, Field] = {}
        token_field = TextField([Token(t) for t in tokens], self._token_indexers)
        fields["tokens"] = token_field
        fields["metadata"] = MetadataField({"tokens": tokens})
        if lemmas is not None and self._lemma_indexers is not None:
            fields["lemmas"] = TextField([Token(l) for l in lemmas], self._lemma_indexers)
        if pos_tags is not None:
            fields["pos_tags"] = SequenceLabelField(pos_tags, token_field, label_namespace="pos")
        if arc_indices is not None and arc_tags is not None:
            fields["arc_tags"] = AdjacencyField(arc_indices, token_field, arc_tags)
        if gold_actions is not None:
            fields["gold_actions"]=MetadataField({"gold_actions":gold_actions})

        return Instance(fields)


def get_oracle_actions(annotated_sentence, directed_arc_indices, arc_tags):
    """

    :param graph: dict of list,
        key: id_of_point
        value: list, [(id_of_head1, label),(id_of_head2, label)]
    :return:
    """
    graph = {}
    for token_idx in range(len(annotated_sentence)):
        graph[token_idx] = []

    for arc, arc_tag in zip(directed_arc_indices, arc_tags):
        graph[arc[0]].append((arc[1], arc_tag))

    N = len(graph)

    # i:head_point j:child_point
    top_down_graph = [[] for i in range(N + 1)]  # N point, 1 root point

    # i:child_point j:head_point ->Bool
    # partical graph during constrution
    sub_graph = [[False for i in range(N + 1)] for j in range(N + 1)]

    root = -1
    # each id is +1 from graph, so when used in graph should -1
    for i in range(N):
        for point_i_child_list in graph[i]:
            head = point_i_child_list[0]
            if head == -1:
                if root != -1:
                    print("error: there should be only one root.")
                root = i + 1
            else:
                top_down_graph[head].append(i + 1)

    actions = []
    stack = []
    buffer = [0]
    deque = []

    for i in range(N, 0, -1):
        buffer.append(i)

    # return if w1 is one head of w0
    def has_head(w0, w1):
        if w0 <= 0:
            return False
        for w in graph[w0 - 1]:
            if w[0] == w1 - 1:
                return True
        return False

    def has_unfound_child(w):
        for child in top_down_graph[w]:
            if not sub_graph[child][w]:
                return True
        return False

    # return if w has other head except the present one
    def has_other_head(w):
        head_num = 0
        for h in sub_graph[w]:
            if h:
                head_num += 1
        if head_num + 1 < len(graph[w - 1]):
            return True
        return False

    # return if w has any unfound head
    def lack_head(w):
        if w < 0:
            return False
        head_num = 0
        for h in sub_graph[w]:
            if h:
                head_num += 1
        if head_num < len(graph[w - 1]):
            return True

    # return if w has any unfound child in stack sigma
    # !!! except the top in stack
    def has_other_child_in_stack(stack, w):
        if w <= 0:
            return False
        for c in top_down_graph[w]:
            if c in stack \
                    and c != stack[-1] \
                    and not sub_graph[c][w]:
                return True
        return False

    # return if w has any unfound head in stack sigma
    # !!! except the top in stack
    def has_other_head_in_stack(stack, w):
        if w <= 0:
            return False
        for h in graph[w - 1]:
            if h[0] + 1 in stack \
                    and h[0] + 1 != stack[-1] \
                    and not sub_graph[w][h[0] + 1]:
                return True
        return False

    # return the relation between child: w0, head: w1
    def get_arc_label(w0, w1):
        for h in graph[w0 - 1]:
            if h[0] == w1 - 1:
                return h[1]

    def get_oracle_actions_onestep(sub_graph, stack, buffer, deque, actions):
        b0 = buffer[-1] if len(buffer) > 0 else -1
        s0 = stack[-1] if len(stack) > 0 else -1

        if s0 > 0 and has_head(s0, b0):
            if not has_unfound_child(s0) and not has_other_head(s0):
                # actions.append("LR")
                actions.append("LR(" + get_arc_label(s0, b0) + ")")
                stack.pop()
                sub_graph[s0][b0] = True
                return
            else:
                actions.append("LP(" + get_arc_label(s0, b0) + ")")
                deque.append(stack.pop())
                sub_graph[s0][b0] = True
                return

        elif s0 > 0 and has_head(b0, s0):
            if not has_other_child_in_stack(stack, b0) and not has_other_head_in_stack(stack, b0):
                actions.append("RS(" + get_arc_label(b0, s0) + ")")
                while len(deque) != 0:
                    stack.append(deque.pop())
                stack.append(buffer.pop())
                sub_graph[b0][s0] = True
                return

            elif s0 > 0:
                actions.append("RP(" + get_arc_label(b0, s0) + ")")
                deque.append(stack.pop())
                sub_graph[b0][s0] = True
                return

        elif len(buffer) != 0 and not has_other_head_in_stack(stack, b0) \
                and not has_other_child_in_stack(stack, b0):
            actions.append("NS")
            while len(deque) != 0:
                stack.append(deque.pop())
            stack.append(buffer.pop())
            return

        elif s0 > 0 and not has_unfound_child(s0) and not lack_head(s0):
            actions.append("NR")
            stack.pop()
            return

        elif s0 > 0:
            actions.append("NP")
            deque.append(stack.pop())
            return

        else:
            actions.append('-E-')
            print('"error in oracle!"')
            return

    while (len(buffer) != 0):
        get_oracle_actions_onestep(sub_graph, stack, buffer, deque, actions)

    return actions


if __name__ == "__main__":
    reader = SemanticDependenciesDatasetReader()
    dataset = reader.read('/Users/longxud/Documents/Code/data/semeval2015-task18/english/dm/en.dm.train.sdp')
    for instance in dataset:
        print(instance)

    # graph={1:[(2,'A')]}
    # get_oracle_actions(graph)
