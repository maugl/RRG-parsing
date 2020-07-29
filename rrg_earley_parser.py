from copy import deepcopy


class State:
    def __init__(self, production, p, j, f, alpha, dot):
        self.production = production
        self.p = p  # int 0 <= p <= d - 1, index of production in state_set
        self.j = j  # int 0 <= j <= p' where p' is the number of symbols on the right-hand side in a production (indicates the "dot")
        self.f = f  # int 0 <= f <= n+1
        self.alpha = alpha  # list of terminal symbols
        self.dot = dot  # index of where the dot is located in the production (it is assumed to be before the index without occupying an index itself)

    def is_final(self):
        return self.j == len(self.production[1])

    def __eq__(self, other):
        return type(other) is type(self) and self.p == other.p and self.j == other.j and self.f == other.f\
               and self.alpha == other.alpha

    def __str__(self):
        """
                prod = self.production[1].copy()
                prod.insert(self.j, ".")
                return " ".join([str(symb) for symb in self.production[0]]) + " -> " + " ".join([str(symb) for symb in prod])\
                    + " " + str(self.alpha)
        """

        return "(" + ", ".join([str(self.production), str(self.p), str(self.j), str(self.f), str(self.alpha), str(self.dot)]) + ")"

    def __repr__(self):
        return str(self)


class Symbol:
    """
    represents one symbol of a grammar
    """
    def __init__(self, symbol, is_terminal=False):
        self.symbol = symbol
        self.is_terminal = is_terminal
        self.is_non_terminal = not self.is_terminal

    def __eq__(self, other):
        return type(other) == type(self) and other.symbol == self.symbol and other.is_terminal == self.is_terminal

    def __str__(self):
        return self.symbol

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(self.symbol + str(self.is_terminal))


class RRG_earley_parser:
    def __init__(self, input_string, grammar, root, end_symbol=Symbol("<\\s>", is_terminal=True), start_symbol=None):
        self.state_set = list()  # nested lists one state list for each step in the recognition process
        self.X = None
        self.G = grammar  # list of productions: [([symb], [symb, symb]), ([symb], [symb, symb, symb])]
        self.terminals = list()
        self.terminals = list(set([symbol for prod in grammar for side in prod for symbol in side if
                                   symbol.is_terminal]))
        self.non_terminals = list(set([symbol for prod in grammar for side in prod for symbol in side if
                                       symbol.is_non_terminal]))
        self.end_symbol = end_symbol
        self.start_symbol = start_symbol
        self.root = root

    def initiate(self):
        self.X.append(self.end_symbol)
        # create start_symbol for grammar
        if not self.start_symbol:
            self.start_symbol = Symbol("S") if Symbol("S") not in self.non_terminals else None

        if not self.start_symbol:
            for nt in self.non_terminals:
                self.start_symbol = Symbol(str(hash(nt))) if Symbol(str(hash("nt"))) not in self.non_terminals else None
                if self.start_symbol:
                    break
        if not self.start_symbol:
            raise RuntimeError("Cannot create start symbol of grammar")

        self.start_symbol = self.start_symbol

        # add start_symbol
        self.non_terminals.append(self.start_symbol)

    def recognizer(self, input_string, k=1):
        self.X =
        start_production = ([self.start_symbol], [self.root] + [self.end_symbol for _ in range(k)])
        self.G.append(start_production)

        print(self.G)

        self.state_set = list(list() for _ in range(len(self.X) + 1))
        self.state_set[0].append(State(start_production, -1, 0, 0, [self.end_symbol for _ in range(k)], 0))

        end_state = State(start_production, -1, 2, 0, [self.end_symbol for _ in range(k)], 0)
        for i, ch in enumerate(self.X):
            z = 0
            while z < len(self.state_set[i]):
                s = self.state_set[i][z]
                if not s.is_final() and s.production[1][s.j].is_non_terminal:
                    self.predictor(s, i, k)
                elif s.is_final() and s.alpha == self.X[i:i+k]:
                    self.completer(s, i)
                elif not s.is_final() and s.production[1][s.j].is_terminal:
                    self.scanner(s, i)
                z += 1
            print("states " + str(i))
            for st in self.state_set[i]:
                print(st, st.is_final())
            if len(self.state_set[i+1]) == 0:
                return False
            if i == len(self.X) - k and self.state_set[i+1][0] == end_state:
                return True
        print("done")

    def predictor(self, state, X_index, k):
        new_productions = [(q, prod) for q, prod in enumerate(self.G) if state.production[1][state.j] == prod[0][0]]
        beta = list() # criterion for lookahead, Earley p.97 ????
        if len(state.production[1]) > state.j+1+k:
            for symb in state.production[1][state.j+1:state.j+1+k]:
                if symb.is_terminal:
                    beta.append(symb)
                else:
                    beta = state.alpha
                    break
        else:
            beta = state.alpha

        for q, prod in new_productions:
            new_state = State(prod, q, 0, X_index, beta, -1)
            if new_state not in self.state_set[X_index]:
                self.state_set[X_index].append(new_state)

    def scanner(self, state, X_index):
        if state.production[1][state.j] == self.X[X_index]:
            state_new = deepcopy(state)
            state_new.j += 1
            if state_new not in self.state_set[X_index + 1]:
                self.state_set[X_index + 1].append(state_new)

    def completer(self, state, X_index):
        for s in self.state_set[state.f]:
            if state.production[0][0] == s.production[1][s.j]:
                new_state = deepcopy(s)
                new_state.j += 1
                if new_state not in self.state_set[X_index]:
                    self.state_set[X_index].append(new_state)



if __name__ == "__main__":
    grammar = [
        ([Symbol("E")], [Symbol("E"), Symbol("+", is_terminal=True), Symbol("T")]),
        ([Symbol("E")], [Symbol("T")]),
        ([Symbol("T")], [Symbol("T"), Symbol("*", is_terminal=True), Symbol("P")]),
        ([Symbol("T")], [Symbol("P")]),
        ([Symbol("P")], [Symbol("a", is_terminal=True)])
    ]

    parser = RRG_earley_parser(["a", "+", "a", "*", "a"], grammar, Symbol("E"))
    parser.initiate()
    """
    print(parser.X)
    print(parser.G)
    print(parser.terminals)
    print(parser.non_terminals)
    """
    print(parser.recognizer(k=2))
#    for states in parser.state_set:
#        print(states)
