# ------------------------------------------------------------
# Analizador léxico para Triton
# Codigo desarrollado por:
# - Milan De Alba
# - Yael Morales
# - Luis Daniel Garcia
# - Antoine Ganem
# - Luis Omar Olmedo
# ------------------------------------------------------------

# ---------------- TOKEN IDS ----------------
TOK = {
    # KEYWORDS (0–17)
    "def": 0, "return": 1, "if": 2, "else": 3, "elif": 4, "for": 5, "while": 6, "in": 7, "is": 8, "and": 9,
    "or": 10, "not": 11, "True": 12, "False": 13, "None": 14, "pass": 15, "break": 16, "continue": 17,

    # OPERATORS (18–35)
    "+": 18, "-": 19, "*": 20, "/": 21, "//": 22, "%": 23, "**": 24, "<": 25, ">": 26, "<=": 27, ">=": 28,
    "==": 29, "!=": 30, "=": 31, "+=": 32, "-=": 33, "*=": 34, "/=": 35,

    # DELIMITERS (36–52)
    "(": 36, ")": 37, "[": 38, "]": 39, "{": 40, "}": 41, ",": 42, ":": 43, ".": 44, "@": 45, "->": 46,
    "~": 47, "&": 48, "|": 49, "^": 50, "<<": 51, ">>": 52,

    # GENERIC
    "NAME": 53, "NUMBER": 54, "STRING": 55, "NEWLINE": 56, "ERROR": 99
}

# ---------------- CATEGORIES ----------------
KEYWORDS = set(list(TOK.keys())[:18])
OPERATORS = set(list(TOK.keys())[18:36])
DELIMITERS = set(list(TOK.keys())[36:53])
BOOLEAN = {"True", "False"} # Display as boolean, treat as keyword


DATA_TYPES = {"int", "float", "str", "list", "tuple", "range", "dict", "set", "bool", "bytes", "bytearray", "frozenset"}

OPENING = {"(", "[", "{"}
CLOSING = {")": "(", "]": "[", "}": "{"}

ASSIGNMENT_OPS = {"=", "+=", "-=", "*=", "/="}

# ---------------- STORAGE ----------------
tokens = []
line = 1

# ---------------- HELPERS ----------------
def add_token(tid, ttype, lex, err=""):
    tokens.append((tid, ttype, lex, err))

def add_error(lex, msg):
    global error_count
    add_token(TOK["ERROR"], "ERROR", lex, msg)
    error_count += 1

def is_id(c):
    return c.isalpha() or c == "_"

# ---------------- LEXER ----------------
def lexer(text):
    global line, error_count
    i = 0
    prev_type = None
    stack = []
    error_count = 0

    while i < len(text):
        c = text[i]

        # NEWLINE
        if c == "\n":
            add_token(TOK["NEWLINE"], "NEWLINE", "\\n")
            line += 1
            prev_type = None
            i += 1
            continue

        # WHITESPACE
        if c in " \t":
            i += 1
            continue

        # COMMENT
        if c == "#":
            while i < len(text) and text[i] != "\n":
                i += 1
            continue

        # IDENTIFIER / KEYWORD / BOOLEAN / TYPE
        if is_id(c):
            start = i
            while i < len(text) and (is_id(text[i]) or text[i].isdigit()):
                i += 1
            lex = text[start:i]

            if lex in KEYWORDS:
                ttype = "BOOLEAN" if lex in BOOLEAN else "KEYWORD"
                add_token(TOK[lex], ttype, lex)
            elif lex in DATA_TYPES:
                ttype = "TYPE"
                add_token(TOK["NAME"], ttype, lex)
            else:
                ttype = "NAME"
                add_token(TOK["NAME"], ttype, lex)

            if prev_type == "OPERAND" and ttype == "NAME":
                add_error(lex, "Nombres consecutivos")

            prev_type = None if ttype in ["TYPE", "BOOLEAN", "KEYWORD"] else "OPERAND"
            continue

        # NUMBER
        if c.isdigit():
            start = i
            dots = 0
            invalid = False

            while i < len(text) and (text[i].isdigit() or text[i] == "." or is_id(text[i])):
                if text[i] == ".":
                    dots += 1
                if is_id(text[i]):
                    invalid = True
                i += 1

            lex = text[start:i]

            if invalid or dots > 1:
                add_error(lex, "Numero invalido")
                prev_type = None
            else:
                add_token(TOK["NUMBER"], "NUMBER", lex)
                if prev_type == "OPERAND":
                    add_error(lex, "Operandos consecutivos")
                prev_type = "OPERAND"

            continue

        # STRING
        if c in ['"', "'", "`"]:
            quote = c
            i += 1
            start = i

            while i < len(text) and text[i] != quote and text[i] != "\n":
                i += 1

            if i < len(text) and text[i] == quote:
                lex = text[start:i]
                add_token(TOK["STRING"], "STRING", lex)
                i += 1
                prev_type = "OPERAND"
            else:
                lex = text[start:i]
                add_error(lex, "Cadena no terminada")
                prev_type = None

            continue

        # OPERATORS
        three = text[i:i+3]
        two = text[i:i+2]

        op = None
        if three in OPERATORS:
            op = three; i += 3
        elif two in OPERATORS:
            op = two; i += 2
        elif c in OPERATORS:
            op = c; i += 1

        if op:
            if op in ASSIGNMENT_OPS:
                add_token(TOK[op], "OPERATOR", op)
                prev_type = None
            elif prev_type != "OPERAND":
                add_error(op, "Operador mal posicionado")
                prev_type = None
            else:
                add_token(TOK[op], "OPERATOR", op)
                prev_type = "OPERATOR"
            continue

        # DELIMITERS
        if c in DELIMITERS:
            if c in OPENING:
                stack.append(c)
            elif c in CLOSING:
                if not stack or stack[-1] != CLOSING[c]:
                    add_error(c, "Simbolo no balanceado")
                else:
                    stack.pop()

            add_token(TOK[c], "SYMBOL", c)
            prev_type = None
            i += 1
            continue

        # UNKNOWN
        add_error(c, "Caracter invalido")
        prev_type = None
        i += 1

    # FINAL CHECKS
    if prev_type == "OPERATOR":
        add_error("", "Expresion termina en operador")

    while stack:
        add_error(stack.pop(), "Simbolo no cerrado")

    return error_count


# ---------------- PRINT ----------------
def print_table(error_count):
    print("\nRESULTADO DEL ANALISIS LEXICO")
    print("-" * 75)
    print(f"{'ID':<5}{'TOKEN':<15}{'LEXEME':<25}{'ERROR'}")
    print("-" * 75)

    for t in tokens:
        print(f"{t[0]:<5}{t[1]:<15}{t[2]:<25}{t[3]}")

    print("-" * 75)
    print(f"{error_count} error(es) encontrados\n")


# ---------------- MAIN ----------------
def main():
    with open("tests\\input.txt", "r") as f:
        text = f.read()

    errors = lexer(text)
    print_table(errors)


if __name__ == "__main__":
    main()