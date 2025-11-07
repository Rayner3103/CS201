from collections import defaultdict
from utils import default_edit_distance

class Array_BKTree:
    class Node:
        def __init__(self, max_dist=20, x=None):
            self.word = x
            self.MAX_DIST = max_dist
            self.next = [-1] * self.MAX_DIST
            self.entity_counts = defaultdict(int)

        def increment_entity(self, entity):
            if self.entity_counts.get(entity):
                self.entity_counts[entity] += 1
            else:
                self.entity_counts[entity] = 1

    def __init__(self, maxn=1, tol=2, max_dist=20, edit_distance=default_edit_distance):
        self.MAXN = maxn
        self.TOL = tol
        self.max_dist = max_dist
        self.root = self.Node(self.max_dist)
        self.tree = [self.Node(self.max_dist) for _ in range(self.MAXN)]
        self.ptr = 0
        self.edit_distance = edit_distance

    def add(self, word, entity=""):
        toAdd = self.Node(self.max_dist, word)
        if not self.root.word:
            self.root.word = toAdd.word
            self.root.next = toAdd.next
            self.root.increment_entity(entity)
            return
        self.add_helper(self.root, toAdd, entity)

    def add_helper(self, node: Node, toAdd: Node, entity: str):
        # ensure node.next is large enough for the distance index
        dist = self.edit_distance(toAdd.word, node.word)
        if dist == 0:
            node.increment_entity(entity)
            return

        if dist >= len(node.next):
            node.next.extend([-1] * (dist - len(node.next) + 1))

        idx = node.next[dist]
        if idx == -1 or not self.tree[idx] or not self.tree[idx].word:
            if self.ptr >= self.MAXN:
                self.tree.extend([self.Node(self.max_dist) for _ in range(self.MAXN)])
                self.MAXN *= 2
            toAdd.increment_entity(entity)
            self.tree[self.ptr] = toAdd
            node.next[dist] = self.ptr
            self.ptr += 1
        else:
            self.add_helper(self.tree[idx], toAdd, entity)

    def get_similar_words(self, s:str)->list[str]:
        return list(map(lambda node: node.word, self.get_similar_words_helper(self.root, s)))
    
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

    def get_similar_words_helper(self, curr, s):
        ret = []
        if not curr or not curr.word:
            return ret

        dist = self.edit_distance(curr.word, s)

        if dist <= self.TOL:
            ret.append(curr)
        start = dist - self.TOL if dist - self.TOL > 0 else 1
        while start <= dist + self.TOL and start < self.max_dist:
            idx = curr.next[start]
            if idx == -1:
                start += 1
                continue
            tmp = self.get_similar_words_helper(self.tree[idx], s)
            ret += tmp
            start += 1
        return ret


