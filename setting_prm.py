import math, random

class VlcSetting:
    def __init__(self):
        pass
    START_VLC = 3.0

    def calc_base_vlc(self, dst):
        return 20.0 - (dst - 2000) / 1000

    def calc_limit_vlc(self, base_vlc):
        return 0.85 * base_vlc

    def calc_blocked_limit_vlc(self, itv_front, front_vlc):
        return (0.988 + 0.006 * itv_front) * front_vlc

    def calc_min_vlc(self, rev_gut, base_vlc):
        return 0.85 * base_vlc + ((200.0 * rev_gut)**0.5) * 0.001
   
    def calc_base_target_vlc(self, sct, base_vlc, rst, phase, rev_spd, rev_itl, prop_dst):
        RST_PHASE_COEFDICT = {
            "大逃げ": (1.063, 0.962, 0.950, 0.950),
            "逃げ": (1.000, 0.980, 0.962, 0.962),
            "先行": (0.978, 0.991, 0.975, 0.975),
            "差し": (0.938, 0.998, 0.994, 0.994),
            "追込": (0.931, 1.000, 1.000, 1.000)
        }
        PROP_DST_COEFDICT = {"S":1.05, "A":1.0, "B":0.9, "C":0.8, "D":0.6, "E":0.4, "F":0.2, "G":0.1}
        
        itl_rev = self.calc_itl_rands_rev(sct, rev_itl, base_vlc)

        if phase == 0 or phase == 1:
            return base_vlc * RST_PHASE_COEFDICT[rst][phase] * (1 + itl_rev)
        elif phase == 2 or phase == 3:
            return base_vlc * RST_PHASE_COEFDICT[rst][phase] * (1 + itl_rev) + math.sqrt(500.0 * rev_spd) * PROP_DST_COEFDICT[prop_dst] * 0.002
        else:
            raise Exception("Error: phase must be between 0 and 3")

    def calc_itl_rands_rev(self, sct, rev_itl, base_vlc):
        upper_percent = (rev_itl/5500) * math.log10(rev_itl * 0.1)
        lower_percent = upper_percent - 0.65
        itl_rand_list = []
        for i in range(24):
            rand = random.uniform(upper_percent/100, lower_percent/100)
            itl_rand_list.append(rand)
        return itl_rand_list[sct-1] * base_vlc

    def calc_target_vlc(self, rst, base_target_vlc, mode, is_upslp, is_dnslp, is_dnslp_aclmode, ang, rev_pwr):
        POSITION_KEEP_COEFDICT = {
            "normal": 1.0,
            "speedup": 1.04,
            "overtake": 1.05,
            "paceup": 1.04, 
            "pacedown": 0.915
        }

        RST_REV = {"逃げ":0.02, "先行":0.01, "差し":0.01, "追込":0.03}
        inner_move_rev = random.uniform(0, 0.1) + RST_REV[rst]

        skl_rev = 0

        if is_upslp:
            slp_rev = abs(100 * math.tan(ang) * 0.017453) * 200 / rev_pwr
        elif is_dnslp and is_dnslp_aclmode:
            slp_rev = 0.3 + abs(math.tan(ang) * 0.017453) / 10
        else:
            slp_rev = 0

        return base_target_vlc * POSITION_KEEP_COEFDICT[mode] + inner_move_rev + skl_rev + slp_rev

class AclSetting:
    def __init__(self):
        pass

class HtpSetting:
    def __init__(self):
        pass
    
    def calc_init_htp(self, rst, rev_stm, dst):
        RST_COEFDICT = {"大逃げ": 0.86, "逃げ": 0.95, "先行": 0.89, "差し": 1.00, "追込": 0.995}
        return 0.8 * RST_COEFDICT[rst] * rev_stm + dst

    def calc_consumption_htp_persec(self, is_inp, is_pacedown, is_dwnslp_aclmode, c_vlc, base_vlc, grd, cnd, phase, rev_gut):
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
            return base_consumption * gut_coef
        else:
            return base_consumption

def show_init_prm_list(init_hp):
    init_prm_dict = dict(
    init_pst = 0,
    init_spd = 3.0,
    init_acl = 24.0,
    init_HP = init_hp,
    init_mode = 0
    )
    return init_prm_dict.values()