from typing import Tuple
from skrf import Network as network
import skrf.frequency as frequency
from types import MappingProxyType
from .enums import StandardType
from .enums import EErrorTerms12
from .rf_cal_base import rf_cal_base
import os
from os.path import exists
from .umTRL import umTRL

class rf_cal_umtrl(rf_cal_base):
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
        self.__cal: umTRL
        
    def _set_standards(self) -> None:
        """
        Calibration standards for LRRM
        """
        std_list: list = []
        for key, value in self._measured.items():
            std_list.append(key)
            if self._is_thru_type(key):
                self.__thru_type = key
        self._stds: tuple = tuple(std_list)

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
        lines: network = []
        reflect: network
        line_lengths = []
        att_name_reflect: str = ''
        for std in self._stds:
            if self._is_thru_type(std):
                lines.append(network(file=self._measured[std]))
                file_name: str = os.path.basename(self._measured[std])
                att_name = 'length_{}'.format(os.path.splitext(file_name)[0]).lower()
                if att_name in settings:
                    line_lengths.append(float(settings[att_name]))
                break
                
        for std in self._stds:
            if self._is_line(std):
                lines.append(network(self._measured[std]))
                file_name: str = os.path.basename(self._measured[std])
                att_name = 'length_{}'.format(os.path.splitext(file_name)[0]).lower()
                if att_name in settings:
                    line_lengths.append(float(settings[att_name]))

            if self._is_reflect(std):
                reflect = network(self._measured[std])
                file_name: str = os.path.basename(self._measured[std])
                att_name = 'offset_{}'.format(os.path.splitext(file_name)[0]).lower()
                att_name_reflect = att_name
        
        measured_sw: network = network(self._measured_switch[self.__thru_type])
        switch_term: network = [measured_sw.s21, measured_sw.s12]

        reflect_est = int(settings['reflect_est']) # open=1 or short=-1
        reflect_offset = float(settings[att_name_reflect]) # unit: mm
        ereff_est = complex(float(settings['ereff_est']), 0.0) # unit: None
        self.__cal = umTRL(lines=lines, line_lengths=line_lengths, reflect=reflect, 
                            reflect_est=reflect_est, reflect_offset=reflect_offset, 
                            ereff_est=ereff_est, switch_term=switch_term)
        self.__cal.run_mTRL()
        # shift plane
        ref_plane = float(settings['ref_plane'])
        self.__cal.shift_plane(ref_plane)
        self.__cal.error_coef()
        
    def save_ets(self, files: MappingProxyType) -> None:
        """
        Save error term to S1P file
        """
        
        # get file directory
        file_dir = os.path.dirname(files[EErrorTerms12.FwdEd])
        # Save gamma
        file = rf'{file_dir}\gamma.s1p'
        gamma = self.__cal.gamma
        ntw_ets: network =network(s=gamma,frequency=self.__cal.f)
        ntw_ets.write_touchstone(file)
        # Save ereff
        file = rf'{file_dir}\ereff.s1p'
        ereff = self.__cal.ereff
        ntw_ets: network =network(s=ereff,frequency=self.__cal.f)
        ntw_ets.write_touchstone(file)
        """
        # forward direction
        self.coefs['EDF'] = EDF
        self.coefs['ESF'] = ESF
        self.coefs['ERF'] = ERF
        self.coefs['ELF'] = ELF
        self.coefs['ETF'] = ETF
        self.coefs['EXF'] = EXF
        self.coefs['GF']  = GF

        # reverse direction
        self.coefs['EDR'] = EDR
        self.coefs['ESR'] = ESR
        self.coefs['ERR'] = ERR
        self.coefs['ELR'] = ELR
        self.coefs['ETR'] = ETR
        self.coefs['EXR'] = EXR
        self.coefs['GR']  = GR
        """
        ets12_ntwks = self.__cal.coefs
        for key in ets12_ntwks:
            try:
                et_type: EErrorTerms12 = EErrorTerms12.Unknown
                if key == 'EDF':
                    et_type = EErrorTerms12.FwdEd
                elif key == 'ESF':
                    et_type = EErrorTerms12.FwdEs
                elif key == 'ERF':
                    et_type = EErrorTerms12.FwdErt
                elif key == 'EDR':
                    et_type = EErrorTerms12.RevEd
                elif key == 'ESR':
                    et_type = EErrorTerms12.RevEs
                elif key == 'ERR':
                    et_type = EErrorTerms12.RevErt
                elif key == 'EXF':
                    et_type = EErrorTerms12.FwdEx
                elif key == 'ELF':
                    et_type = EErrorTerms12.FwdEl
                elif key == 'ETF':
                    et_type = EErrorTerms12.FwdEtt
                elif key == 'EXR':
                    et_type = EErrorTerms12.RevEx
                elif key == 'ELR':
                    et_type = EErrorTerms12.RevEl
                elif key == 'ETR':
                    et_type = EErrorTerms12.RevEtt
                    
                if et_type == EErrorTerms12.Unknown:
                    continue

                file: str = files[et_type]
                ntw_ets: network =network(s=ets12_ntwks[key],name=f'{et_type}',frequency=self.__cal.f)
                ntw_ets.write_touchstone(file)
            except Exception as e:
                self._log(e)