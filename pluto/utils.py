import ast
import re

def extract_list(input_string):
    # Find the start of the list
    start = input_string.find('[')
    if start == -1:
        print("No Python list found in the input string.")
        return None

    # Count the brackets to find the end of the list
    count = 0
    for i, char in enumerate(input_string[start:]):
        if char == '[':
            count += 1
        elif char == ']':
            count -= 1
        if count == 0:
            end = i + start + 1
            break
                # Extract the list
    found_list_str = input_string[start:end]
    found_list = ast.literal_eval(found_list_str)

    return found_list


def replace_linebreaks(input_string):
    return input_string.replace("\n", "\\n")


def remove_linebreaks_and_spaces(input_string):
    # Remove line breaks
    no_linebreaks = re.sub(r'\s+', ' ', input_string)

    # Remove extra spaces
    no_spaces = ' '.join(no_linebreaks.split())

    return no_spaces


