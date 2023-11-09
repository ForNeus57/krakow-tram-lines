from dataclasses import dataclass
from pathlib import Path
from typing import Literal


@dataclass(frozen=True)
class SavingInfo:
    save_path: Path
    force_save: bool = False
    format: Literal['excel', 'pickle', 'both'] = 'both'
