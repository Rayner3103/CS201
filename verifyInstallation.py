try:
    import time
    import random
    import re

    import matplotlib.pyplot as plt
    import pandas as pd

    from collections import defaultdict
    from datetime import datetime
    from pympler import asizeof
    from Levenshtein import distance as levenshtein_distance

    from data_structures.Trie import Trie
    from data_structures import Array_BKTree
    from data_structures import Linked_BKTree
    from utils import *

    print("All libraries installed successfully.")

except ImportError as e:
    print("Error -> ", e)