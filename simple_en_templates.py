from lsc_parser import Template

templates = list()
templates.append(Template("SENTENCE", [Template("LDP"), Template("CLAUSE")]))
templates.append(Template("SENTENCE", [Template("CLAUSE")]))
templates.append(Template("CLAUSE", [Template("CORE")]))
templates.append(Template("CLAUSE", [Template("PrCS"), Template("CORE")]))
templates.append(
    Template("CORE", [Template("NUC").add_child(Template("PRED").add_child(Template("V"))), Template("RP")]))
templates.append(Template("CORE", [Template("RP"), Template("NUC").add_child(Template("PRED").add_child(Template("V"))),
                                   Template("PP")]))
templates.append(Template("CORE", [Template("RP"), Template("NUC").add_child(Template("PRED").add_child(Template("V"))),
                                   Template("RP")]))
templates.append(
    Template("CORE", [Template("RP"), Template("NUC").add_child(Template("PRED").add_child(Template("V")))]))
templates.append(Template("CORE", [Template("RP"), Template("NUC").add_child(Template("PRED").add_child(Template("V"))),
                                   Template("RP"), Template("PP")]))
templates.append(Template("CORE", [Template("RP"), Template("NUC").add_child(Template("PRED").add_child(Template("V"))),
                                   Template("RP"), Template("RP")]))
templates.append(Template("RP", [Template("N")]))
templates.append(Template("VP", [Template("V")]))
