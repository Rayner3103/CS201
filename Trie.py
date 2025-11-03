from collections import defaultdict

class Node:
    def __init__(self):
        # 26 English lowercase letters (a–z)
        self.links = [None] * 26
        self.is_end_of_word = False
        # airline_name → count of times this word appears for that airline
        self.airline_counts = defaultdict(int)

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

    def insert(self, word, airline_name):
        """
        Insert a word and increment count for airline_name.
        """
        node = self.root
        for ch in word.lower():
            if not ('a' <= ch <= 'z'):
                continue  # skip non-letter characters
            if not node.contains_key(ch):
                node.put(ch, Node())
            node = node.get(ch)
        node.set_end()
        node.airline_counts[airline_name] += 1  

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

    def get_airlines_for_word(self, word):
        """
        Return dict of airline → count for an exact word.
        """
        node = self._search_prefix(word)
        if node and node.is_end():
            return dict(node.airline_counts)
        return {}

    def get_words_and_airlines_starting_with(self, prefix):
        """
        Return list of (word, {airline: count}) for all words starting with prefix.
        """
        results = []
        node = self._search_prefix(prefix)
        if node is None:
            return results

        self._dfs(node, list(prefix.lower()), results)
        return results

    def _dfs(self, node, path, results):
        if node.is_end():
            word = "".join(path)
            results.append((word, dict(node.airline_counts)))

        for i in range(26):
            if node.links[i] is not None:
                path.append(chr(i + ord('a')))
                self._dfs(node.links[i], path, results)
                path.pop()

    def get_airline_ranking_for_prefix(self, prefix):
        """
        Aggregate total counts across all words starting with prefix.
        Return airlines ranked by frequency.
        """
        results = self.get_words_and_airlines_starting_with(prefix)
        total_counts = defaultdict(int)

        # aggregate counts across all matching words
        for word, airline_counts in results:
            for airline, count in airline_counts.items():
                total_counts[airline] += count

        # sort descending by frequency
        ranked = sorted(total_counts.items(), key=lambda x: x[1], reverse=True)
        return ranked


# ------------------- Example Usage -------------------
if __name__ == "__main__":
    trie = Trie()

    # Simulate multiple reviews per airline
    sample_data = [
        ("delay", "AirAsia"),
        ("delay", "AirAsia"),
        ("delay", "AirAsia"),
        ("delay", "Scoot"),
        ("delayed", "AirAsia"),
        ("delayed", "Jetstar"),
        ("delays", "AirAsia"),
        ("delight", "SingaporeAir"),
        ("service", "Emirates"),
        ("service", "Emirates"),
    ]

    for word, airline in sample_data:
        trie.insert(word, airline)

    print("Words and airline counts for prefix 'del':")
    results = trie.get_words_and_airlines_starting_with("del")
    for word, counts in results:
        print(f"{word:10s} → {counts}")

    print("\nAirline ranking for prefix 'del':")
    ranking = trie.get_airline_ranking_for_prefix("del")
    for airline, total in ranking:
        print(f"{airline:15s} {total}")
