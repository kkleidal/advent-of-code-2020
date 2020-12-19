import sys


def parse_rules(rules_str):
    rules = {}
    for line in rules_str.strip().split("\n"):
        rule_id, rule_def = line.strip().split(": ")
        rule_id = int(rule_id)
        tokens = rule_def.split(" ")
        clauses = []
        clause = []
        for token in tokens:
            if token[0] == '"':
                literal = token[1:-1]
                clause.append(literal)
            elif token[0] == "|":
                clauses.append(clause)
                clause = []
            else:
                clause.append(int(token))
        if len(clause) > 0:
            clauses.append(clause)
        rules[rule_id] = clauses
    return rules


def match_clause(value, clause):
    if len(clause) == 0:
        yield ""
    else:
        rule_id = clause[0]
        for possible_match1 in match_rule(value, rule_id):
            subvalue = value[len(possible_match1) :]
            for possible_match2 in match_clause(subvalue, clause[1:]):
                yield possible_match1 + possible_match2


def match_rule(value, rule_id=0):
    if isinstance(rule_id, str):
        if len(value) > 0 and value[0] == rule_id:
            yield rule_id
    else:
        clauses = rules[rule_id]
        for clause in clauses:
            for possible_match in match_clause(value, clause):
                yield possible_match


def is_match(value):
    return any(pm == value for pm in match_rule(value))


state = 0
rules_strs = []
matches = 0
for line in sys.stdin:
    line = line.strip()
    if state == 0:
        if line != "":
            rules_strs.append(line)
        else:
            rules = parse_rules("\n".join(rules_strs))
            state = 1
    else:
        if line:
            if is_match(line):
                print("   MATCH", line)
                matches += 1
            else:
                print("NO MATCH", line)
print(matches)
