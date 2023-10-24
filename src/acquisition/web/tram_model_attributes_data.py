from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
from pathlib import Path

from src.acquisition.web.constants import TRAM_NAME_LENGTH, DEFAULT_EXCEL_INPUT_PATH
from src.acquisition.web.tram_models import change_column_names


@dataclass(frozen=True)
class TramModelsAttributesData:
    """

    """
    model_attributes: pd.DataFrame
    excel_path: Path = DEFAULT_EXCEL_INPUT_PATH

    @classmethod
    def from_excel(cls, excel_path: Path = DEFAULT_EXCEL_INPUT_PATH) -> TramModelsAttributesData:
        data = pd.read_excel(excel_path)

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

        data.columns = [change_column_names(col) for col in data.columns]

        return cls(data, excel_path)
