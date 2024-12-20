import sys

class Lexer:
    keywords = ['draw', 'write', 'grid']
    operators = '+/*'
    specialSymbols = '(),;'
    
    def __init__(self, source_code):
        self.source_code = source_code
        self.position = 0  
        self.length = len(source_code) 

    # Return the next char & move position forward
    def get_next_char(self):
        if self.position < self.length:
            char = self.source_code[self.position]
            self.position += 1
            return char
        return None

    # Peek at the next char
    def peek_next_char(self):
        if self.position < self.length:
            return self.source_code[self.position]
        return None

    # Tokenize source code
    def tokenize(self):
        tokens = []  # List to store tokens
        state = 'S0'  # Initial state
        buffer = ''  # Buffer to store characters for multi-character tokens
        min_kw_len = min(len(kw) for kw in self.keywords) #to know when to check for kws
        max_kw_len = max(len(kw) for kw in self.keywords) #to know when to make transition from S1 to S5
        skip = False # Helps with position tracking
        
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
                elif char in self.operators:
                    state = 'S3' # to correspond to state descriptions
                    tokens.append(("Operator", char))
                    state = 'S0'
                elif char in self.specialSymbols:
                    state = 'S4' # to correspond to state descriptions
                    tokens.append(("Special Symbol", char))
                    state = 'S0'
                elif not char.isspace():
                    # If the character is not whitespace and not recognized, emit an error
                    print(f"Error: Unexpected character '{char}' at position {self.position} not parsed.", file=sys.stderr)
            elif state == 'S1':
                # State S1: Building a keyword or identifier
                if char is not None and char.isalpha():
                    buffer += char
                    if len(buffer) > max_kw_len: #if can't be a keyword due to length, go to S5 to build identifier
                        state = 'S5'
                    elif len(buffer)>=min_kw_len: #check if buffer is long enough to determine if keyword
                        # Check if the buffer matches a keyword
                        if buffer in self.keywords:
                            state = 'S6' #transition to keyword accept state
                else:
                    self.position -= 1
                    skip = True
                    state = 'S5' #transition to identifier state
            elif state == 'S6':
                # State S6: Keyword accept state.
                tokens.append(("Keyword", buffer))
                buffer = ''
                state = 'S0'
                if char is not None:
                    self.position -= 1
            elif state == 'S5':
                # State S5: Identifier build & accept state.
                if char is not None and char.isalpha():
                    buffer += char
                else:
                    tokens.append(("Identifier", buffer))
                    buffer = ''
                    state = 'S0'
                    if char is not None and not skip:
                        self.position -= 1
                    if skip:
                        skip = not skip
            elif state == 'S2':
                # State S2: Building a number
                if char is not None and char.isdigit():
                    buffer += char #self-loop to S2
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
