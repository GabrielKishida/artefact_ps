brackets = "(((()(()())))()"


def is_brackets_syntax_correct(string):
    """Function that verifies if a string of brackets has a correct or incorrect syntax.

    Args:
        A string containing brackets only.
    Returns:
        boolean: True if the syntax is correct and False if it is incorrect.
    """
    # This is a stack containing all unclosed brackets.
    bracket_stack = []
    for character in string:
        # If an opening bracket is met, then it is stacked.
        if character == "(":
            bracket_stack.append(character)
        # If a closing bracket is met, then an element of the stack must be popped.
        # If no other elements exist, then the syntax is wrong since there is a closing bracket
        # without its opening counterpart.
        elif character == ")":
            if bracket_stack:
                bracket_stack.pop()
            else:
                return False
    # If the bracket stack is not completely empty after looking at all characters, then an
    # opening bracket does not have a closing counterpart, which means the syntax is wrong.
    if bracket_stack:
        return False
    return True


# Verify a given case.
print(is_brackets_syntax_correct(brackets))
