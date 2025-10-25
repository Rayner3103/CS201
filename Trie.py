class Node:
    def __init__(self):
        # 26 English lowercase letters (a–z)
        self.links = [None] * 26
        self.is_end_of_word = False

    def contains_key(self, ch):
        return self.links[ord(ch) - ord('a')] is not None

    def get(self, ch):
        return self.links[ord(ch) - ord('a')]

    def put(self, ch, node):
        self.links[ord(ch) - ord('a')] = node

    def set_end(self):
        self.is_end_of_word = True

    def is_end(self):
        return self.is_end_of_word


class Trie:
    def __init__(self):
        self.root = Node()

    def insert(self, word):
        node = self.root
        for ch in word.lower():
            if not ('a' <= ch <= 'z'):
                continue  # skip non-letter characters
            if not node.contains_key(ch):
                node.put(ch, Node())
            node = node.get(ch)
        node.set_end()

    def search(self, word):
        node = self._search_prefix(word)
        return node is not None and node.is_end()

    def starts_with(self, prefix):
        node = self._search_prefix(prefix)
        return node is not None

    def _search_prefix(self, word):
        node = self.root
        for ch in word.lower():
            if not ('a' <= ch <= 'z'):
                continue
            if node.contains_key(ch):
                node = node.get(ch)
            else:
                return None
        return node

    # Equivalent to getWordsStartingWith()
    def get_words_starting_with(self, prefix):
        results = []
        node = self._search_prefix(prefix)
        if node is None:
            return results  # no such prefix

        self._dfs(node, list(prefix.lower()), results)
        return results

    def _dfs(self, node, path, results):
        if node.is_end():
            results.append("".join(path))

        for i in range(26):
            if node.links[i] is not None:
                path.append(chr(i + ord('a')))
                self._dfs(node.links[i], path, results)
                path.pop()


# ------------------- Example Usage -------------------
if __name__ == "__main__":
    trie = Trie()
    trie.insert("delay")
    trie.insert("delayed")
    trie.insert("delight")
    trie.insert("service")

    print(trie.get_words_starting_with("del"))
