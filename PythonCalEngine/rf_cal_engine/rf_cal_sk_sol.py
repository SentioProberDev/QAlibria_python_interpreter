# Reference: https://scikit-rf.readthedocs.io/en/latest/api/calibration/generated/skrf.calibration.calibration.OnePort.html#skrf.calibration.calibration.OnePort
from typing import Tuple
from skrf import Network as network
from skrf.calibration import OnePort
from types import MappingProxyType
from .enums import StandardType
from .enums import EErrorTerms12
from .rf_cal_base import rf_cal_base
from os.path import exists

class rf_cal_sk_sol(rf_cal_base):
    def __init__(self, 
                models: MappingProxyType, 
                measured: MappingProxyType):
        """
        ---
        Types:
        ---
        MappingProxyType: Key is 'StandardType'; Value is 'str'

        ---
        Parameters:
        ---
        models: Contain 'Short', 'Open' and 'Load' SNP file
        measured: Contain 'Short', 'Open' and 'Load' SNP file
        """
        super().__init__(models, measured)
        self.__cal: OnePort

    def _set_standards(self) -> None:
        """
        Calibration standards for SOLT
        """
        self._stds: tuple = (StandardType.Short, StandardType.Open, StandardType.Load)

    def can_run(self) -> Tuple[bool, str]:
        """
        ---
        Checker:
        ---
        -SNP file exist
        """
        try:
            # Check SNP file exist
            for s in self._stds:
                snp_file: str = self._measured[s]
                if not exists(snp_file):
                    self._msg = r'{} measured SNP file not exist'.format(s)
                    raise Exception(self._msg)
                snp_file: str = self._models[s]
                if not exists(snp_file):
                    self._msg = r'{} model SNP file not exist'.format(s)
                    raise Exception(self._msg)
        except Exception as e:
            self._log(e)
            self._can_run = False
            return False, self._msg

        self._can_run = True
        self._msg = ""
        return self._can_run, self._msg

    def run(self, settings: MappingProxyType) -> None:
        """
        Parameters(Calibration Settings):
        ---
        settings: Settings parameter
        """
        measured: network = []
        model: network = []
        for std in self._stds:
            measured.append(network(self._measured[std]))
            model.append(network(self._models[std]))
            
        self.__cal = OnePort(ideals = model, measured = measured)
        self.__cal.run()

    def save_ets(self, files: MappingProxyType) -> None:
        """
        Save error term to S1P file
        """
        ets3_ntwks = self.__cal.coefs_3term_ntwks
        for key in ets3_ntwks:
            try:
                et_type: EErrorTerms12 = self._get_ets_type(key)
                file: str = files[et_type]
                ntw_ets: network = ets3_ntwks[key]
                ntw_ets.write_touchstone(file)
            except Exception as e:
                self._log(e)