import argparse


class Lexicon:
    def __init__(self):
        self.data = dict()
        self.len = 0

    def get(self, word):
        if type(self.data[word]) is not dict:
            return self.data[self.data[word]]
        else:
            return self.data[word]

    def get_type(self, word):
        if word not in self.data:
            return None
        else:
            return self.get(word)["type"]

# first only encode number of arguments/macro-roles
pred_lexicon = Lexicon()
pred_lexicon.data = {
    "run": {"lemma": "run", "mr": [1, 2], "type": "V", "pred": ["run", "be-LOC"], "act_art": {"ACTIVITY": [0, 1], "ACTIVE_ACCOMPLISHMENT": [0]}},
    "runs": "run",  # variant: reference to entry, can be used to define operators (tense, aspect,...)
    "drive": {"lemma": "drive", "mr": [1, 2], "type": "V", "pred": ["drive", "be-LOC"], "act_art": {"ACTIVITY": [0, 1], "ACTIVE_ACCOMPLISHMENT": [0]}},
    "drives": "drive",
    "eat": {"lemma": "eat", "mr": [1, 2], "type": "V", "pred": ["eat", "consumed"], "act_art": {"ACTIVITY": [1], "ACTIVE_ACCOMPLISHMENT": [1]}},
    "carry": {"lemma": "carry", "mr": [2], "type": "V", "pred": ["carry"], "act_art": {"ACTIVITY": [1]}},
    "carries": "carry",
    "do": {"lemma": "do", "mr": [2], "type": "V", "pred": ["do"], "act_art": {"ACTIVITY": [1]}},
    "race": {"lemma": "race", "mr": [1, 2], "type": "V", "pred": ["race"], "act_art": {"ACTIVITY": [1]}},
    "break": {"lemma": "break", "mr": [1, 2], "type": "V", "pred": ["break"], "act_art": {"ACHIEVEMENT": [0]}},
    "breaks": "break"
}

# first encode possible macro-roles
arg_lexicon = Lexicon()
arg_lexicon.data = {
    "i": {"lemma": "i", "mr": ["actor"], "type": "N",
          "thematic_role": ["EFFECTOR", "MOVER", "ST-MOVER", "S-EMITTER", "PERFORMER", "CONSUMER", "CREATOR",
                            "OBSERVER", "USER", "PERCEIVER", "COGNIZER", "WANTER", "JUDGER", "POSSESSOR",
                            "EXPERIENCER", "EMOTER"]
          }, # not correct, but used for development purposes
    "he": {"lemma": "he", "mr": ["actor"], "type": "N",
           "thematic_role": ["EFFECTOR", "MOVER", "ST-MOVER", "S-EMITTER", "PERFORMER", "CONSUMER", "CREATOR",
                             "OBSERVER", "USER", "PERCEIVER", "COGNIZER", "WANTER", "JUDGER", "POSSESSOR",
                             "EXPERIENCER", "EMOTER"]
           },
    "car": {"lemma": "car", "mr": ["actor", "undergoer"], "type": "N",
            "thematic_role": ["MOVER", "L-EMITTER", "S-EMITTER", "CONSUMER", "LOCATION", "POSSESSOR", "ATTRIBUTANT",
                              "IDENTIFIED", "VARIABLE", "THEME", "CONTENT", "POSSESSED", "TARGET",
                              "IDENTITY", "VALUE", "CREATION", "IMPLEMENT", "PATIENT", "ENTITY"]
            },
    "cars": "car",  # variant: reference to entry
    "me": {"lemma": "me", "mr": ["undergoer"], "type": "N",
           "thematic_role": ["ATTRIBUTANT", "IDENTIFIED", "VARIABLE", "THEME", "STIMULUS", "CONTENT", "DESIRE",
                             "JUDGMENT", "POSSESSED", "SENSATION", "TARGET", "ATTRIBUTE", "IDENTITY", "VALUE",
                             "PERFORMANCE", "CONSUMED", "CREATION", "PATIENT", "ENTITY"]
           },
    "her": {"lemma": "her", "mr": ["undergoer"], "type": "N",
            "thematic_role": ["ATTRIBUTANT", "IDENTIFIED", "VARIABLE", "THEME", "STIMULUS", "CONTENT", "DESIRE",
                             "JUDGMENT", "POSSESSED", "SENSATION", "TARGET", "ATTRIBUTE", "IDENTITY", "VALUE",
                             "PERFORMANCE", "CONSUMED", "CREATION", "PATIENT", "ENTITY"]
            },
    "run": {"lemma": "run", "mr": ["actor", "undergoer"], "type": "N",
            "thematic_role": ["EFFECTOR", "LOCATION", "ATTRIBUTANT", "IDENTIFIED", "VARIABLE", "THEME",
                              "CONTENT", "TARGET", "ATTRIBUTE", "IDENTITY", "VALUE", "CREATION", "IMPLEMENT",
                              "PATIENT", "ENTITY"]
            },
    "runs": "run",
    "race": {"lemma": "race", "mr": ["actor", "undergoer"], "type": "N",
             "thematic_role": ["EFFECTOR", "LOCATION", "ATTRIBUTANT", "IDENTIFIED", "VARIABLE", "THEME",
                              "CONTENT", "TARGET", "ATTRIBUTE", "IDENTITY", "VALUE", "CREATION", "IMPLEMENT",
                              "PATIENT", "ENTITY"]
             },
    "man": {"lemma": "man", "mr": ["actor", "undergoer"], "type": "N",
            "thematic_role": ["EFFECTOR", "MOVER", "ST-MOVER", "S-EMITTER", "PERFORMER", "CONSUMER",
                              "CREATOR", "OBSERVER", "USER", "PERCEIVER", "COGNIZER", "WANTER", "JUDGER",
                              "POSSESSOR", "EXPERIENCER", "EMOTER", "ATTRIBUTANT", "IDENTIFIED", "VARIABLE",
                              "CONTENT", "DESIRE", "POSSESSED", "TARGET", "ATTRIBUTE", "IDENTITY",
                              "VALUE", "PERFORMANCE", "CONSUMED", "CREATION", "IMPLEMENT", "PATIENT", "ENTITY"]
            },
    "window": {"lemma": "window", "mr": ["undergoer"], "type": "N"}
}

