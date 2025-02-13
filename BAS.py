from sage.combinat.root_system.weyl_group import WeylGroup
from sage.sets.set import Set
from sage.combinat.posets.posets import Poset
from sage.graphs.graph import Graph

def hroot (r):
    return sum(WeylGroup(['A', r], implementation = 'permutation').simple_roots())

def weightify(r, L):
    if L == 0:
            return 0;
    W = WeylGroup(['A', r], implementation = 'permutation');
    alpha = list(W.simple_roots());
    return sum([
            L[i] * alpha[i] for i in range(len(L))
    ]);

def influence (w):
    return Set(w.reduced_word())

def is_connected (J):
    if len(J) <= 1:
        return True;
    for j in range(min(J) + 1, max(J)):
        if j not in J:
            return False;
    return True
    

def connected_influences (r, L, M):
    W = WeylGroup(['A', r], implementation = 'permutation');
    alpha = list(W.simple_roots());
    rho = 1/2*sum(W.positive_roots());
    
    def act_on_weight(w, L):
        return sum([
            L[i] * w.action_on_root(alpha[i]) for i in range(len(alpha))
        ])
    
    if type(L) != type(rho):
        L = weightify(r, L);
    
    if type(M) != type(rho):
        M = weightify(r, M);
    
    out = set();

    for w in W:
        J = influence(w);
        if J not in out and is_connected(J) and len(J) > 0:
            if min(act_on_weight(w, L + rho) - rho - M) >= 0:
                out.add(J)
    
    return out

# Returns the set of connected influences ordered by containment
def connected_influences_poset (r, L, M):
    influences = connected_influences(r, L, M);
    relations = {}

    for s in influences:
        relations[s] = [t for t in influences if s in t.subsets() and s != t]

    return Poset(relations);

def extend (I):
    J = set();
    for i in I:
        J.add(i - 1);
        J.add(i);
        J.add(i + 1);
    
    return J;

# Returns the set of connected influences with an edge whenever
# two influences are not independent
def connected_influences_graph (r, L, M):
    influences = connected_influences(r, L, M);
    relations = {}

    G = Graph();

    for I in influences:
        for J in influences:
            if I != J and len(extend(I).intersection(J)) > 0:
                G.add_edge(I,J)

    return G;