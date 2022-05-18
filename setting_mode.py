import math, random

class Mode:  # mode = normal, speedup, overtake, pacedown, paceup の５種類
    def __init__(self):
        pass

    def show_mode(self, dst, rst, subrank, itv_top, is_inp, itv_back, rev_itl, is_actskls_spd):
        if rst == "逃げ":
            if subrank == 0:
                mode = "speedup"
            else:
                mode = "overtake"
        else:
            coef = 0.0008 * (dst - 1000) + 1.0

            RST_NORMAL_LIMIT_COEFDICT = {
                "先行": {"pacedown": 3.0 * coef, "paceup": 5.0 * coef},
                "差し": {"pacedown": 6.5 * coef, "paceup": 7.0 * coef},
                "追込": {"pacedown": 7.5 * coef, "paceup": 8.0 * coef}
            }

            if itv_top < RST_NORMAL_LIMIT_COEFDICT[rst]["pacedown"] and subrank!=0:
                mode = "pacedown"
            elif itv_top > RST_NORMAL_LIMIT_COEFDICT[rst]["paceup"]:
                mode = "paceup"
            else:
                mode = "normal"

            
    
        def jdg_start_speedup(self, is_inp, itv_back, rev_itl):
            if is_inp==True:
                return True

            elif is_inp==False and itv_back <= 4.5:
                prob = 20 * math.log10(rev_itl * 0.1) / 100
                rand = random.random()
                if rand < prob:
                    return True
                else:
                    return False
            else:
                return False

        def jdg_start_overtake(self, is_inp, rev_itl):
            if is_inp==True:
                return True

            elif is_inp==False:
                prob = 20 * math.log10(rev_itl * 0.1) / 100
                rand = random.random()
                if rand < prob:
                    return True
                else:
                    return False
            else:
                return False

        def jdg_start_paceup(self, is_inp, rev_itl):
            if is_inp==True:
                return True

            elif is_inp==False:
                prob = 15 * math.log10(rev_itl * 0.1) / 100
                rand = random.random()
                if rand < prob:
                    return True
                else:
                    return False
            else:
                return False

        def jdg_start_pacedown(self, is_actskls_spd):
            if is_actskls_spd==True:
                return False
            else:
                return True
                
        if mode == "speedup":
            jdg = jdg_start_speedup(self, is_inp, itv_back, rev_itl)
            mode = "speedup" if jdg == True else "normal"
        elif mode == "overtake":
            jdg = jdg_start_overtake(is_inp, rev_itl)
            mode = "overtake" if jdg == True else "normal"
        elif mode == "paceup":
            jdg = jdg_start_paceup(is_inp, rev_itl)
            mode = "paceup" if jdg == True else "normal"
        elif mode == "pacedown":
            jdg = jdg_start_pacedown(is_actskls_spd)
            mode = "pacedown" if jdg == True else "normal"

        return mode
            


    def jdg_stop_speedup(self, itv_back):
        return True if itv_back >= 4.5 else False
    
    def jdg_stop_overtake(self):
        """掛かりを考慮した同脚質で2位以下か、掛かりを考慮せず同脚質のウマが1人以下の場合は継続"""
        #  --> False
        """掛かりを考慮せずに同脚質の2位のウマと10mの差をつけると終了"""
        #  --> True
        return True

    def jdg_stop_paceup(self, rst, dst, itv_top):
        coef = 0.0008 * (dst - 1000) + 1.0
        RST_NORMAL_LIMIT_COEFDICT = {
            "先行": {"pacedown": 3.0 * coef, "paceup": 5.0 * coef},
            "差し": {"pacedown": 6.5 * coef, "paceup": 7.0 * coef},
            "追込": {"pacedown": 7.5 * coef, "paceup": 8.0 * coef}
            }
        rand_itv_jdgnum = random.uniform(RST_NORMAL_LIMIT_COEFDICT[rst]["pacedown"], RST_NORMAL_LIMIT_COEFDICT[rst]["paceup"])            
        if itv_top < rand_itv_jdgnum:
            return True
        else:
            return False

    def jdg_stop_pacedown(self, is_actskls, dst, rst, itv_top):
        if is_actskls == True:
            return True
        else:
            coef = 0.0008 * (dst - 1000) + 1.0
            RST_NORMAL_LIMIT_COEFDICT = {
                "先行": {"pacedown": 3.0 * coef, "paceup": 5.0 * coef},
                "差し": {"pacedown": 6.5 * coef, "paceup": 7.0 * coef},
                "追込": {"pacedown": 7.5 * coef, "paceup": 8.0 * coef}
                }
            rand_itv_jdgnum = random.uniform(RST_NORMAL_LIMIT_COEFDICT[rst]["pacedown"], RST_NORMAL_LIMIT_COEFDICT[rst]["paceup"])            
            if itv_top < rand_itv_jdgnum:
                return True
            else:
                return False
