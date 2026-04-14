"""Custom indicator service layer."""
from typing import Dict, Any, Callable, Optional
import ast
import logging

logger = logging.getLogger(__name__)


class CustomIndicator:
    """Represents a custom indicator."""
    
    def __init__(self, name: str, expression: str, description: Optional[str] = None):
        """
        Initialize a custom indicator.
        
        Args:
            name: Name of the indicator
            expression: Python expression to calculate the indicator
            description: Optional description of the indicator
        """
        self.name = name
        self.expression = expression
        self.description = description or ""
        self._compiled: Optional[Callable] = None
        self._validate_expression()
    
    def _validate_expression(self):
        """Validate the expression for safety and correctness."""
        try:
            # Parse the expression to AST for validation
            tree = ast.parse(self.expression, mode='eval')
            
            # Validate that only allowed nodes are present
            allowed_types = {
                ast.Expression, ast.Name, ast.Constant, ast.Num, ast.Str,
                ast.BinOp, ast.UnaryOp, ast.Add, ast.Sub, ast.Mult, ast.Div,
                ast.FloorDiv, ast.Mod, ast.Pow, ast.LShift, ast.RShift,
                ast.BitOr, ast.BitXor, ast.BitAnd, ast.Invert,
                ast.Not, ast.UAdd, ast.USub, ast.Compare, ast.Eq, ast.NotEq,
                ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.Is, ast.IsNot,
                ast.In, ast.NotIn, ast.BoolOp, ast.And, ast.Or,
                ast.IfExp, ast.Attribute, ast.Subscript, ast.Slice,
                ast.ExtSlice, ast.Index, ast.Starred, ast.Call,
                ast.Load, ast.Store, ast.Del,
                # Allow common math operations if we provide them in globals
            }
            
            # Simple traversal to check for forbidden nodes
            for node in ast.walk(tree):
                if type(node) not in allowed_types:
                    raise ValueError(f"Forbidden node type in expression: {type(node).__name__}")
            
            # Compile the expression for later use
            self._compiled = compile(self.expression, filename='<custom_indicator>', mode='eval')
            logger.debug(f"Successfully validated and compiled indicator: {self.name}")
            
        except SyntaxError as e:
            logger.error(f"Syntax error in indicator expression: {e}")
            raise
        except Exception as e:
            logger.error(f"Error validating indicator expression: {e}")
            raise
    
    def calculate(self, data: Dict[str, Any]) -> Any:
        """
        Calculate the indicator value using the provided data.
        
        Args:
            data: Dictionary of data to use in the expression
            
        Returns:
            Calculated indicator value
        """
        if not self._compiled:
            raise RuntimeError("Indicator has not been compiled")
        
        try:
            # Provide a safe globals dict with common utilities
            safe_globals = {
                '__builtins__': {
                    'abs': abs, 'round': round, 'min': min, 'max': max,
                    'sum': sum, 'len': len,
                }
            }
            
            return eval(self._compiled, safe_globals, data)
            
        except Exception as e:
            logger.error(f"Error calculating indicator {self.name}: {e}")
            raise


class CustomIndicatorManager:
    """Manages registration and retrieval of custom indicators."""
    
    def __init__(self):
        """Initialize the indicator manager."""
        self._indicators: Dict[str, CustomIndicator] = {}
    
    def register(self, indicator: CustomIndicator) -> None:
        """
        Register a custom indicator.
        
        Args:
            indicator: The indicator to register
        """
        if indicator.name in self._indicators:
            logger.warning(f"Overwriting existing indicator: {indicator.name}")
        
        self._indicators[indicator.name] = indicator
        logger.info(f"Registered indicator: {indicator.name}")
    
    def unregister(self, name: str) -> bool:
        """
        Unregister a custom indicator.
        
        Args:
            name: Name of the indicator to unregister
            
        Returns:
            True if indicator was unregistered, False if not found
        """
        if name in self._indicators:
            del self._indicators[name]
            logger.info(f"Unregistered indicator: {name}")
            return True
        
        logger.warning(f"Indicator not found: {name}")
        return False
    
    def get(self, name: str) -> Optional[CustomIndicator]:
        """
        Get a registered indicator by name.
        
        Args:
            name: Name of the indicator to retrieve
            
        Returns:
            The indicator if found, None otherwise
        """
        return self._indicators.get(name)
    
    def list_indicators(self) -> Dict[str, CustomIndicator]:
        """
        Get all registered indicators.
        
        Returns:
            Dictionary of indicator name to indicator object
        """
        return self._indicators.copy()


# Global indicator manager instance
indicator_manager = CustomIndicatorManager()
