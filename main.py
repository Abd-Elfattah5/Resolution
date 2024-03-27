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
        i += 1
        length = len(final)
    return final


test = "∀y((∃x Test(y, x)) ∧ Easy(y) ⇒ ∀z Pass(z, y))"
print(elimination_universal(prenex_form(test)))
