# Codigo desarrollado por:
# - Milan De Alba
# - Yael Morales
# - Luis Daniel Garcia
# - Antoine Ganem
# - Luis Omar Olmedo

# ---------- STATES ----------
# Each constant represents a DFA state
START = "START"
IDENTIFIER = "IDENTIFIER"
NUMBER = "NUMBER"
FLOAT = "FLOAT"
STRING_DQ = "STRING_DQ"   # "string"
STRING_SQ = "STRING_SQ"   # 'string'
STRING_BT = "STRING_BT"   # `string`
COMMENT_SL = "COMMENT_SL" # // comment
COMMENT_ML = "COMMENT_ML" # /* comment */


# ---------- DEFINITIONS ----------
KEYWORDS = {
    "if", "else", "while", "for", "function", "return", "var", "let",
    "const", "class", "import", "export", "default", "new", "this",
    "super", "extends", "try", "catch", "finally", "throw", "break",
    "continue", "switch", "case", "do", "in", "of"
}

BOOLEANS = {"true", "false"}

# Valid operators (1–3 chars)
OPERATORS = {
    "+", "-", "*", "/", "%", "=", "==", "===", "!=", "!==",
    "<", ">", "<=", ">=", "&&", "||", "!", "++", "--",
    "+=", "-=", "*=", "/=", "%="
}

# Symbols that must be balanced
OPENING = {'(': ')', '{': '}', '[': ']'}
CLOSING = {')': '(', '}': '{', ']': '['}

# All possible starting characters for operators
OPERATOR_START = set(op[0] for op in OPERATORS)


# ---------- HELPERS ----------
# Classify identifier into keyword / boolean / name
def classify_identifier(lexeme):
    if lexeme in BOOLEANS:
        return "BOOLEAN"
    if lexeme in KEYWORDS:
        return "KEYWORD"
    return "NAME"


# Match longest operator (3 → 2 → 1 chars)
def match_operator(text, i):
    for length in (3, 2, 1):
        if i + length <= len(text):
            candidate = text[i:i+length]
            if candidate in OPERATORS:
                return candidate, length
    return None, 0


# ---------- LEXER ----------
def lexer(text):
    state = START
    lexeme = ""   # current token being built
    items = []    # unified output: (TOKEN, VALUE, ERROR)
    stack = []    # used for symbol balancing
    invalid_identifier = False

    i = 0
    while i < len(text):
        c = text[i]

        # -------- START --------
        if state == START:

            if c.isalpha() or c == "_":
                state = IDENTIFIER
                lexeme += c

            elif c.isdigit():
                state = NUMBER
                lexeme += c

            elif c == '"':
                state = STRING_DQ

            elif c == "'":
                state = STRING_SQ

            elif c == "`":
                state = STRING_BT

            # ---- COMMENTS ----
            elif c == "/":
                if i + 1 < len(text):
                    if text[i+1] == "/":
                        state = COMMENT_SL
                        i += 2
                        continue
                    elif text[i+1] == "*":
                        state = COMMENT_ML
                        i += 2
                        continue
                items.append(("OPERATOR", "/", ""))

            # ---- SYMBOLS ----
            elif c in OPENING:
                stack.append(c)
                items.append(("SYMBOL", c, ""))

            elif c in CLOSING:
                if not stack or stack[-1] != CLOSING[c]:
                    items.append(("SYMBOL", c, "Símbolo no balanceado"))
                else:
                    stack.pop()
                    items.append(("SYMBOL", c, ""))

            # ---- OPERATORS ----
            elif c in OPERATOR_START:
                temp = ""

                # collect consecutive operator chars
                while i < len(text) and text[i] in OPERATOR_START:
                    temp += text[i]
                    i += 1

                # validate sequence
                j = 0
                valid = True
                while j < len(temp):
                    found = False
                    for l in (3, 2, 1):
                        if j + l <= len(temp) and temp[j:j+l] in OPERATORS:
                            j += l
                            found = True
                            break
                    if not found:
                        valid = False
                        break

                if valid and j == len(temp):
                    j = 0
                    while j < len(temp):
                        op, length = match_operator(temp, j)
                        items.append(("OPERATOR", op, ""))
                        j += length
                else:
                    items.append(("OPERATOR", temp, "Operador inválido"))

                continue

            elif c.isspace():
                pass

            else:
                items.append(("(desconocido)", c, "Carácter inválido/no reconocido"))

        # -------- IDENTIFIER --------
        elif state == IDENTIFIER:
            if c.isalnum() or c == "_":
                lexeme += c
            else:
                if invalid_identifier:
                    items.append(("NAME", lexeme, "Identificador inválido: no puede iniciar con dígito"))
                else:
                    items.append((classify_identifier(lexeme), lexeme, ""))

                lexeme = ""
                state = START
                invalid_identifier = False
                continue

        # -------- NUMBER --------
        elif state == NUMBER:
            if c.isdigit():
                lexeme += c

            elif c.isalpha():
                lexeme += c
                invalid_identifier = True
                state = IDENTIFIER

            elif c == ".":
                state = FLOAT
                lexeme += c

            else:
                items.append(("NUMBER", lexeme, ""))
                lexeme = ""
                state = START
                continue

        # -------- FLOAT --------
        elif state == FLOAT:
            if c.isdigit():
                lexeme += c
            else:
                if lexeme.endswith("."):
                    items.append(("NUMBER", lexeme, "Número flotante inválido"))
                else:
                    items.append(("NUMBER", lexeme, ""))
                lexeme = ""
                state = START
                continue

        # -------- STRINGS --------
        elif state in (STRING_DQ, STRING_SQ, STRING_BT):
            closing = '"' if state == STRING_DQ else "'" if state == STRING_SQ else "`"

            if c == closing:
                items.append(("STRING", lexeme, ""))
                lexeme = ""
                state = START

            elif c == "\n":
                items.append(("STRING", lexeme, "Cadena no terminada"))
                lexeme = ""
                state = START

            else:
                lexeme += c

        # -------- COMMENTS --------
        elif state == COMMENT_SL:
            if c == "\n":
                state = START

        elif state == COMMENT_ML:
            if c == "*" and i + 1 < len(text) and text[i+1] == "/":
                state = START
                i += 2
                continue

        i += 1

    # -------- FINAL CLEANUP --------
    if state == IDENTIFIER:
        if invalid_identifier:
            items.append(("NAME", lexeme, "Identificador inválido: no puede iniciar con dígito"))
        else:
            items.append((classify_identifier(lexeme), lexeme, ""))

    elif state in (STRING_DQ, STRING_SQ, STRING_BT):
        items.append(("STRING", lexeme, "Cadena no terminada"))

    return items


# ---------- PRINT ----------
def print_table(rows):
    print(f"{'Token':<15}{'Valor':<25}{'Error'}")
    print("-" * 60)

    error_count = 0

    for t, v, e in rows:
        print(f"{t:<15}{v:<25}{e}")
        if e:  # count only rows with error message
            error_count += 1

    print("-" * 60)
    print(f"{error_count} error(es) encontrados")


# ---------- MAIN ----------
def main():
    with open("input.txt", "r") as f:
        text = f.read()

    rows = lexer(text)
    print_table(rows)


if __name__ == "__main__":
    main()