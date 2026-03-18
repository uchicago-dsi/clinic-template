"""Basic scaffold for any inference strategy."""
from abc import ABC, abstractmethod
from typing import Any

from {{ cookiecutter.code_directory }}.register import discover_subclasses, get_subclass


class InferenceStrategy(ABC):
    """Abstract base class for inference strategies."""

    @abstractmethod
    def do_inference(self, inference_input: Any) -> dict[str, Any]:
        pass

    def metadata(self) -> dict[str, Any]:
        """Metadata about the inference strategy."""
        return {
            "name": self.__class__.__name__,
            "description": self.__doc__,
            "parameters": self.parameters(),
        }

    def parameters(self) -> dict[str, Any]:
        """Parameters for the inference strategy."""
        return {
            key: value
            for key, value in self.__dict__.items()
            if not callable(value) and not key.startswith('_')
        }


def discover_inference_strategies() -> dict[str, type]:
    """Discover all concrete InferenceStrategy subclasses in the inference_strategies package."""
    from {{ cookiecutter.code_directory }} import inference_strategies as pkg
    return discover_subclasses(pkg, InferenceStrategy)


def get_inference_strategy(name: str) -> type:
    """Get a specific InferenceStrategy subclass by class name."""
    from {{ cookiecutter.code_directory }} import inference_strategies as pkg
    return get_subclass(name, pkg, InferenceStrategy, label="inference strategy")
