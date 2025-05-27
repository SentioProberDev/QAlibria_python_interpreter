import sys
from types import MappingProxyType
from rf_cal_engine.rf_cal_base import rf_cal_base
from rf_cal_engine.rf_cal_settings import rf_cal_settings
from rf_cal_engine.rf_cal_sk_lrrm import rf_cal_sk_lrrm as sk_lrrm
from rf_cal_engine.rf_cal_sk_solt import rf_cal_sk_solt as sk_solt
from rf_cal_engine.rf_cal_sk_sol import rf_cal_sk_sol as sk_sol
from rf_cal_engine.rf_cal_umtrl import rf_cal_umtrl as rf_umtrl

def main(cal_file: str) -> None:
    """
    Execute calibration method
    """
    setting: rf_cal_settings = rf_cal_settings()
    setting.read(cal_file)
    method: str = setting.get_settings['name']
    if method == 'sk_lrrm':
        sk_cal_lrrm(setting)
    elif method == 'umtrl':
        sk_cal_umtrl(setting)
    elif method == 'sk_solt':
        sk_cal_solt(setting)
    elif method == 'sk_sol':
        sk_cal_sol(setting)
    else:
        raise Exception("Not support{}".format(method))

def sk_cal_lrrm(setting: rf_cal_settings) -> None:
    """
    Execute scikit-rf LRRM calibration method
    """
    measured: MappingProxyType = setting.get_measured_snp
    model: MappingProxyType = setting.get_model_snp
    measured_switch: MappingProxyType = setting.get_measured_sw_snp
    lrrm: rf_cal_base = sk_lrrm(model, measured, measured_switch)
    can_run, msg = lrrm.can_run()
    if not can_run:
        raise Exception(msg)
    lrrm.run(setting.get_settings)
    lrrm.save_ets(setting.get_ets_snp)
    lrrm.save_solved_parameter(setting.get_output_parameter_snp)

def sk_cal_umtrl(setting: rf_cal_settings) -> None:
    """
    Execute scikit-rf LRRM calibration method
    """
    measured: MappingProxyType = setting.get_measured_snp
    model: MappingProxyType = setting.get_model_snp
    measured_switch: MappingProxyType = setting.get_measured_sw_snp
    umtrl: rf_cal_base = rf_umtrl(model, measured, measured_switch)
    can_run, msg = umtrl.can_run()
    if not can_run:
        raise Exception(msg)
    umtrl.run(setting.get_settings)
    umtrl.save_ets(setting.get_ets_snp)

def sk_cal_solt(setting: rf_cal_settings) -> None:
    """
    Execute scikit-rf SOLT calibration method
    """
    measured: MappingProxyType = setting.get_measured_snp
    model: MappingProxyType = setting.get_model_snp
    solt: rf_cal_base = sk_solt(model, measured)
    can_run, msg = solt.can_run()
    if not can_run:
        raise Exception(msg)
    solt.run(setting.get_settings)
    solt.save_ets(setting.get_ets_snp)

def sk_cal_sol(setting: rf_cal_settings) -> None:
    """
    Execute scikit-rf SOL calibration method
    """
    measured: MappingProxyType = setting.get_measured_snp
    model: MappingProxyType = setting.get_model_snp
    sol: rf_cal_base = sk_sol(model, measured)
    can_run, msg = sol.can_run()
    if not can_run:
        raise Exception(msg)
    sol.run(setting.get_settings)
    sol.save_ets(setting.get_ets_snp)

if __name__ == '__main__':
    try:
        args = sys.argv
        # Debug use
        # cal_setting_xml: str = r'C:/ProgramData/MPI Corporation/QAlibria/PythonCalEngine/cal_settings.xml'
        # Release use
        cal_setting_xml: str = ""
        for idx in range(len(args)):
            print(r'Args[{}]:{}'.format(idx, args[idx]))
            if idx == 1:
                cal_setting_xml = args[idx]
                print(r'cal_setting_xml={}'.format(cal_setting_xml))
        
        if cal_setting_xml == "":
            raise Exception("No calibration setting file.")
        main(cal_setting_xml)
        print("Pass")
    except Exception as e:
        print(e)
        print("Fail")