aktionsart = {
    "STATE": ["pred(x)",
              "pred(x,y)"],
    "ACTIVITY": ["do(x,pred(x))",
                 "do(x,pred(x,y))"],
    "ACHIEVEMENT": ["INGR pred(x)",
                    "INGR pred(x,y)",
                    "INGR do(x,pred(x))",
                    "INGR do(x,pred(x,y))"],
    "SEMELFACTIVE": ["SEML pred(x)",
                     "SEML pred(x,y)",
                     "SEML do(x,pred(x))",
                     "SEML do(x,pred(x,y))"],
    "ACCOMPLISHMENT": ["BECOME pred(x)",
                       "BECOME pred(x,y)",
                       "BECOME do(x,pred(x))",
                       "BECOME do(x,pred(x,y))"],
    "ACTIVE_ACCOMPLISHMENT": ["do(x,pred(x)) & INGR pred2(z,x)",
                              "do(x,pred(x,y)) & INGR pred2(y)"],
    "CAUSATIVE": ["a CAUSE b"]
}
"""
verb_classes = {
    "motion": {
        "ACTIVE_ACCOMPLISHMENT": lambda log, pred: log.replace("pred", pred) + " & INGR be-LOC(x,y)"
    },
    "creation":{
        "ACTIVE_ACCOMPLISHMENT": lambda log: log + " & INGR exist(y)"
    },
    "consumption":{
        "ACTIVE_ACCOMPLISHMENT": lambda log: log + " & INGR consumed(y)"
    },
    "destruction": {
        "ACTIVE_ACCOMPLISHMENT": lambda log: log + " & INGR destroyed(y)"
    },
    "vehicle_use": {
        "ACTIVE_ACCOMPLISHMENT": lambda log, pred: log.replace("pred", pred) + " & INGR be-LOC(x,z)"
    }
}
"""
thematic_relations = {
    "do(x,": {
        "actor": [
            "EFFECTOR",
            "MOVER",
            "ST-MOVER",
            "L-EMITTER",
            "S-EMITTER",
            "PERFORMER",
            "CONSUMER",
            "CREATOR",
            "OBSERVER",
            "USER"
        ]
    },
    "pred(x,y)": {
        "actor": [
            "LOCATION",
            "PERCEIVER",
            "COGNIZER",
            "WANTER",
            "JUDGER",
            "POSSESSOR",
            "EXPERIENCER",
            "EMOTER",
            "ATTRIBUTANT",
            "IDENTIFIED",
            "VARIABLE"
        ],
        "undergoer": [
            "THEME",
            "STIMULUS",
            "CONTENT",
            "DESIRE",
            "JUDGMENT",
            "POSSESSED",
            "SENSATION",
            "TARGET",
            "ATTRIBUTE",
            "IDENTITY",
            "VALUE",
            "PERFORMANCE",
            "CONSUMED",
            "CREATION",
            "IMPLEMENT"
        ]
    },
    "pred(x)": {
        "undergoer": [
            "PATIENT",
            "ENTITY"
        ]
    }
}


