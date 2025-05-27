# Reference: https://docs.python.org/3/library/xml.etree.elementtree.html
import xml.etree.ElementTree as ET
from types import MappingProxyType
from .enums import StandardType
from .enums import EErrorTerms12

class rf_cal_settings:
    def __init__(self):
        self.__measured: MappingProxyType[StandardType, str]
        self.__model: MappingProxyType[StandardType, str]
        self.__measured_sw: MappingProxyType[StandardType, str]
        self.__ets: MappingProxyType[EErrorTerms12, str]
        self.__settings: MappingProxyType[str, str]
        self.__output_parameter: MappingProxyType[str, str]
    
    def read(self, file: str):
        """
        
        """
        tree = ET.parse(file)
        root = tree.getroot()
        tag = root.tag
        attrib = root.attrib
        print('Tag:{}, Attribute:{}'.format(tag, attrib))
        cal_method: str = attrib['method']

        for child in root:
            tag = child.tag
            attrib = child.attrib
            print('Child: Tag:{}, Attribute:{}'.format(tag, attrib))
            if tag == 'settings':
                settings = {}
                for c in child:
                    setting_method: str = c.attrib['name']
                    print('Settings Method: {}'.format(setting_method))
                    if c.tag == 'method' and cal_method == setting_method:
                        settings['name'] = setting_method
                        for cc in c:
                            setting_name = cc.tag
                            setting_value = c.find(setting_name).text
                            settings[setting_name] = setting_value
                            print('Parameter Name:{}, Value:{}'.format(setting_name, setting_value))
                self.__settings = MappingProxyType(settings)
            elif tag == 'snp' and attrib['name'] == 'measured':
                stds = {}
                gthru = {}
                for c in child:
                    tag_child = c.tag
                    std_snp = child.find(tag_child).text
                    print('Measured standard:{}, SNP:{}'.format(tag_child, std_snp))
                    std: StandardType = self.__get_std_type(tag_child)
                    if tag_child == f'g{self.__get_std_str(std)}':
                        gthru[std] = std_snp
                    else:
                        stds[std] = std_snp
                self.__measured = MappingProxyType(stds)
                self.__measured_sw = MappingProxyType(gthru)
            elif tag == 'snp' and attrib['name'] == 'model':
                stds = {} 
                for c in child:
                    tag_child = c.tag
                    std_snp = child.find(tag_child).text
                    print('Model standard:{}, SNP:{}'.format(tag_child, std_snp))
                    std: StandardType = self.__get_std_type(tag_child)
                    stds[std] = std_snp
                self.__model = MappingProxyType(stds)
            elif tag == 'snp' and attrib['name'] == 'error_term':
                ets = {} 
                for c in child:
                    tag_child = c.tag
                    et_snp = child.find(tag_child).text
                    print('Error Term:{}, SNP:{}'.format(tag_child, et_snp))
                    et: EErrorTerms12 = self.__get_ets_type(tag_child)
                    ets[et] = et_snp
                self.__ets = MappingProxyType(ets)
            elif tag == 'snp' and attrib['name'] == 'output_parameter':
                output_parameter = {} 
                for c in child:
                    tag_child = c.tag
                    output_parameter_snp = child.find(tag_child).text
                    print('Error Term:{}, SNP:{}'.format(tag_child, output_parameter_snp))
                    output_parameter[tag_child] = output_parameter_snp
                self.__output_parameter = MappingProxyType(output_parameter)
    
    @property
    def get_measured_snp(self) -> MappingProxyType:
        return self.__measured

    @property
    def get_measured_sw_snp(self) -> MappingProxyType:
        return self.__measured_sw

    @property
    def get_model_snp(self) -> MappingProxyType:
        return self.__model

    @property
    def get_ets_snp(self) -> MappingProxyType:
        return self.__ets
    
    @property
    def get_output_parameter_snp(self) -> MappingProxyType:
        return self.__output_parameter
    
    @property
    def get_settings(self) -> MappingProxyType:
        return self.__settings

    def __get_std_str(self, std: StandardType) ->str:
        if std == StandardType.Thru:
            return 'thru'
        elif std == StandardType.ThruStraight:
            return 'thru_straight'
        elif std == StandardType.ThruLoopBackLeft:
            return 'thru_loopbackleft'
        elif std == StandardType.ThruLoopBackRight:
            return 'thru_loopbackright'
        elif std == StandardType.ThruLoopBack:
            return 'thru_loopback'
        elif std == StandardType.ThruNwSe:
            return 'thru_nwse'
        elif std == StandardType.ThruSwNe:
            return 'thru_swne'
        elif std == StandardType.Line1:
            return 'line1'
        elif std == StandardType.Line2:
            return 'line2'
        elif std == StandardType.Line3:
            return 'line3'
        elif std == StandardType.Line4:
            return 'line4'
        elif std == StandardType.Line5:
            return 'line5'
        elif std == StandardType.Open:
            return 'open'
        elif std == StandardType.Short:
            return 'short'
        elif std == StandardType.Load:
            return 'load'

        return ''

    def __get_std_type(self, text: str) ->StandardType:
        if text == 'thru' or text == 'gthru':
            return StandardType.Thru
        elif text == 'thru_straight' or text == 'gthru_straight':
            return StandardType.ThruStraight
        elif text == 'thru_loopbackleft' or text == 'gthru_loopbackleft':
            return StandardType.ThruLoopBackLeft
        elif text == 'thru_loopbackright' or text == 'gthru_loopbackright':
            return StandardType.ThruLoopBackRight
        elif text == 'thru_loopback' or text == 'gthru_loopback':
            return StandardType.ThruLoopBack
        elif text == 'thru_nwse' or text == 'gthru_nwse':
            return StandardType.ThruNwSe
        elif text == 'thru_swne' or text == 'gthru_swne':
            return StandardType.ThruSwNe
        elif text == 'line1':
            return StandardType.Line1
        elif text == 'line2':
            return StandardType.Line2
        elif text == 'line3':
            return StandardType.Line3
        elif text == 'line4':
            return StandardType.Line4
        elif text == 'line5':
            return StandardType.Line5
        elif text == 'open':
            return StandardType.Open
        elif text == 'short':
            return StandardType.Short
        elif text == 'load':
            return StandardType.Load

        return StandardType.Unknown

    def __get_ets_type(self, text: str) ->EErrorTerms12:
        if text == 'fwd_ed':
            return EErrorTerms12.FwdEd
        elif text == 'fwd_es':
            return EErrorTerms12.FwdEs
        elif text == 'fwd_ert':
            return EErrorTerms12.FwdErt
        elif text == 'rev_ed':
            return EErrorTerms12.RevEd
        elif text == 'rev_es':
            return EErrorTerms12.RevEs
        elif text == 'rev_ert':
            return EErrorTerms12.RevErt
        elif text == 'fwd_ex':
            return EErrorTerms12.FwdEx
        elif text == 'fwd_el':
            return EErrorTerms12.FwdEl
        elif text == 'fwd_ett':
            return EErrorTerms12.FwdEtt
        elif text == 'rev_ex':
            return EErrorTerms12.RevEx
        elif text == 'rev_el':
            return EErrorTerms12.RevEl
        elif text == 'rev_ett':
            return EErrorTerms12.RevEtt

        return EErrorTerms12.Unknown
        
def main():
    file: str = r'C:/Users/User/Desktop/python_rf_cal_engine/cal_settings.xml'
    cal_par: rf_cal_settings = rf_cal_settings()
    cal_par.read(file)
    print("--------------------------------------")
    print("--------------Result------------------")
    print("--------------------------------------")
    print(cal_par.get_measured_snp)
    print(cal_par.get_measured_sw_snp)
    print(cal_par.get_model_snp)
    print(cal_par.get_settings)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print("An exception occurred: {}".format(str(e)))