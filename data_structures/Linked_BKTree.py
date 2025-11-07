from collections import defaultdict
from utils import default_edit_distance

class Linked_BKTree:
    class Node:
        def __init__(self, x=None):
            self.word = x
            self.children = {}  # distance -> Node
            self.entity_counts = defaultdict(int)

        def increment_entity(self, entity):
            if self.entity_counts.get(entity):
                self.entity_counts[entity] += 1
            else:
                self.entity_counts[entity] = 1

    def __init__(self, tol=2, edit_distance=default_edit_distance):
        self.root = self.Node()
        self.tol = tol
        self.edit_distance = edit_distance

    def add_helper(self, curr: Node, toAdd: Node, entity: str):
        if not curr.word:
            curr.word = toAdd.word
            curr.children = toAdd.children
            curr.increment_entity(entity)
            return

        d = self.edit_distance(toAdd.word, curr.word)
        if d == 0:
            curr.increment_entity(entity)
            return

        child = curr.children.get(d)
        if not child or not child.word:
            toAdd.increment_entity(entity)
            curr.children[d] = toAdd
        else:
            self.add_helper(child, toAdd, entity)

    def add(self, word: str, entity: str=""):
        self.add_helper(self.root, self.Node(word), entity)

    def get_similar_words_helper(self, curr: Node, s: str)->list[Node]:
        results = []
        if not curr or not curr.word:
            return results
        
        d = self.edit_distance(curr.word, s)
        if d <= self.tol:
            results.append(curr)

        low = max(0, d - self.tol)
        high = d + self.tol
        for i in range(low, high + 1):
            results += self.get_similar_words_helper(curr.children.get(i, None), s)
        return results

    def get_similar_words(self, s):
        similar_word_nodes = self.get_similar_words_helper(self.root, s)
        return list(map(lambda node: node.word, similar_word_nodes))

    def get_entity_rank_by_similar_words(self, s:str)->dict[str: int]:
        result = dict()
        similar_nodes = self.get_similar_words_helper(self.root, s)
        for node in similar_nodes:
            for entity, count in node.entity_counts.items():
                if result.get(entity):
                    result[entity] += count
                else:
                    result[entity] = count
        return sorted(result.items(), key=lambda x: x[1], reverse=True)