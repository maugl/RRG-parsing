from copy import deepcopy
from rrg_earley_parser import Symbol
from rrg_earley_parser import RRG_earley_parser

class Template:
    def __init__(self, name=None, children=None):
        self.name = name
        self.children = list() if children is None else children

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def add_child(self, child):
        assert(type(child) is Template)
        self.children.append(child)
        return self

    def is_leaf(self):
        return len(self.children) == 0

    def subsume_template(self, template):
        for i, ch in enumerate(self.children):
            if ch.is_leaf:
                if ch.get_name() == template.get_name():
                    self.children[i] = template
                    return True
            else:
                if ch.subsume_template(template):
                    return True
                else:
                    continue
        return False

    def get_deepcopy(self):
        return deepcopy(self)

    def tostr(self):
        return [self.name, [ch.tostr() for ch in self.children]]


def generate_rules(templates):
    rules = set()
    for temp in templates:
        rules.add((temp.name, tuple([ch.name for ch in temp.children])))
        for ch in temp.children:
            if not ch.is_leaf():
                rules.union(generate_rules(ch.children))
    return rules


def generate_grammar(temps, all_temps=None, ind=None):
    rules = list()
    all_temps = temps if all_temps is None else all_temps

    for i, temp in enumerate(temps):
        index = i if ind is None else ind

        left_side = [Symbol(temp.name, is_terminal=False)]
        right_side = [Symbol(ch.name, is_terminal=ch.is_leaf() and not
        max([ch.get_name() == atemp.get_name() for atemp in all_temps])) for ch in temp.children]
        gen_rule = (left_side, right_side, index)
        if gen_rule not in rules:
            rules.append(gen_rule)
        for ch in temp.children:
            if not ch.is_leaf():
                new_rules = generate_grammar([ch], all_temps, ind=index)
                for r in new_rules:
                    if r not in rules:
                        rules.append(r)
    return rules

if __name__ == "__main__":
    templates = list()
    templates.append(Template("SENTENCE", [Template("LDP"), Template("CLAUSE")]))
    templates.append(Template("SENTENCE", [Template("CLAUSE")]))
    templates.append(Template("CLAUSE", [Template("CORE")]))
    templates.append(Template("CLAUSE", [Template("PrCS"), Template("CORE")]))
    templates.append(Template("CORE", [Template("NUC").add_child(Template("PRED").add_child(Template("V"))), Template("RP")]))
    templates.append(Template("CORE", [Template("RP"), Template("NUC").add_child(Template("PRED").add_child(Template("V"))), Template("PP")]))
    templates.append(Template("CORE", [Template("RP"), Template("NUC").add_child(Template("PRED").add_child(Template("V"))), Template("RP")]))
    templates.append(Template("CORE", [Template("RP"), Template("NUC").add_child(Template("PRED").add_child(Template("V")))]))
    templates.append(Template("CORE", [Template("RP"), Template("NUC").add_child(Template("PRED").add_child(Template("V"))), Template("RP"), Template("PP")]))
    templates.append(Template("CORE", [Template("RP"), Template("NUC").add_child(Template("PRED").add_child(Template("V"))), Template("RP"), Template("RP")]))
    templates.append(Template("RP", [Template("N")]))
    templates.append(Template("VP", [Template("V")]))

    for t in templates:
        print(t.tostr())

    grammar = generate_grammar(templates)

    for rule in grammar:
        print(rule)

    parser = RRG_earley_parser(grammar, Symbol("SENTENCE"))
    parser.initiate()

    print(parser.G)
    print(parser.terminals)
    print(parser.non_terminals)


    parser.recognizer(["V", "N"])


    """
    print(templates[0].subsume_template(templates[1]))
    print(templates[0].tostr())
    """