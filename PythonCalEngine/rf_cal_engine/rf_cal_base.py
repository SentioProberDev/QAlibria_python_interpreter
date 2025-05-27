from abc import ABC, abstractmethod
# http://net-informations.com/python/iq/immutable.htm
# https://adamj.eu/tech/2022/01/05/how-to-make-immutable-dict-in-python/
from types import MappingProxyType
from typing import Tuple
from .enums import StandardType
from .enums import EErrorTerms12

class rf_cal_base(ABC):
    def __init__(self, 
                models: MappingProxyType, 
                measured: MappingProxyType, 
                measured_switch: MappingProxyType = None):
        """
        ---
        Types:
        ---
        MappingProxyType: Key is 'StandardType'; Value is 'str'

        Parameters(Calibration Data):
        ---
        models: SNP files.
        measured: SNP files.
        measured_switch(Option): SNP files.
        """
        self._models = models
        self._measured = measured
        self._measured_switch = measured_switch
        self._settings = None
        self._can_run: bool = False
        self._msg: str = ""
        self._set_standards()
        self._can_run, self._msg = self.can_run()

    @abstractmethod
    def _set_standards(self) -> None:
        """
        Standards for calibration method.
        """
        pass

    @abstractmethod
    def can_run(self) -> Tuple[bool, str]:
        """
        Check standards SNP file available.
        """
        pass


    @abstractmethod
    def run(self, settings: MappingProxyType) -> None:
        """
        Parameters(Calibration Settings):
        ---
        settings: Setting file for calibration
        """
        print("Calibration Implementation")

    @abstractmethod
    def save_ets(self, files: MappingProxyType) -> None:
        """
        Save error term to S1P file
        """
        print("Save Error Term Implementation")

    def _log(self, msg: str) -> None:
        print("cal exception:{}".format(msg))

    def _is_thru_type(self, std: StandardType) ->bool:
        if std == StandardType.Thru:
            return True
        elif std == StandardType.ThruStraight:
            return True
        elif std == StandardType.ThruLoopBackLeft:
            return True
        elif std == StandardType.ThruLoopBackRight:
            return True
        elif std == StandardType.ThruLoopBack:
            return True
        elif std == StandardType.ThruNwSe:
            return True
        elif std == StandardType.ThruSwNe:
            return True

        return False

    def _get_ets_type(self, text: str) ->EErrorTerms12:
        if text == 'forward directivity' or text == 'directivity':
            return EErrorTerms12.FwdEd
        elif text == 'forward source match' or text == 'source match':
            return EErrorTerms12.FwdEs
        elif text == 'forward reflection tracking' or text == 'reflection tracking':
            return EErrorTerms12.FwdErt
        elif text == 'reverse directivity':
            return EErrorTerms12.RevEd
        elif text == 'reverse source match':
            return EErrorTerms12.RevEs
        elif text == 'reverse reflection tracking':
            return EErrorTerms12.RevErt
        elif text == 'forward isolation':
            return EErrorTerms12.FwdEx
        elif text == 'forward load match':
            return EErrorTerms12.FwdEl
        elif text == 'forward transmission tracking':
            return EErrorTerms12.FwdEtt
        elif text == 'reverse isolation':
            return EErrorTerms12.RevEx
        elif text == 'reverse load match':
            return EErrorTerms12.RevEl
        elif text == 'reverse transmission tracking':
            return EErrorTerms12.RevEtt

        return EErrorTerms12.Unknown

    def _is_line(self, std: StandardType) ->bool:
        str_std = str(std)
        return "LINE" in str_std.upper()

    def _is_reflect(self, std: StandardType) ->bool:
        return std == StandardType.Open or std == StandardType.Short
