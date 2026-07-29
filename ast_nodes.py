from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

class ASTNode:
    pass

@dataclass
class JSXAttribute(ASTNode):
    name: str
    value: Any

@dataclass
class JSXElement(ASTNode):
    tag: str
    attributes: List[JSXAttribute]
    children: List[Any]

@dataclass
class StateNode(ASTNode):
    name: str
    initial_value: Any

@dataclass
class MethodNode(ASTNode):
    name: str
    params: List[str]
    body: str

@dataclass
class EffectNode(ASTNode):
    dependencies: List[str]
    body: str

@dataclass
class ComponentNode(ASTNode):
    name: str
    imports: Dict[str, List[str]] = field(default_factory=dict)
    props: Dict[str, Any] = field(default_factory=dict)
    states: List[StateNode] = field(default_factory=list)
    methods: List[MethodNode] = field(default_factory=list)
    effects: List[EffectNode] = field(default_factory=list)
    styles: Dict[str, Dict[str, str]] = field(default_factory=dict)
    render_tree: Optional[str] = None