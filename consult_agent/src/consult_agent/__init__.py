"""Agent care transforma dictarea unui consult medical intr-un raport structurat."""

from .pipeline import Result, run
from .schema import Template, load_template

__all__ = ["Result", "Template", "load_template", "run"]
__version__ = "0.1.0"
