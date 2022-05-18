import math

SLOPE_COURSEDATA_DICT = {
    # "place+dst": ((start, finish, up_or_dn),(start, finish, up[+1]_or_dn[-1]), ...)
    "中山":{ 
        "1200": ((0, 0, -1), (1030, 1030, 1), (1170, 1170, -1))

    }
    }

class Slp:
    def __init__(self):
        pass

    def calc_slp_per(self, ang):
        return math.tan(ang) * 100




def judge_slope(pst, plc, dst):  # slope_placesは((start=a, finish=b, up_or_dn= 1 or -1), ...)の形式で坂の始点と終点が指定されている
    slope_pst_dict = SLOPE_COURSEDATA_DICT[plc][dst]

    for i in len(slope_pst_dict):
        if pst - slope_pst_dict[i]["start"] >= 0 and pst - slope_pst_dict[i]["finish"] <= 0: # start ~ finish の間に pst が存在
            return slope_pst_dict["up_or_dn"]
        break

    return 0

