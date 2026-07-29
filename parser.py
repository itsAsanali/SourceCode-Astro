import json
from typing import List, Dict, Any
from ast_nodes import ComponentNode, StateNode, MethodNode, EffectNode
from lexer import Token, TokenType

class AstroParser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def parse_component(self) -> ComponentNode:
        raw_dict = self._parse_json_structure()
        
        comp = ComponentNode(name=raw_dict.get("component", "AstroComponent"))
        comp.imports = raw_dict.get("imports", {})
        comp.props = raw_dict.get("props", {})

        for name, init_val in raw_dict.get("state", {}).items():
            comp.states.append(StateNode(name=name, initial_value=init_val))

        for name, body in raw_dict.get("methods", {}).items():
            comp.methods.append(MethodNode(name=name, params=[], body=body))

        for eff in raw_dict.get("effects", []):
            comp.effects.append(EffectNode(
                dependencies=eff.get("deps", []),
                body=eff.get("body", "")
            ))

        comp.styles = raw_dict.get("styles", {})
        comp.render_tree = raw_dict.get("render", "<div></div>")
        
        return comp

    def _parse_json_structure(self) -> Dict[str, Any]:
        res_str = ""
        for tok in self.tokens:
            if tok.type == TokenType.JSX_TEXT:
                escaped = json.dumps(tok.value)
                res_str += f"{escaped}"
            elif tok.type == TokenType.EOF:
                break
            elif tok.type == TokenType.STRING:
                res_str += json.dumps(tok.value)
            elif tok.type == TokenType.NUMBER:
                res_str += str(tok.value)
            elif tok.type == TokenType.BOOLEAN:
                res_str += "true" if tok.value else "false"
            elif tok.type == TokenType.COLON:
                res_str += ":"
            elif tok.type == TokenType.COMMA:
                res_str += ","
            elif tok.type == TokenType.LBRACE:
                res_str += "{"
            elif tok.type == TokenType.RBRACE:
                res_str += "}"
            elif tok.type == TokenType.LBRACKET:
                res_str += "["
            elif tok.type == TokenType.RBRACKET:
                res_str += "]"
            elif tok.type in (TokenType.LPAREN, TokenType.RPAREN):
                continue

        return json.loads(res_str)