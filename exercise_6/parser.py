class ParserException(Exception):
    pass

def find_open_parenthesis(text):
    for index, character in enumerate(text):
        if character == '(':
            return text[index + 1:]
    raise ParserException("Unable to find opening parenthesis")

def get_argument(text):
    start_index = None
    for index, character in enumerate(text):
        if character == '(':
            arg, remaining_text = perform_operation(text[index + 1:])
            return arg, remaining_text
        elif character != ' ' and start_index is None:
            start_index = index
        elif (character == ' ' or character == ')') and start_index is not None:
            try:
                arg = int(text[start_index:index])
            except ValueError:
                raise ParserException(f"Invalid character found: '{text[start_index:index]}'")
            remaining_text = text[index:]
            return arg, remaining_text
    raise ParserException("Unable to get argument")

def perform_operation(text):
    if text[0] == '+':
        arg1, remaining_text = get_argument(text[1:])
        if remaining_text and remaining_text[0] != ')':
            arg2, remaining_text = get_argument(remaining_text)
            remaining_text = remaining_text[1:] if remaining_text and remaining_text[0] == ')' else remaining_text
            return arg1 + arg2, remaining_text
        else:
            
            return arg1, remaining_text[1:] if remaining_text and remaining_text[0] == ')' else remaining_text
    else:
        raise ParserException("Invalid operation")



result, _ = perform_operation(find_open_parenthesis("(+ (+ 1 2) (+ (+ 3) 5))"))
print("Result:", result)
