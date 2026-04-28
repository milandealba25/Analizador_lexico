# Codigo desarrollado por:
# - Milan De Alba
# - Yael Morales
# - Luis Daniel Garcia
# - Antoine Ganem
# - Luis Omar Olmedo

# Leer el archivo de entrada
with open("input.txt", "r") as f:
    lines = f.readlines()
f.close()


# for line in lines:
    # Every line detects \n so its used as end of line
    # print("\\n") if line.endswith("\n") else print(line.strip())


# Palabras reservadas
# KEYWORDS = ["if", "else", "while", "for", "function", "return", "var", "let", "const", "class", "import", "export", "default", "new",
# "this", "super", "extends", "try", "catch", "finally", "throw", "break", "continue", "switch", "case", "do", "in", "of"]

# Operadores
# OPERATORS = ["+", "-", "*", "/", "%", "=", "==", "===", "!=", "!==", "<", ">", "<=", ">=", "&&", "||", "!", "++", "--", "+=", "-=", "*=", "/=", "%="]

# Identificadores
# if IDENTIFIER.startswith(NUMBER): raise Error "no puede iniciar con un numero"
# if IDENTIFIER in KEYWORDS: raise Error "no puede ser una palabra reservada"
# if IDENTIFIER in OPERATORS: raise Error "no puede ser un operador"
# assure IDENTIFIER.startswith(LETTER) or IDENTIFIER.startswith("_") or IDENTIFIER.startswith("$"), raise Error "debe iniciar con letra, guion bajo o signo de dolar"
# assure IDENTIFIER.endswith(LETTER) or IDENTIFIER.endswith(NUMBER) or IDENTIFIER.endswith("_") or IDENTIFIER.endswith("$"), raise Error "debe terminar con letra, numero, guion bajo o signo de dolar"

# Simbolos
# Asegurar que las comillas, parentesis, corchetes y llaves esten balanceados (se cierren)