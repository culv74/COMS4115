class ASTNode:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

    def __repr__(self):
        return f"ASTNode({self.type}, {self.value})"

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current_token(self):
        return self.tokens[self.position] if self.position < len(self.tokens) else None
    
    def eat(self, token_type):
        """Consumes the current token if it matches the expected type."""
        if self.current_token() and self.current_token()[0] == token_type:
            self.position += 1
        else:
            raise SyntaxError(f"Expected {token_type}, found {self.current_token()}")

    def parse_program(self):
        root = ASTNode("Program")
        while self.position < len(self.tokens):
            statement = self.parse_statement()
            root.add_child(statement)
        return root

    def parse_statement(self):
        current = self.current_token()
        if current and current[0] == 'Keyword':
            keyword = current[1]
            if keyword == 'draw':
                return self.parse_draw_statement()
            elif keyword == 'write':
                return self.parse_write_statement()
            elif keyword == 'grid':
                return self.parse_grid_statement()
            else:
                raise SyntaxError(f"Unknown statement {keyword}")
        else:
            raise SyntaxError(f"Unexpected token {current}")

    def parse_draw_statement(self):
        self.eat('Keyword')  # eat 'draw'
        self.eat('Special Symbol')  # eat '('
        expression = self.parse_expression()
        self.eat('Special Symbol')  # eat ')'
        node = ASTNode('DrawStatement')
        node.add_child(expression)
        return node

    def parse_write_statement(self):
        self.eat('Keyword')  # eat 'write'
        self.eat('Special Symbol')  # eat '('
        expression = self.parse_expression()
        self.eat('Special Symbol')  # eat ')'
        node = ASTNode('WriteStatement')
        node.add_child(expression)
        return node

    def parse_grid_statement(self):
        """Parse a 'grid' statement."""
        self.eat('Keyword')  # eat 'grid'
        self.eat('Special Symbol')  # eat '('
        rows = self.parse_number()
        self.eat('Special Symbol')  # eat ','
        cols = self.parse_number()
        self.eat('Special Symbol')  # eat ','

        # Now parse the grid content (it can contain draw, write, etc.)
        grid_content = self.parse_grid_content()

        self.eat('Special Symbol')  # eat ')'
        node = ASTNode('GridStatement', value=(rows, cols))
        node.add_child(grid_content)
        return node

    def parse_grid_content(self):
        """Parse content inside the grid, which could be multiple expressions (draw, write, etc.)."""
        content_node = ASTNode('GridContent')
        while self.position < len(self.tokens):
            current = self.current_token()

            # If we encounter a keyword (draw/write), we parse the expression
            if current and current[0] in ['Keyword', 'Identifier']:
                content_node.add_child(self.parse_expression())

                # Check if the next token is a comma, indicating multiple items in the grid
                if self.position < len(self.tokens) and self.current_token()[0] == 'Special Symbol' and self.current_token()[1] == ',':
                    self.eat('Special Symbol')  # Eat the comma
                else:
                    break  # No more commas or invalid token, stop parsing
            elif current and current[0] == 'Special Symbol' and current[1] == ')':
                break  # We found the closing parenthesis, stop parsing grid content
            else:
                break  # Stop if any unexpected token is found

        return content_node

    def parse_expression(self):
        """Parse an expression, which could be an image or an operator."""
        left = self.parse_image()
        while self.current_token() and self.current_token()[0] == 'Operator':
            operator = self.current_token()[1]
            self.eat('Operator')
            right = self.parse_image()
            operator_node = ASTNode('Expression', value=operator)
            operator_node.add_child(left)
            operator_node.add_child(right)
            left = operator_node  # Update left to the new operator node
        return left

    def parse_image(self):
        """Parse an image (either 'draw' or 'write' with an identifier)."""
        current = self.current_token()
        if current[0] == 'Keyword' and current[1] in ['draw', 'write']:
            keyword = current[1]
            self.eat('Keyword')
            self.eat('Special Symbol')  # eat '('
            identifier = self.parse_identifier()
            self.eat('Special Symbol')  # eat ')'
            return ASTNode(keyword.capitalize() + 'Image', value=identifier)
        elif current[0] == 'Identifier':
            identifier = self.current_token()[1]
            self.eat('Identifier')
            return ASTNode('Identifier', value=identifier)
        else:
            raise SyntaxError(f"Unexpected token in image: {current}")

    def parse_identifier(self):
        """Parse an identifier (like dog, cat, etc.)."""
        identifier = self.current_token()[1]
        self.eat('Identifier')
        return identifier

    def parse_number(self):
        """Parse a number."""
        number = self.current_token()[1]
        self.eat('Number')
        return number
