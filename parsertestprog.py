# Import necessary classes from lexer.py and parser.py
from lexer import Lexer
from parser import Parser

# Sample source code to test the lexer and parser
source_code = """
draw(sun + dog);
grid(2, 2, draw(sun), write(dog), write(tree), draw(cat));
(3 * draw(dog)) / write(I like dogs);
"""

# Step 1: Tokenize the source code using the Lexer
lexer = Lexer(source_code)  # Initialize lexer with the source code
tokens = lexer.tokenize()  # Tokenize the source code

# Step 2: Print out the tokens generated by the lexer (optional step for debugging)
print("Tokens Generated by Lexer:")
for token in tokens:
    print(f"<{token[0]}, {token[1]}>")

# Step 3: Parse the tokens using the Parser to generate an AST
parser = Parser(tokens)  # Initialize parser with the tokenized input
ast = parser.parse()  # Generate AST from the tokens

# Step 4: Print the generated AST (ensure __str__ or __repr__ methods are implemented in AST)
print("\nGenerated AST:")
print(ast)

# Step 5: Optional: Check for a specific AST structure for validation
# Example of a structure check for a DrawStatement with an AdditionExpression
if isinstance(ast, DrawStatement) and isinstance(ast.expression, AdditionExpression):
    print("\nTest Passed: Draw Statement with Addition Expression found!")
else:
    print("\nTest Failed: Unexpected AST structure.")