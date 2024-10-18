import sys

# Class for the lexer that tokenizes the source code
class Lexer:
    #static variable initialization
    def keywords = ['draw', 'write', 'grid']
    def operators = '+/*'
    def specialSymbols = '(),;'
    
    # Initialize the lexer with the source code
    def __init__(self, source_code):
        self.source_code = source_code
        self.position = 0  # Current position in the source code
        self.length = len(source_code)  # Length of the source code

    # Return the next character in the source code, and move the position forward
    def get_next_char(self):
        if self.position < self.length:
            char = self.source_code[self.position]
            self.position += 1
            return char
        return None

    # Peek at the next character without moving the position forward
    def peek_next_char(self):
        if self.position < self.length:
            return self.source_code[self.position]
        return None

    # Tokenize the source code into a list of tokens
    def tokenize(self):
        tokens = []  # List to store tokens
        state = 'S0'  # Initial state
        buffer = ''  # Buffer to store characters for multi-character tokens

        # Loop through the source code character by character
        while self.position <= self.length:
            char = self.get_next_char()
            if state == 'S0':
                # Initial state: Determine the type of character and transition to the appropriate state
                if char is None:
                    break
                elif char.isalpha():
                    # If the character is alphabetic, start building a keyword or identifier
                    buffer += char
                    state = 'S1'
                elif char.isdigit():
                    # If the character is a digit, start building a number
                    buffer += char
                    state = 'S2'
                elif char in operators:
                    # If the character is an operator, emit an operator token
                    tokens.append(("Operator", char))
                elif char in specialSymbols:
                    # If the character is a special symbol, emit a special symbol token
                    tokens.append(("Special Symbol", char))
                elif not char.isspace():
                    # If the character is not whitespace and not recognized, emit an error
                    print(f"Error: Unexpected character '{char}' at position {self.position}", file=sys.stderr)
            elif state == 'S1':
                # State S1: Building a keyword or identifier
                if char is not None and char.isalpha():
                    buffer += char
                else:
                    # Check if the buffer matches a keyword, otherwise it's an identifier
                    if buffer in keywords:
                        tokens.append(("Keyword", buffer))
                    else:
                        tokens.append(("Identifier", buffer))
                    buffer = ''
                    state = 'S0'
                    if char is not None:
                        self.position -= 1
            elif state == 'S2':
                # State S2: Building a number
                if char is not None and char.isdigit():
                    buffer += char
                else:
                    tokens.append(("Number", buffer))
                    buffer = ''
                    state = 'S0'
                    if char is not None:
                        self.position -= 1
        return tokens

# Main function to run the lexer
if __name__ == "__main__":
    # Check if an input file or input code is provided
    if len(sys.argv) == 2:
        input_file = sys.argv[1]
        try:
            # Read the source code from the input file
            with open(input_file, "r") as f:
                source_code = f.read()
        except FileNotFoundError:
            print(f"Error: File '{input_file}' not found.", file = sys.stderr)
            sys.exit(1)
    elif len(sys.argv) == 3 and sys.argv[1] == '--input':
        # Read the source code from the command line input
        source_code = sys.argv[2]
    else:
        print("Usage: python3 lexer.py <input_file> or python3 lexer.py --input '<input_code>'")
        sys.exit(1)

    # Create a Lexer object and tokenize the source code
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    # Print the tokens
    for token in tokens:
        print(f"<{token[0]}, {token[1]}>")
