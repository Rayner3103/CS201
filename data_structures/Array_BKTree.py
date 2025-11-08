from collections import defaultdict
from Levenshtein import distance as levenshtein_distance

class Array_BKTree:
    class Node:
        __slots__ = ('word', 'next', 'entity_counts')  # Memory optimization
        
        def __init__(self, max_dist=20, x=None):
            self.word = x
            self.next = [-1] * max_dist
            self.entity_counts = defaultdict(int)

        def increment_entity(self, entity):
            self.entity_counts[entity] += 1  # Simplified

    def __init__(self, maxn=1000, max_dist=20, edit_distance=levenshtein_distance):
        self.MAXN = maxn
        self.max_dist = max_dist
        self.tree = [None] * maxn  # Pre-allocate, use None instead of empty nodes
        self.ptr = 0
        self.edit_distance = edit_distance

    def add(self, word, entity=""):
        # Handle root case inline
        if self.ptr == 0:
            self.tree[0] = self.Node(self.max_dist, word)
            self.tree[0].increment_entity(entity)
            self.ptr = 1
            return
        
        # Iterative instead of recursive
        node_idx = 0
        while True:
            node = self.tree[node_idx]
            dist = self.edit_distance(word, node.word)
            
            if dist == 0:
                node.increment_entity(entity)
                return
            
            # Bounds check
            if dist >= self.max_dist:
                node.next.extend([-1] * (dist - len(node.next) + 1))
            
            next_idx = node.next[dist]
            
            if next_idx == -1:
                # Need to expand tree?
                if self.ptr >= self.MAXN:
                    self._expand_tree()
                
                # Create new node
                new_node = self.Node(self.max_dist, word)
                new_node.increment_entity(entity)
                self.tree[self.ptr] = new_node
                node.next[dist] = self.ptr
                self.ptr += 1
                return
            
            node_idx = next_idx

    def _expand_tree(self):
        """Expand tree capacity."""
        new_size = self.MAXN * 2
        self.tree.extend([None] * self.MAXN)
        self.MAXN = new_size

    def get_similar_words(self, s: str, tol) -> list[str]:
        """Get list of similar words."""
        nodes = self.get_similar_words_helper(0, s, tol)
        return [node.word for node in nodes]
    
    def get_entity_rank_by_similar_words(self, s: str, tol) -> list[tuple[str, int]]:
        """Get ranked list of entities by frequency."""
        result = defaultdict(int)
        similar_nodes = self.get_similar_words_helper(0, s, tol)
        
        for node in similar_nodes:
            for entity, count in node.entity_counts.items():
                result[entity] += count
        
        return sorted(result.items(), key=lambda x: x[1], reverse=True)

    def get_similar_words_helper(self, node_idx, s, tol):
        """Recursively find similar words."""
        if node_idx == -1:
            return []
        
        node = self.tree[node_idx]
        if not node or not node.word:
            return []

        results = []
        dist = self.edit_distance(node.word, s)

        if dist <= tol:
            results.append(node)
        
        # Only check valid distance range
        low = max(0, dist - tol)
        high = min(self.max_dist - 1, dist + tol)
        
        for i in range(low, high + 1):
            next_idx = node.next[i]
            if next_idx != -1:
                results.extend(self.get_similar_words_helper(next_idx, s, tol))
        
        return results