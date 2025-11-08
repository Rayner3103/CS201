from collections import defaultdict
from Levenshtein import distance as levenshtein_distance

class Linked_BKTree:
    class Node:
        def __init__(self, x=None):
            self.word = x
            self.children = {}  # distance -> Node
            self.entity_counts = defaultdict(int)

        def increment_entity(self, entity):
            self.entity_counts[entity] += 1

    def __init__(self, edit_distance=levenshtein_distance):
        self.root = self.Node()
        self.edit_distance = edit_distance

    def add(self, word: str, entity: str=""):
        if not self.root.word:
            self.root.word = word
            self.root.increment_entity(entity)
            return

        curr = self.root
        while True:
            d = self.edit_distance(word, curr.word)
            
            if d == 0:
                curr.increment_entity(entity)
                return
            
            if d not in curr.children:
                curr.children[d] = self.Node(word)
                curr.children[d].increment_entity(entity)
                return
            
            curr = curr.children[d]

    def get_similar_words_helper(self, curr: Node, s: str, tol)->list[Node]:
        results = []
        if not curr or not curr.word:
            return results
        
        d = self.edit_distance(curr.word, s)
        if d <= tol:
            results.append(curr)

        low = max(0, d - tol)
        high = d + tol
        for i in range(low, high + 1):
            if i in curr.children:
                results += self.get_similar_words_helper(curr.children[i], s, tol)
        return results

    def get_similar_words(self, s, tol):
        similar_word_nodes = self.get_similar_words_helper(self.root, s, tol)
        return list(map(lambda node: node.word, similar_word_nodes))

    def get_entity_rank_by_similar_words(self, s:str, tol)->dict[str: int]:
        result = dict()
        similar_nodes = self.get_similar_words_helper(self.root, s, tol)
        for node in similar_nodes:
            for entity, count in node.entity_counts.items():
                result[entity] = result.get(entity, 0) + count
        return sorted(result.items(), key=lambda x: x[1], reverse=True)