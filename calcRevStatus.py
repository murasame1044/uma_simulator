

class CalcRevStatus:
    def __init__(self):
        pass

    def calc_rev_spd(self, spd, stm, pwr, gut, itl, mtv, psv_skl, plc, grd, cnd, dst, breeding_bool=False):    
        GRD_REVDICT= {"良": 0, "稍重": 0, "重": 0, "不良": -50}
        MTV_COEFDICT = {"絶好調":1.04, "好調":1.02, "普通":1.0, "不調":0.98, "絶不調": 0.96}
        BREEDING_REVDICT = {True: 400, False: 0}

        def calc_course_coef(plc=plc, grd=grd, dst=dst, spd=spd, stm=stm, pwr=pwr, gut=gut, itl=itl):
            COURSE_DICT = {
        "札幌":{
            "gls":{
                2000: (pwr, None),
                2600: (stm, None)
            },
            "mud":{
                1700: (spd, None)
            }
        },
        "函館":{
            "gls":{
                1800: (pwr, None),
                2000: (spd, None),
                2600: (stm, None)
            },
            "mud":{
                2400: (stm, None)
            }
        },
        "新潟":{
            "gls":{
                1000: (pwr, None),
                1800: (pwr, None),
                2000: (stm, pwr),
                2200: (spd, None)
            },
            "mud":{
                1800: (itl, None)
            }
        },
        "福島":{
            "gls":{
                1800: (stm, None),
                2000: (stm, None)
            },
            "mud":{
                1700: (pwr, None),
                2400: (stm, None)
            }
        },
        "中山":{
            "gls":{
                1600: (pwr, None),
                2000: (spd, None),
                2200: (stm, gut),
                2500: (stm, gut),
                3600: (stm, None)
            },
            "mud":{
                1200: (pwr, None),
                1800: (pwr, None),
                2400: (stm, None)
            }
        },
        "東京":{
            "gls":{
                1400: (stm, pwr),
                1600: (stm, gut),
                1800: (spd, None),
                2300: (pwr, None),
                2500: (stm, None)
            },
            "mud":{
                1300: (spd, None),
                1400: (stm, None),
                1600: (spd, stm),
                2400: (stm, None)
            }
        },
        "中京":{
            "gls":{
                1600: (spd, None),
                2200: (stm, None)
            },
            "mud":{
                1800: (stm, None)
            }
        },
        "京都":{
            "gls":{
                1600: (spd, None),
                2000: (pwr, None),
                2200: (spd, None),
                2400: (pwr, None),
                3000: (pwr, itl)
            },
            "mud":{
            }
        },
        "阪神":{
            "gls":{
                1600: (pwr, None),
                1800: (pwr, None),
                2000: (gut, None),
                2200: (spd, None),
                2400: (pwr, None),
                3000: (pwr, None)
            },
            "mud":{
                2000: (stm, pwr)
            }
        },
        "小倉":{
            "gls":{
                1200: (spd, None),
                1800: (pwr, None),
                2000: (pwr, None),
                2600: (stm, None)
            },
            "mud":{
                1000: (spd, None)
            }
        },
        }
            if COURSE_DICT[plc][grd].get(dst):
                bonus_status1 = COURSE_DICT[plc][grd].get(dst)[0]
                bonus_status2 = COURSE_DICT[plc][grd].get(dst)[1]
            else:
                bonus_status1 = None
                bonus_status2 = None

            def show_selected_status(selected_status):
                tmp_coef_bonus_speed = 0
                if selected_status != None:
                    if selected_status > 1000:
                        tmp_coef_bonus_speed += 0.20
                    elif selected_status > 900:
                        tmp_coef_bonus_speed += 0.15
                    elif selected_status > 600:
                        tmp_coef_bonus_speed += 0.10
                    elif selected_status > 300:
                        tmp_coef_bonus_speed += 0.05
                    return tmp_coef_bonus_speed
                else:
                    return 0

            if bonus_status1 and bonus_status2:
                coef_speed_coursebonus = 1 + show_selected_status(bonus_status1)/2 + show_selected_status(bonus_status2)/2
            else:
                coef_speed_coursebonus = 1 + show_selected_status(bonus_status1) + show_selected_status(bonus_status2)

            return coef_speed_coursebonus    
        course_coef = calc_course_coef()

        return spd * MTV_COEFDICT[mtv] * course_coef + GRD_REVDICT[cnd] + BREEDING_REVDICT[breeding_bool] + psv_skl[0]

    def calc_rev_stm(self, stm, mtv, psv_skl, breeding_bool=False):
        MTV_COEFDICT = {"絶好調":1.04, "好調":1.02, "普通":1.0, "不調":0.98, "絶不調": 0.96}
        BREEDING_REVDICT = {True: 400, False: 0}

        return stm * MTV_COEFDICT[mtv] + BREEDING_REVDICT[breeding_bool] + psv_skl[1]

    def calc_rev_pwr(self, pwr, mtv, cnd, psv_skl, breeding_bool=False):
        MTV_COEFDICT = {"絶好調":1.04, "好調":1.02, "普通":1.0, "不調":0.98, "絶不調": 0.96}
        GRD_REVDICT= {"良": 0, "稍重": -50, "重": -50, "不良": -50}
        BREEDING_REVDICT = {True: 400, False: 0}

        return pwr * MTV_COEFDICT[mtv] + GRD_REVDICT[cnd] + BREEDING_REVDICT[breeding_bool] + psv_skl[2]

    def calc_rev_gut(self, gut, mtv, psv_skl, breeding_bool=False):
        MTV_COEFDICT = {"絶好調":1.04, "好調":1.02, "普通":1.0, "不調":0.98, "絶不調": 0.96}
        BREEDING_REVDICT = {True: 400, False: 0}
    
        return gut * MTV_COEFDICT[mtv] + BREEDING_REVDICT[breeding_bool] + psv_skl[3]

    def calc_rev_itl(self, itl, mtv, rank_rst, psv_skl, breeding_bool=False):
        MTV_COEFDICT = {"絶好調":1.04, "好調":1.02, "普通":1.0, "不調":0.98, "絶不調": 0.96}
        RANK_RST_COEFDICT= {"S":1.1, "A":1.0, "B":0.85, "C":0.75, "D":0.6, "E":0.4, "F":0.2, "G":0.1}
        BREEDING_REVDICT = {True: 400, False: 0}
    
        return itl * MTV_COEFDICT[mtv] * RANK_RST_COEFDICT[rank_rst] + + BREEDING_REVDICT[breeding_bool] + psv_skl[3]

