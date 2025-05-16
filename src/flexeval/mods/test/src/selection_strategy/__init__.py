from flexeval.mods.test.src.System import System
from importlib import import_module
from .core import SelectionBase

AVAILABLE_MODULES = ["least_seen", "latin_square"]  # NOTE: if possible, it would be good to get rid of this!


def get_strategy(strategy_name: str, systems: dict[str, System]) -> SelectionBase:
    strategy = None

    for module_path in AVAILABLE_MODULES:
        try:
            module = import_module(f"flexeval.mods.test.src.selection_strategy.{module_path}")
            strategy_cls = getattr(module, strategy_name)
            strategy = strategy_cls(systems)
        except (ImportError, AttributeError):
            # FIXME: really check if it exists here, all other exceptions should be reported
            continue

    # Least Seen module
    if strategy is None:
        raise Exception(f"{strategy_name} is not a valid strategies: a corresponding class doesn't exist")
    elif not isinstance(strategy, SelectionBase):
        raise Exception(
            f"{strategy_name} is not a valid strategies: the corresponding class doesn't subclass SelectionBase"
        )

    return strategy


__all__ = ["SelectionBase", "get_strategy"]
