from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

import pandas as pd
from pathlib import Path

from constants import  TRAM_NAME_LENGTH, DEFAULT_TRAM_MODELS_SAVE_PATH, TRAM_MODELS_ATTRIBUTES

# I 
# HATE
# PATHS
#DEFAULT_TRAM_MODELS_SAVE_PATH = Path('./data/generated/data/')
#TRAM_MODELS_ATTRIBUTES = r'~/data/Tramwaje_dane_modeli.xlsx'

@dataclass(frozen=True)
class TramModelsAttributesData:
    """

    """
    path: Path = DEFAULT_TRAM_MODELS_SAVE_PATH
    excel: str = TRAM_MODELS_ATTRIBUTES

    @classmethod
    def from_excel(cls, path: Path = DEFAULT_TRAM_MODELS_SAVE_PATH, excel: str = excel) -> TramModelsAttributesData:
        data = pd.read_excel('data/Tramwaje_dane_modeli.xlsx')

        data = data.fillna(0)

        data['Model'] = data['Model'].astype(str)
        data['Wielkość'] = data['Wielkość'].astype(str)
        data['Rodzaj'] = data['Rodzaj'].astype(str)
        data['Długość'] = data['Długość'].astype(float)
        data['Szerokość'] = data['Szerokość'].astype(float)
        data['Wysokość nadwozia'] = data['Wysokość nadwozia'].astype(float)
        data['Rozstaw czopów skrętu'] = data['Rozstaw czopów skrętu'].astype(float)
        data['Rozstaw osi'] = data['Rozstaw osi'].astype(float)
        data['Masa własna'] = data['Masa własna'].astype(int)
        data['Masa całkowita'] = data['Masa całkowita'].astype(int)
        data['Miejsca ogółem'] = data['Miejsca ogółem'].astype(int)
        data['Miejsca siedzące'] = data['Miejsca siedzące'].astype(int)
        data['Wysokość podłogi przy wejściu'] = data['Wysokość podłogi przy wejściu'].astype(float)
        data['Liczba silników'] = data['Liczba silników'].astype(int)
        data['Moc silnika'] = data['Moc silnika'].astype(float)
        data['Średnica kół tocznych'] = data['Średnica kół tocznych'].astype(float)

        data.to_pickle(f"{path}/vehicles_types.pkl")

TramModelsAttributesData.from_excel(DEFAULT_TRAM_MODELS_SAVE_PATH, TRAM_MODELS_ATTRIBUTES)

