syntax_input = "({a"

opening_brackets = ["(", "{", "["]
closing_brackets = [")", "}", "]"]

closing_brackets_dict = {
    "(": ")",
    "{": "}",
    "[": "]",
}

opening_brackets_dict = {
    ")": "(",
    "}": "{",
    "]": "[",
}


def backtrack_missing_open_bracket(error_index, stack, bracket_to_insert, string):
    """Function that backtracks the syntax from a given index where an error of a missing
    opening bracket occurred (closed bracket was found with no open bracket in the stack).
    It analyzes each point that it can insert a bracket to fix it and returns a list of
    possible correct syntaxes.

    Args:
        error_index (int): index where the syntax error was found
        stack (list of chars): contains the stack of syntax analysis when the error was found
        bracket_to_insert (char): contains the character to be inserted to fix the error
        string (string): contains the original syntax to be fixed.
    Returns:
        possible_syntaxes (list of strings): A list of correct syntax corrections derived from
        the original string.
    """
    # List of possible syntaxes to be filled and returned.
    possible_syntaxes = []
    backtrack_stack = stack.copy()
    # The first possible syntax is to add the correction right where the error was detected
    possible_syntax = string[:error_index] + bracket_to_insert + string[error_index:]
    possible_syntaxes.append(possible_syntax)

    # Backtracking Loop
    for i in reversed(range(error_index)):
        character = string[i]
        # Reverse logic from the analysis: if it is a opening bracket, it must pop.
        if character in opening_brackets:
            if backtrack_stack:
                backtrack_stack.pop()
            else:
                break
        # Reverse logic: if there is a closing bracket, it must append its opening counterpart.
        elif character in closing_brackets:
            backtrack_stack.append(opening_brackets_dict[character])
        # If the stack is smaller than when it was when the error was encountered, no further
        # positions to fix the error exist.
        if len(backtrack_stack) < len(stack):
            break
        # If the stack is exactly the same size it was when the error was encountered, this is
        # a correct position to fix the error.
        elif len(backtrack_stack) == len(stack):
            possible_syntax = string[:i] + bracket_to_insert + string[i:]
            possible_syntaxes.append(possible_syntax)
    return possible_syntaxes


def get_possible_closing_placements(lone_i, string):
    """Function that, given the index of where a lone open bracket exists on the string,
    gives the possible placements to fix the lone open bracket.

    Args:
        lone_i (integer): The index of the lone open bracket on the string.
        string (string): The syntax to be fixed.
    Returns:
        possible_syntaxes (list of strings): A list of syntax corrections derived from
        the original string.
    """
    # An empty stack to analyze where the placements are valid.
    stack = []
    # List with all the possible syntaxes to correct the given error.
    possible_syntaxes = []
    # Obtaining the correct bracket to insert to fix the error.
    character_to_insert = closing_brackets_dict[string[lone_i]]
    # Looping the string after the lone open bracket. The last extra iteration allows the placement
    # of a closing bracket at the end of the string (after all characters) if possible.
    for i in range(lone_i + 1, len(string) + 1):
        # If the stack is empty, then the placement is valid since there are no other open brackets
        # in between the lone open bracket and current placement.
        if not stack:
            possible_syntax = string[:i] + character_to_insert + string[i:]
            possible_syntaxes.append(possible_syntax)
        if i < len(string):
            character = string[i]
            # Just like the regular analysis, the stack should be popped. Validity of what
            # character it is and what has been popped is unnecessary since the string has
            # already been checked.
            if character in closing_brackets:
                if stack:
                    stack.pop()
                else:
                    break
            # Just like the regular analysis, if an opening bracket appears, stack it.
            elif character in opening_brackets:
                stack.append(character)
    return possible_syntaxes


def fix_brackets_syntax(string):
    """Function that given a string, finds the first bracket syntax error it encounters and
    outputs every single possible fix for that error.

    Args:
        A string containing brackets and other characters.
    Returns:
        list of strings: A list of corrected syntax brackets (only contains itself if
        it is already correct)
    """
    # This is a stack containing all unclosed brackets.
    bracket_stack = []
    bracket_index_stack = []
    for index, character in enumerate(string):
        # If an opening bracket is met, then it is stacked.
        if character in opening_brackets:
            bracket_index_stack.append(index)
            bracket_stack.append(character)
        # If a closing bracket is met, then an element of the stack must be popped.
        # If no other elements exist, then the syntax is wrong since there is a closing bracket
        # without its opening counterpart.
        elif character in closing_brackets:
            if bracket_stack:
                popped_bracket = bracket_stack.pop()
                bracket_index_stack.pop()
                # If the popped bracket is different than its closing counterpart, the syntax is wrong.
                if character != closing_brackets_dict[popped_bracket]:
                    # Calling the backtracking function to find which points the opening counterpart can
                    # be added, and finding possible correct syntaxes.
                    return backtrack_missing_open_bracket(
                        index, bracket_stack, opening_brackets_dict[character], string
                    )

            else:
                # If the stack is empty when a closing bracket is found, then an opening counterpart must
                # be added. Calling the backtracking function to find where that can be added.
                return backtrack_missing_open_bracket(
                    index, bracket_stack, opening_brackets_dict[character], string
                )

    # If the bracket stack is not completely empty after looking at all characters, then an
    # opening bracket does not have a closing counterpart, which means the syntax is wrong.
    if bracket_stack:
        # For every remaining bracket in the stack, backtrack to find where its closing counterpart
        # can be added.
        possible_syntaxes = []
        if bracket_stack and bracket_index_stack:
            lone_bracket_index = bracket_index_stack.pop()
            possible_syntaxes += get_possible_closing_placements(
                lone_bracket_index, string
            )
        return possible_syntaxes
    return [string]


def fix_multiple_syntax_errors(string):
    """Function that given a string, finds all bracket syntax errors it encounters and
    outputs every single possible fix for all errors.

    Args:
        A string containing brackets and other characters.
    Returns:
        list of strings: A list of corrected syntax brackets (only contains itself if
        it is already correct)
    """
    # List of strings containing all possible syntaxes.
    possible_syntaxes = [string]
    keep_running = True
    # Since the function fix_brackets_syntax only corrects a single error at a time, multiple
    # iterations will be necessary.
    while keep_running:
        keep_running = False
        # List that will be filled with all corrected syntax for a given iteration.
        new_fixed_syntaxes = []
        for possible_syntax in possible_syntaxes:
            new_fixed_syntaxes += fix_brackets_syntax(possible_syntax)
        # If there are new fixed syntaxes, that means an error was encountered. If there are no
        # new fixed syntaxes, then no new error was encountered and no more iterations are needed.
        for new_fixed_syntax in new_fixed_syntaxes:
            if new_fixed_syntax not in possible_syntaxes:
                keep_running = True
        possible_syntaxes = new_fixed_syntaxes.copy()
    return possible_syntaxes


# Verify a given case.
print("Original syntax: ", syntax_input)
print("Possible fixes: ", fix_multiple_syntax_errors(syntax_input))
