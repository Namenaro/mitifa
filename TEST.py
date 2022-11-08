from collections import namedtuple
from operator import attrgetter
from bisect import bisect, insort
from pprint import pprint

''' ExemplarEntry = namedtuple('ExemplarEntry', ('exemplar', 'non_triviality'))

entries = []



entry = ExemplarEntry('three', 3)
insort(entries, entry, key= lambda x : -x.non_triviality)

entry = ExemplarEntry('4three', 4)
insort(entries, entry,  key= lambda x : -x.non_triviality)

entry = ExemplarEntry('4three', 4)
insort(entries, entry,  key= lambda x : -x.non_triviality)

pprint(entries)

for entry in entries:
    print (entry.exemplar)

entries = entries[:2]

pprint(entries) 

from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree
X = csr_matrix([[0, 8, 0, 3.2],
                [8, 0, 2, 5],
                [0, 2, 0, 6],
                [3.2, 5, 6, 0]])
Tcsr = minimum_spanning_tree(X)
print(Tcsr.toarray().astype(float))
'''