operator_lexicon = {"will"}


def parse_sentence(sentence, approach="max"):
    words = split_sentence(sentence)
    comp_pred = find_pred_args(words)

    #print("compatibilities and predicates {}:".format(comp_pred))

    # only allow for compatibilities which make use of all the arguments?
    # refine compatibilities with other means? (compare to LSC, more semantic information,...)

    # maximum element usage approach
    # keep the configuration(s) which use the most elements in the sentence
    configs = list()
    if approach == "max":
        for confs, pred in comp_pred:
            max_len = max([len(comp) for comp in confs])
            confs = [comp for comp in confs if len(comp) == max_len]
            configs.append((confs, pred))

    print(configs)

    for config, pred in configs:
        for cfg in config:
            # pred, actor, undergoer
            label_inds = {
                # predicate
                "PRED": pred,
                # actor
                "ACT": cfg[0],
                # undergoer
                "UND": cfg[1] if len(cfg) > 1 else -1
            }
            # put pred, actor, undergoer in indices
            labels = ["" for w in words]
            for k, v in label_inds.items():
                if -1 < v < len(labels):
                    labels[v] = k

            types = [pred_lexicon.get_type(w) if l == "PRED" else arg_lexicon.get_type(w) for w, l in zip(words, labels)]

            yield words, labels, types


def split_sentence(text):
    split_text = text.split(" ")
    split_text = [w.strip(".").lower() for w in split_text]
    return split_text
    

def find_pred_args(sentence):
    # first find predicate canditates in list
    pred_candidate_ind = [i for i, w in enumerate(sentence) if w in pred_lexicon.data]
    # refine
    sent_args_ind = find_args(sentence)
    #args = [sentence[i] for i in sent_args_ind]
    compatibilities = list()
    # check if predicate can appear with possible arguments
    for i in pred_candidate_ind:
        compatibilities.append(check_pred_arg_compatibility(sentence, i, sent_args_ind))
        #compatibilities.append(check_pred_arg_compatibility_thematic(sentence, i, sent_args_ind))

    # if there are no compatibilities for one pred, eliminate
    comp_pred = [(comp, pred) for comp, pred in zip(compatibilities, pred_candidate_ind) if len(comp) > 0]

    return comp_pred


def find_args(sentence):

    args_ind = [i for i, w in enumerate(sentence) if w in arg_lexicon.data]

    #print("args_ind: {}".format(args_ind))
    return args_ind

def check_pred_arg_compatibility(sentence, predicate, arguments):
    """ Simple approach determining if predicates and arguments are compatible based on
    number of macroroles (predicates) and
    possible macrorole assignment (arguments)
    :param sentence:
    :param predicate:
    :param arguments:
    :return:
    """
    arg_config = list()

    #print("arguments_ind: {}".format(arguments))
    for mr in pred_lexicon.get(sentence[predicate])["mr"]:
        if mr == 1:
            # check if the argument given can appear as actor
            arg_config.extend([[arg] for arg in arguments if "actor" in arg_lexicon.get(sentence[arg])["mr"]
                               and arg != predicate])
            # only undergoer as in "the window breaks"
            if len(arg_config) < 1:
                arg_config.extend([[-1, arg] for arg in arguments if "undergoer" in arg_lexicon.get(sentence[arg])["mr"]
                                   and arg != predicate])

        if mr == 2:
            # check which of the arguments can appear as actor and/or undergoer
            if len(arguments) < 2:
                continue
            arg_config.extend([[arg1, arg2] for arg1, arg2 in zip(arguments, arguments[::-1])
                               if "actor" in arg_lexicon.get(sentence[arg1])["mr"]
                               and "undergoer" in arg_lexicon.get(sentence[arg2])["mr"]
                               and arg1 != predicate and arg2 != predicate and arg1 != arg2])

    print("arg_config: " + str(arg_config))

    return arg_config

