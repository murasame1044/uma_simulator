import math, random

class VlcRev:
    def __init__(self):
        pass
        
    def calc_gut_lastsplinting(self, rev_gut):
        return (450 * rev_gut) ** 0.597 * 0.0001
    
    def calc_lane_change_skill(self):
        """
        レーン移動速度アップのスキル効果中、レーン移動した次のfrで目標速度UP
        target_speed_rev = (0.0002 * rev_pwr) ** 0.5 [m/s]
        """
        pass
    
    class PositionKeep:
        def __init__(self):
            pass


class AclRev:
    def __init__(self):
        pass

    STARTDASH = 24.0

    def calc_accel(self, rev_pwr, rst, phase, prop_grd, prop_dst, act_skls, is_startdash):
        RST_PHASE_COEFDICT = {
            "大逃げ": (1.170, 0.940, 0.956, 0.956),
            "逃げ": (1.000, 1.000, 0.996, 0.996),
            "先行": (0.985, 1.000, 0.996, 0.996),
            "差し": (0.975, 1.000, 1.000, 1.000),
            "追込": (0.945, 1.000, 1.000, 0.997)
        }
        PROP_GRD_COEFDICT = {"S":1.05, "A":1.0, "B":0.9, "C":0.8, "D":0.6, "E":0.4, "F":0.2, "G":0.1}
        PROP_DST_COEFDICT = {"S":1.00, "A":1.0, "B":1.0, "C":1.0, "D":1.0, "E":0.6, "F":0.5, "G":0.4}
        rev_startdash = 24.0 if is_startdash else 0
        act_skls = 0 if act_skls == None else act_skls

        accel = 0.0006 * math.sqrt(500.0 * rev_pwr) * RST_PHASE_COEFDICT[rst][phase] * PROP_GRD_COEFDICT[prop_grd] * PROP_DST_COEFDICT[prop_dst] + act_skls + rev_startdash
        return accel


class HtpRev:
    def __init__(self):
        pass

    def calc_consumption_htp_persec(self, is_inp, is_pacedown, is_dwnslp_aclmode, c_vlc, base_vlc, grd, cnd, phase, rev_gut):
        FRMPERSEC = 0.066
        HORSE_INP_COEFDICT = {True: 1.6, False: 1.0}
        HORSE_PACEDOWN_COEFDICT = {True: 0.6, False: 1.0}
        HORSE_DWNSLP_ACLMODE_COEFDICT = {True: 0.4, False: 1.0}
        GRD_CND_COEFDICT = {
            "gls": {"不良":1.02, "重":1.02, "稍重":1.00, "良":1.00},
            "mud": {"不良":1.02, "重":1.01, "稍重":1.00, "良":1.00}
            }

        horse_situation_coef = HORSE_INP_COEFDICT[is_inp] * HORSE_PACEDOWN_COEFDICT[is_pacedown] * HORSE_DWNSLP_ACLMODE_COEFDICT[is_dwnslp_aclmode]
        base_consumption =  20.0 * horse_situation_coef * (c_vlc - base_vlc + 12.0) **2 / 144.0 * GRD_CND_COEFDICT[grd][cnd]
        if phase >= 2:
            gut_coef = (200 / math.sqrt(600 * rev_gut) + 1)
            return base_consumption * gut_coef * FRMPERSEC
        else:
            return base_consumption * FRMPERSEC
