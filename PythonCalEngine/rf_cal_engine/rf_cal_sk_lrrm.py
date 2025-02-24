# Reference: https://scikit-rf.readthedocs.io/en/latest/api/calibration/generated/skrf.calibration.calibration.LRRM.html#skrf.calibration.calibration.LRRM
from typing import Tuple
import numpy as np
from skrf import Network as network
from skrf.calibration import LRRM
from types import MappingProxyType
from .enums import StandardType
from .enums import EErrorTerms12
from .rf_cal_base import rf_cal_base
from os.path import exists

class rf_cal_sk_lrrm(rf_cal_base):
    def __init__(self, 
                models: MappingProxyType, 
                measured: MappingProxyType, 
                measured_switch: MappingProxyType):
        """
        ---
        Types:
        ---
        MappingProxyType: Key is 'StandardType'; Value is 'str'

        ---
        Parameters:
        ---
        models: Contain 'Thru', 'Open', 'Short' and 'Load' SNP file
        measured: Contain 'Thru', 'Open', 'Short' and 'Load' SNP file
        measured_switch: Contain 'Thru' SNP file
        """        
        self.__thru_type = StandardType.Thru
        super().__init__(models, measured, measured_switch)
        self.__cal: LRRM
        

    def _set_standards(self) -> None:
        """
        Calibration standards for LRRM
        """
        self._stds: tuple = (StandardType.Thru, StandardType.Open, StandardType.Short, StandardType.Load)

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

            # get self._measured thru
            snp_file: str = self._measured_switch[self.__thru_type]
            if not exists(snp_file):
                self._msg = r'{} measured switch term SNP file not exist'.format(s)
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
        
        ntw_sw: network = network(self._measured_switch[self.__thru_type])
        measured_sw: network = [ntw_sw.s21, ntw_sw.s12]
        match_fit = settings['match_fit'] # l, lc, none
        # TODO: Check with Andrej
        #match_port = settings['match_port']        
        self.__cal = LRRM(ideals = model, measured = measured, switch_terms = measured_sw, match_fit=match_fit)
        self.__cal.run()

    def save_ets(self, files: MappingProxyType) -> None:
        """
        Save error term to S1P file
        """
        ets12_ntwks = self.__cal.coefs_12term_ntwks
        for key in ets12_ntwks:
            try:
                et_type: EErrorTerms12 = self._get_ets_type(key)
                file: str = files[et_type]
                ntw_ets: network = ets12_ntwks[key]
                ntw_ets.write_touchstone(file)
            except Exception as e:
                self._log(e)

    def save_solved_parameter(self, files: MappingProxyType) ->None:
        solved_l = self.__cal.solved_l
        solved_c = self.__cal.solved_c
        solved_m = self.__cal.solved_m
        solved_r1 = self.__cal.solved_r1
        solved_r2 = self.__cal.solved_r2
        
        if "solved_l" in files:
            # Float to complex list
            complex_list = [complex(num) for num in solved_l]
            # Complex list to scikit-rf network
            n_freqs = len(complex_list)
            s_parameters = np.array(complex_list).reshape((n_freqs, 1, 1))
            solved_l_nwt = network(frequency=solved_m.frequency, s=s_parameters)
            # Save SNP file by scikit-rf network
            file: str = files["solved_l"]
            solved_l_nwt.write_touchstone(file)
        
        if "solved_c" in files:
            # Complex list to scikit-rf network
            s_parameters = np.array(solved_c).reshape((n_freqs, 1, 1))
            solved_c_nwt = network(frequency=solved_m.frequency, s=s_parameters)
            # Save SNP file by scikit-rf network
            file: str = files["solved_c"]
            solved_c_nwt.write_touchstone(file)

        if "solved_m" in files:
            # Save SNP file by scikit-rf network
            file: str = files["solved_m"]
            solved_m.write_touchstone(file)

        if "solved_r1" in files:
            # Save SNP file by scikit-rf network
            file: str = files["solved_r1"]
            solved_r1.write_touchstone(file)

        if "solved_r2" in files:
            # Save SNP file by scikit-rf network
            file: str = files["solved_r2"]
            solved_r2.write_touchstone(file)