
# Triton Lexical Analyzer

**Developed by:**
- **Milan De Alba**
- **Yael Morales**
- **Luis Daniel Garcia**
- **Antoine Ganem**
- **Luis Omar Olmedo**

This lexical analyzer is designed mainly for Triton (essentially Python).

Lexer.py is a program that reads Triton code and divides it into tokens. Tokens have an ID and belong to categories,
this way interpretation (contextualization) of Triton code is possible rather than just characters.

The code it analyzes is located at ./tests/input.txt


## Functionality

The lexer scans code in the following order:

1. NEWLINE
2. WHITESPACE / TAB
3. COMMENTS
4. LETTER / UNDERSCORE
    1. BOOLEAN
    2. KEYWORDS
    3. DATA TYPES
    4. IDENTIFIERS
5. NUMBERS
6. STRINGS
7. OPERATORS
8. DELIMITERS
9. UNKNOWN (ERROR)


## Rules
* NEWLINES
    - Must be exactly chars '\n'

* WHITESPACE / TAB
    - Ignored unless part of a string (detected by ' ' or '\t')

* COMMENTS
    - Starting with # gets ignored until NEWLINE

* LETTER / UNDERSCORE
    * BOOLEAN or KEYWORDS
        - KEYWORDS are reserved words (if, for, return, etc.)
        - BOOLEAN are also keywords, but for better display they get detected by either of 'True' or 'False'

    * DATA TYPES
        - Not reserved words as KEYWORDS, but built-in names that shouldn't be used as IDENTIFIERS
        - Defined by a set (int, float, str, bool, list, set, etc.)

    * IDENTIFIERS
        - User-defined names
        - Must start with a letter or underscore
        - Can include letters, underscores or numbers

* NUMBERS
    - Can be int or float (complex not supported)
    - Int must only include digits, Float contains only 1 dot (1.2.3 is invalid)
    - Invalid if mixed with letters

* STRINGS
    - Must be enclosed in quotes ('single', "double" or backtick``)
    - Must be balanced (closing matching opening) otherwise error is raised

* OPERATORS
    - Must be placed between operands, otherwise raise misplaced error
        + x = 1, where = between x and 1 is valid
        + despite operations like x++1 being 'allowed' they are not common in Triton, so will raise an error (as a warning)
    - Include multiple categories, all marked as OPERATORS:
        + Arithmetic                        [+, -, *, /, //, %, **]
        + Comparison                        [<, >, <=, >=, ==, !=]
        + Assignment                        [=, +=, -=, *=, /=]
        + Logical (defined in keywords):    [and, or, not]


* DELIMITERS
    - Opening symbols must match a closing symbol; otherwise marked as “unbalanced”
    - Includes the following categories:
        + Grouping symbols:     (), [], {}
        + Separators:           , :
        + Others:               ., @, ->, ~, &, |, ^, <<, >>

* UNKNOWN (ERROR)
    - Any symbol not recognized is marked as an error
