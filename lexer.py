# Codigo desarrollado por:
# - Milan De Alba
# - Yael Morales
# - Luis Daniel Garcia
# - Antoine Ganem
# - Luis Omar Olmedo

# ---------- STATES LABELS ----------
# Each constant represents a state in the DFA (finite automaton)
START = "START"
IDENTIFIER = "IDENTIFIER"
NUMBER = "NUMBER"
FLOAT = "FLOAT"
STRING_DQ = "STRING_DQ" # Double-quoted string: "string" 
STRING_SQ = "STRING_SQ" # Single-quoted string: 'string'
COMMENT_SL = "COMMENT_SL" # Single-line comment: // comment
COMMENT_ML = "COMMENT_ML" # Multi-line comment: /* comment */


# ---------- DEFINITIONS ----------
# Reserved words of the language
KEYWORDS = {
    "if", "else", "while", "for", "function", "return", "var", "let",
    "const", "class", "import", "export", "default", "new", "this",
    "super", "extends", "try", "catch", "finally", "throw", "break",
    "continue", "switch", "case", "do", "in", "of"
}

# Boolean literals (treated separately for semantic clarity)
BOOLEANS = {"true", "false"}

# All valid operators (1, 2, or 3 characters)
OPERATORS = {
    "+", "-", "*", "/", "%", "=", "==", "===", "!=", "!==",
    "<", ">", "<=", ">=", "&&", "||", "!", "++", "--",
    "+=", "-=", "*=", "/=", "%="
}

# Symbols that must be balanced
OPENING = {'(': ')', '{': '}', '[': ']'}
CLOSING = {')': '(', '}': '{', ']': '['}

# Set of characters that can start an operator (optimization)
OPERATOR_START = set(op[0] for op in OPERATORS)


# ---------- HELPERS ----------
# Classifies an identifier into keyword, boolean, or normal identifier
def classify_identifier(lexeme):
    if lexeme in BOOLEANS:
        return ("BOOLEAN", lexeme)
    if lexeme in KEYWORDS:
        return ("KEYWORD", lexeme)
    return ("IDENTIFIER", lexeme)


# Matches the longest possible operator (3 → 2 → 1 characters)
def match_operator(text, i):
    for length in (3, 2, 1):
        if i + length <= len(text):
            candidate = text[i:i+length]
            if candidate in OPERATORS:
                return candidate, length
    return None, 0


