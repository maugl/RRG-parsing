from copy import deepcopy


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
            if not ch.is_leaf:
                rules.union(generate_rules(ch.children))
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

    print(generate_rules(templates))

    """
    print(templates[0].subsume_template(templates[1]))
    print(templates[0].tostr())
    """