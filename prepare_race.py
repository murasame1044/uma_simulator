import math, random


class StartTime:
    def __init__(self):
        pass

    def calc_starttime(self, act_skls):
        starttime = random.randint(1, 100) * 0.001
        if "コンセントレーション" in act_skls:
            return starttime * 0.4
        elif "集中力" in act_skls:
            return starttime * 0.9
        else:
            return starttime
    
    #  return 1:スコア加算, 0:通常, -1:出遅れ
    def jdg_startdash(self, starttime):
        if starttime < 0.020:
            return 1
        elif starttime > 0.080:
            return -1
        else:
            return 0



def calc_sct_border(dst): 
    sect_border_list = [0]
    for i in range(24):
        finish = (i+1)/24 * dst
        sect_border_list.append(finish)
    return sect_border_list


def show_phase(sct):
    if sct <= 4:
        return 0
    elif sct <= 16:
        return 1
    elif sct <= 20:
        return 2
    else:
        return 3


def select_inp_sct(rev_itl):
    prob = (6.5 * math.log10(0.1 * rev_itl+ 1.0)**2) / 100
    if random.random() < prob:
        return random.randint(2,9)
    else:
        return None