# ---------- LEXER ----------
def lexer(text):

    # Current state of the DFA
    state = START

    # Current sequence of characters being built into a token
    lexeme = ""

    # List of valid tokens found → (TYPE, VALUE)
    tokens = []

    # List of errors found → (ERROR_TYPE, VALUE)
    errors = []

    # Stack used to validate balanced symbols like (), {}, [], "", ''
    stack = []

    # Flag to detect invalid identifiers like 2bad
    invalid_identifier = False

    i = 0
    while i < len(text):
        c = text[i]  # current character

        # -------- START STATE --------
        # Decides what kind of token begins
        if state == START:

            if c.isalpha() or c == "_":
                state = IDENTIFIER
                lexeme += c

            elif c.isdigit():
                state = NUMBER
                lexeme += c

            elif c == '"':
                state = STRING_DQ
                stack.append('"')

            elif c == "'":
                state = STRING_SQ
                stack.append("'")

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
                tokens.append(("OPERATOR", "/"))

            # ---- SYMBOLS ----
            elif c in OPENING:
                stack.append(c)
                tokens.append(("SYMBOL", c))

            elif c in CLOSING:
                if not stack or stack[-1] != CLOSING[c]:
                    errors.append(("SYMBOL_ERROR", c))
                else:
                    stack.pop()
                tokens.append(("SYMBOL", c))

            # ---- OPERATORS ----
            elif c in OPERATOR_START:
                temp = ""

                # collect consecutive operator characters
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
                        tokens.append(("OPERATOR", op))
                        j += length
                else:
                    errors.append(("OPERATOR_ERROR", temp))

                continue

            elif c.isspace():
                pass  # ignore whitespace

            else:
                errors.append(("CHAR_ERROR", c))

        # -------- IDENTIFIER STATE --------
        elif state == IDENTIFIER:
            if c.isalnum() or c == "_":
                lexeme += c
            else:
                if invalid_identifier:
                    errors.append(("IDENTIFIER_ERROR", lexeme))
                else:
                    tokens.append(classify_identifier(lexeme))

                lexeme = ""
                state = START
                invalid_identifier = False
                continue

        # -------- NUMBER STATE --------
        elif state == NUMBER:
            if c.isdigit():
                lexeme += c

            elif c.isalpha() or c == "_":
                lexeme += c
                invalid_identifier = True
                state = IDENTIFIER

            elif c == ".":
                state = FLOAT
                lexeme += c

            else:
                tokens.append(("INT", lexeme))
                lexeme = ""
                state = START
                continue

        # -------- FLOAT STATE --------
        elif state == FLOAT:
            if c.isdigit():
                lexeme += c
            else:
                if lexeme.endswith("."):
                    errors.append(("FLOAT_ERROR", lexeme))
                else:
                    tokens.append(("FLOAT", lexeme))
                lexeme = ""
                state = START
                continue

        # -------- STRING "..." --------
        elif state == STRING_DQ:
            if c == '"':
                if stack:
                    stack.pop()
                tokens.append(("STRING", lexeme))
                lexeme = ""
                state = START

            elif c == "\n":
                # error recovery: stop string and continue parsing
                errors.append(("STRING_ERROR", lexeme))
                lexeme = ""
                state = START
                if stack and stack[-1] == '"':
                    stack.pop()

            else:
                lexeme += c

        # -------- STRING '...' --------
        elif state == STRING_SQ:
            if c == "'":
                if stack:
                    stack.pop()
                tokens.append(("STRING", lexeme))
                lexeme = ""
                state = START

            elif c == "\n":
                errors.append(("STRING_ERROR", lexeme))
                lexeme = ""
                state = START
                if stack and stack[-1] == "'":
                    stack.pop()

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

    # -------- END CLEANUP --------
    # Handle unfinished tokens at end of file
    if state == IDENTIFIER:
        if invalid_identifier:
            errors.append(("IDENTIFIER_ERROR", lexeme))
        else:
            tokens.append(classify_identifier(lexeme))

    elif state == NUMBER:
        tokens.append(("INT", lexeme))

    elif state == FLOAT:
        if lexeme.endswith("."):
            errors.append(("FLOAT_ERROR", lexeme))
        else:
            tokens.append(("FLOAT", lexeme))

    elif state in (STRING_DQ, STRING_SQ):
        errors.append(("STRING_ERROR", lexeme))

    elif state == COMMENT_ML:
        errors.append(("COMMENT_ERROR", "unclosed comment"))

    # Any remaining symbols in stack are unbalanced
    while stack:
        errors.append(("SYMBOL_ERROR", stack.pop()))

    return tokens, errors


# ---------- TABLE FORMAT ----------
def format_table(tokens, errors):
    rows = []

    # Convert tokens into table rows
    for ttype, value in tokens:

        if ttype == "IDENTIFIER":
            rows.append(("NAME", value, ""))

        elif ttype == "KEYWORD":
            rows.append(("KEYWORD", value, ""))

        elif ttype == "BOOLEAN":
            rows.append(("BOOLEAN", value, ""))

        elif ttype in ("INT", "FLOAT"):
            rows.append(("NUMBER", value, ""))

        elif ttype == "STRING":
            rows.append(("STRING", value, ""))

        elif ttype == "OPERATOR":
            rows.append(("OPERATOR", value, ""))

        elif ttype == "SYMBOL":
            rows.append(("SYMBOL", value, ""))

    # Convert errors into table rows
    for err_type, value in errors:

        if err_type == "IDENTIFIER_ERROR":
            rows.append(("NAME", value, "Identificador inválido: no puede iniciar con dígito"))

        elif err_type == "STRING_ERROR":
            rows.append(("STRING", value, "Cadena no terminada"))

        elif err_type == "FLOAT_ERROR":
            rows.append(("NUMBER", value, "Número flotante inválido"))

        elif err_type == "CHAR_ERROR":
            rows.append(("(desconocido)", value, "Carácter inválido/no reconocido"))

        elif err_type == "SYMBOL_ERROR":
            rows.append(("SYMBOL", value, "Símbolo no balanceado"))

        elif err_type == "COMMENT_ERROR":
            rows.append(("COMMENT", value, "Comentario no terminado"))

        elif err_type == "OPERATOR_ERROR":
            rows.append(("OPERATOR", value, "Operador inválido"))

    return rows


# ---------- PRINT ----------
def print_table(rows):
    print(f"{'Token':<15}{'Valor':<25}{'Error'}")
    print("-" * 60)

    for t, v, e in rows:
        print(f"{t:<15}{v:<25}{e}")


# ---------- MAIN ----------
def main():
    # Read input file
    with open("input.txt", "r") as f:
        text = f.read()

    # Run lexer
    tokens, errors = lexer(text)

    # Format and print results
    rows = format_table(tokens, errors)
    print_table(rows)


if __name__ == "__main__":
    main()