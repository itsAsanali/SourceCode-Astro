import re
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Any

class TokenType(Enum):
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    LPAREN = auto()
    RPAREN = auto()
    COLON = auto()
    COMMA = auto()
    STRING = auto()
    NUMBER = auto()
    BOOLEAN = auto()
    JSX_TEXT = auto()
    EOF = auto()

@dataclass
class Token:
    type: TokenType
    value: Any
    line: int
    column: int

class AstroLexer:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = []

    def error(self, msg: str):
        raise SyntaxError(f"[Astro Lexer Error] {msg} at line {self.line}, column {self.column}")

    def tokenize(self) -> List[Token]:
        length = len(self.source)
        
        while self.pos < length:
            char = self.source[self.pos]

            if char in " \t\r\n":
                if char == "\n":
                    self.line += 1
                    self.column = 1
                else:
                    self.column += 1
                self.pos += 1
                continue

            if char == '{':
                self.tokens.append(Token(TokenType.LBRACE, '{', self.line, self.column))
                self.pos += 1; self.column += 1
            elif char == '}':
                self.tokens.append(Token(TokenType.RBRACE, '}', self.line, self.column))
                self.pos += 1; self.column += 1
            elif char == '[':
                self.tokens.append(Token(TokenType.LBRACKET, '[', self.line, self.column))
                self.pos += 1; self.column += 1
            elif char == ']':
                self.tokens.append(Token(TokenType.RBRACKET, ']', self.line, self.column))
                self.pos += 1; self.column += 1
            elif char == '(':
                self.tokens.append(Token(TokenType.LPAREN, '(', self.line, self.column))
                self.pos += 1; self.column += 1
                self._tokenize_jsx_mode()
            elif char == ':':
                self.tokens.append(Token(TokenType.COLON, ':', self.line, self.column))
                self.pos += 1; self.column += 1
            elif char == ',':
                self.tokens.append(Token(TokenType.COMMA, ',', self.line, self.column))
                self.pos += 1; self.column += 1
            elif char == '"':
                self._tokenize_string()
            elif char.isdigit() or (char == '-' and self.pos + 1 < length and self.source[self.pos+1].isdigit()):
                self._tokenize_number()
            elif char.isalpha() or char == '_':
                self._tokenize_identifier()
            else:
                self.error(f"Unexpected character: '{char}'")

        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens

    def _tokenize_string(self):
        start_col = self.column
        self.pos += 1
        start_pos = self.pos
        while self.pos < len(self.source) and self.source[self.pos] != '"':
            if self.source[self.pos] == '\\':
                self.pos += 1
            self.pos += 1
        
        if self.pos >= len(self.source):
            self.error("Unterminated string literal")

        val = self.source[start_pos:self.pos]
        self.pos += 1
        self.column += (self.pos - start_pos + 1)
        self.tokens.append(Token(TokenType.STRING, val, self.line, start_col))

    def _tokenize_number(self):
        match = re.match(r'-?\d+(\.\d+)?', self.source[self.pos:])
        if match:
            raw = match.group(0)
            val = float(raw) if '.' in raw else int(raw)
            self.tokens.append(Token(TokenType.NUMBER, val, self.line, self.column))
            self.pos += len(raw)
            self.column += len(raw)

    def _tokenize_identifier(self):
        match = re.match(r'[a-zA-Z_][a-zA-Z0-9_]*', self.source[self.pos:])
        if match:
            raw = match.group(0)
            if raw == "true":
                self.tokens.append(Token(TokenType.BOOLEAN, True, self.line, self.column))
            elif raw == "false":
                self.tokens.append(Token(TokenType.BOOLEAN, False, self.line, self.column))
            else:
                self.tokens.append(Token(TokenType.STRING, raw, self.line, self.column))
            self.pos += len(raw)
            self.column += len(raw)

    def _tokenize_jsx_mode(self):
        depth = 1
        jsx_str = ""
        start_line, start_col = self.line, self.column
        
        while self.pos < len(self.source) and depth > 0:
            char = self.source[self.pos]
            if char == '(':
                depth += 1
            elif char == ')':
                depth -= 1
                if depth == 0:
                    break
            jsx_str += char
            self.pos += 1
            if char == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1

        self.tokens.append(Token(TokenType.JSX_TEXT, jsx_str.strip(), start_line, start_col))
        self.tokens.append(Token(TokenType.RPAREN, ')', self.line, self.column))
        self.pos += 1