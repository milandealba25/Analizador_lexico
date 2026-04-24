# Verify input will be file

import re

# Define regular expressions for pattern matching
pattern_user_functions = re.compile(r'def\s+([a-zA-Z_]\w*)\s*\(')
pattern_built_in_functions = re.compile(r'\b(print|input|return|len|range|sum|open|globals|next|eval|round)\b')
pattern_loops = re.compile(r'\b(for|while)\b')
pattern_conditions = re.compile(r'\b(if|elif|else)\b')
pattern_grouping_symbols = re.compile(r'[()\[\]{}]')
pattern_comments = re.compile(r'#.*?$')  # Match comments starting with '#'

# Read the input file
input_file_path = "input.txt"
output_file_path = "output.html"

try:
    with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
        # Write the HTML header
        output_file.write(
            "<html><head><title>Highlighted Code</title>"
            "\n<style>"
            "body { background-color: gray; }"
            "\n.comment { color: blue; }"
            "\n.def { color: yellow }"
            "\n.user-functions { color: orange; }"
            "\n.built-in-functions { color: purple; }"
            "\n.loops { color: green; }"
            "\n.conditions { color: red; }"
            "\n.grouping-symbols { color: brown; }"
            "\n</style>"
            "\n</head><body><pre>\n"
        )

        for line in input_file:

            # Check if the line contains a comment
            if '#' in line:
                # If so, split the line by '#' and consider the part before the comment for highlighting
                line_before_comment = line.split('#')[0]
                line_after_comment = line[len(line_before_comment):]

                # Highlight the part before the comment
                line_before_comment = pattern_user_functions.sub(r'<b>def \1</b>(', line_before_comment)
                line_before_comment = pattern_built_in_functions.sub(r'<b>\1</b>', line_before_comment)
                line_before_comment = pattern_loops.sub(r'<b>\1</b>', line_before_comment)
                line_before_comment = pattern_conditions.sub(r'<b>\1</b>', line_before_comment)
                line_before_comment = pattern_grouping_symbols.sub(r'<b>\g<0></b>', line_before_comment)

                # Write the modified line to the output HTML file
                output_file.write(line_before_comment)

                # Write the comment part with blue color directly
                output_file.write(pattern_comments.sub(r'<span class="comment">\g<0></span>', line_after_comment))
            else:
                # If there's no comment in the line, process it for highlighting

                # Highlight keyword "def" with yellow and function name with orange
                line = pattern_user_functions.sub(r'<span class="def">def </span>'
                                                  r'<span class="user-functions">\g<1>(</span>', line)

                # Highlight built-in functions with purple
                line = pattern_built_in_functions.sub(r'<span class="built-in-functions">\g<1></span>', line)

                # Highlight loops with green
                line = pattern_loops.sub(r'<span class="loops">\g<1></span>', line)

                # Highlight conditions with red color
                line = pattern_conditions.sub(r'<span class="conditions">\g<1></span>', line)

                # Check for grouping symbols and highlight with brown color
                line = pattern_grouping_symbols.sub(r'<span class="grouping-symbols">\g<0></span>', line)

                # Write the modified line to the output HTML file
                output_file.write(line)

        # Write the HTML footer
        output_file.write("</pre></body></html>")

    print("Output file 'output.html' created successfully.")

except FileNotFoundError:
    print("File not found. Please provide valid file paths.")
except Exception as e:
    print("An error occurred:", e)