def check_pred_arg_compatibility_thematic(sentence, predicate, arguments):
    """ approach for determining if predicates and arguments are compatible based on
    aktionsart (predicates) and
    thematic relations (arguments)

    :param sentence:
    :param predicate:
    :param arguments:
    :return:
    """
    sem_reps = list()
    for act_art, indices in pred_lexicon.get(sentence[predicate])["act_art"].items():
        sem_reps.extend([aktionsart[act_art][i] for i in indices])
    print(sem_reps)

    actor_roles = list()
    undergoer_roles = list()

    arg_config = list()

    for sem_rep in sem_reps:
        # identify x and y with thematic relations
        actor_roles.append(list())
        undergoer_roles.append(list())
        sem_rep = sem_rep.replace("INGR ", "").replace("SEML ", "").replace("BECOME ", "")
        # van valin 2005 p.63 macrorole assignment
        # get number of macro roles
        num_mr = sum([symb in sem_rep for symb in ["x", "y"]])
        # assign thematic roles to macro roles
        # can be refined with more refined semantic representations for verbs
        # print(sem_rep)
        for log, them_rel in thematic_relations.items():
            if num_mr == 1:
                    # get actors and undergoers for semantic representation
                    if sem_rep.startswith(log):
                        if "actor" in them_rel:
                            actor_roles[-1].extend(them_rel["actor"])
                            sem_rep = sem_rep.strip(log)
                        # in case no activity predicate is found
                        if "undergoer" in them_rel and len(actor_roles[-1]) < 1:
                            undergoer_roles[-1].extend(them_rel["undergoer"] if "undergoer" in them_rel else [])
                            sem_rep = sem_rep.strip(log)
            if num_mr == 2:
                if sem_rep.startswith(log):
                    actor_roles[-1].extend(them_rel["actor"] if "actor" in them_rel else [])
                    undergoer_roles[-1].extend(them_rel["undergoer"] if "undergoer" in them_rel else [])
                    sem_rep = sem_rep.strip(log)

        # find corresponding actor, undergoers from thematic roles
        if num_mr == 1:
            arg_config.extend([[arg] for arg in arguments if
                               max([r in arg_lexicon.get(sentence[arg])["thematic_role"] for r in actor_roles[-1]])
                               and arg != predicate
                               and [arg] not in arg_config])
        if num_mr == 2:
            arg_config.extend([[arg1, arg2] for arg1, arg2 in zip(arguments, arguments[::-1]) if
                               max([r in arg_lexicon.get(sentence[arg1])["thematic_role"] for r in actor_roles[-1]])
                               and max([r in arg_lexicon.get(sentence[arg2])["thematic_role"] for r in undergoer_roles[-1]])
                               and arg1 != predicate and arg2 != predicate and arg1 != arg2
                               and [arg1, arg2] not in arg_config])
    """
    for item in zip(actor_roles, undergoer_roles):
        print(item)

    print("arg_config:" + str(arg_config))
    """

    return arg_config

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description='Parse sentences in RRG.')
    ap.add_argument("filename", help="path to text file for sentence input. One sentence per line")
    ap.add_argument("-pl", "--pl", help="path to predicate lexicon. JSON encoded predicate lexicon", dest="pl")
    ap.add_argument("-al", "--al", help="path to argument lexicon. JSON encoded argument lexicon", dest="al")

    args = ap.parse_args()

    with open(args.filename, "rt", encoding="utf-8") as in_file:
        for i, line in enumerate(in_file.readlines()):
            line = line.strip("\n")
            print("sentence {}".format(i))
            parse = [p for p in parse_sentence(line)]
            print(parse)
