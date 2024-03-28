import random
import string

def insert_letter(original_string, letter, position):
    return ''.join([original_string[:position], letter, original_string[position:]])


def replace_letter(original_string, letter, position):
    return ''.join([original_string[:position], letter, original_string[position + 1:]])


def remove_implication(text):
    q = []
    final = text
    length = len(final)
    i = 0
    while i < length:
        if final[i] == '→':
            final = replace_letter(final, 'v', i)
            j = i - 2
            while j >= 0:
                if final[j] == ')':
                    q.append(final[j])
                elif final[j] == '(' and len(q) != 0:
                    q.pop()
                if len(q) == 0:

                    final = insert_letter(final, '¬', j)
                    break
                j -= 1
        length = len(final)
        i += 1
    return final


def double_negation(text):
    final = text
    i = 0
    length = len(final)

    while i < length - 1:
        if final[i] == '¬' and final[i + 1] == '¬':
            final = replace_letter(final, '', i)
            final = replace_letter(final, '', i)
        length = len(final)
        i += 1

    return final


def prenex_form(text):
    final = text
    i = 0
    length = len(final)

    while i < length:
        if final[i] == '∀' or final[i] == '∃':
            while i < length:
                if (final[i] == '∃' or final[i] == '∀') and str.islower(final[i + 1]):
                    i += 2
                else:
                    break
            j = i
            while j < length:
                if final[j] == '∀' or final[j] == '∃':
                    final = insert_letter(final, final[j], i)
                    final = replace_letter(final, '', j + 1)
                    j += 1
                    i += 1
                    final = insert_letter(final, final[j], i)
                    final = replace_letter(final, '', j + 1)
                    i += 1
                j += 1
            if j >= length:
                break
        i += 1
    return final


def de_morgan(text):
    final = text
    i = 0
    length = len(final)
    q = []
    new = True

    while i < length:
        if final[i] == '¬':
            final = replace_letter(final, '', i)
            while i < length and (new or (len(q) != 0)):
                if final[i] == '∀':
                    final = replace_letter(final, '∃', i)
                elif final[i] == '∃':
                    final = replace_letter(final, '∀', i)
                elif str.isupper(final[i]):
                    final = insert_letter(final, '¬', i)
                    i += 1
                elif final[i] == '(':
                    new = False
                    q.append(final[i])
                elif final[i] == ')':
                    q.pop()
                elif final[i] == '∨':
                    final = replace_letter(final, '∧', i)
                elif final[i] == '∧':
                    final = replace_letter(final, '∨', i)
                length = len(final)
                i += 1
        length = len(final)
        i += 1
    return final


def elimination_universal(text):
    final = text
    i = 0
    length = len(final)

    while i < length:
        if final[i] == '∀' and str.islower(final[i + 1]):
            final = replace_letter(final, '', i)
            final = replace_letter(final, '', i)
            i -= 1
        i += 1
        length = len(final)
    return final


def skolmization(text):
    final = text
    q_para = []
    q_quant_A = []
    q_quant_E = []
    i = 0
    length = len(final)

    while i < length:
        if final[i] == '∀':
            q_quant_A.append(final[i + 1])
        elif final[i] == '∃':
            q_quant_E.append(final[i + 1])
            final = replace_letter(final, '', i)
            final = replace_letter(final, '', i)
            continue
        elif final[i] == '(':
            if len(q_quant_E) == 0:
                q_quant_A = []
            else:
                q_para.append(final[i])
        elif final[i] == ')' and len(q_para) != 0:
            q_para.pop()
        elif final[i] in q_quant_E and len(q_para) != 0:
            if len(q_quant_A) != 0:
                rd = "F{}".format(random.randrange(0, 100, 1))
                co = "{}({})".format(rd, q_quant_A).replace('[', '').replace(']', '').replace('\'', '')
                final = replace_letter(final, co, i)
            else:
                rd = ""
                for j in range(4):
                    rd = insert_letter(rd, random.choice(string.ascii_lowercase), len(rd) - 1)
                rd = insert_letter(rd, random.choice(string.ascii_uppercase), 0)
                final = replace_letter(final, rd, i)
        i += 1
    return final


def distribute_or_over_and(text):
    parts = text.split("∨")
    if len(parts) == 1:
        return [text]
    else:
        left = distribute_or_over_and(parts[0])
        right = distribute_or_over_and("∨".join(parts[1:]))
        return [l + r for l in left for r in right]


def fol_to_conjunction(text):
    text = remove_implication(text)
    disjunctions = distribute_or_over_and(text)
    return "∧".join(disjunctions)


def divide_into_clauses(formula):
    clauses = formula.split("∧")
    return [clause.strip() for clause in clauses]


def standardize(text):
    i = 0
    final = text
    var = []
    length = len(final)

    while i < length:
        if str.islower(final[i]):
            if final[i] not in var:
                var.append(final[i])
            else:
                rd = final[i]
                while rd in var:
                    rd = random.choice(string.ascii_lowercase)
                str.replace(final, final[i], rd)
        i += 1
    return final


def convert_to_CNF(text):
    final = text
    print("start: {}".format(final))
    final = remove_implication(final)
    print("after removing implication: {}".format(final))
    final = de_morgan(final)
    print("after DeMorgan: {}".format(final))
    final = double_negation(final)
    print("after removing double negation: {}".format(final))
    # final = standardize(final)
    # print("after standardization: {}")
    final = prenex_form(final)
    print("Moving quantifiers to the left: {}".format(final))
    final = skolmization(final)
    print("replacing there exist: {}".format(final))
    final = elimination_universal(final)
    print("eliminating universal quantifiers: {}".format(final))
    final = fol_to_conjunction(final)
    print("converting to conjunction form: {}".format(final))
    final = divide_into_clauses(final)
    print("clauses: {}".format(final))


test = "∃x∀y∀z (((P(y)) → (Q(z))) → ((P(x)) → (Q(x))))"
convert_to_CNF(test)