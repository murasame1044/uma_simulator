import math, random
import sys

from girl_and_course import Umagirl, Course
from setting_prm import VlcSetting, AclSetting, HtpSetting, show_init_prm_list
from revision_prm import VlcRev, AclRev, HtpRev
from setting_mode import Mode
from setting_slope import judge_slope
from prepare_race import StartTime, show_phase, calc_sct_border, select_inp_sct

from calcRevStatus import CalcRevStatus
from race_skls_list import skls_list

import numpy as np
import matplotlib.pyplot as plt

"""命名略語一覧

< 変数 >
coef: 係数(coefficient)
rev: 補正数(revision)
prob: 確率(probability)
prop: 適性(prosper)
bool: 条件正誤(bool)

< 関数 >
jdg: 判定(judge) => return Bool or int
calc: 計算(calculation) => return int or float
show: 値を示す

< ステータス >
spd: 速度(speed)
stm: スタミナ(stamina)
pwr: パワー(power)
gut: 根性(guts)
int: 賢さ(intelligence)
mtv: やる気(motivation)
prop: 適性(property)
psv_skls: パッシブスキル(passive-skills)

< コース >
plc: 会場(place)
grd: バ場(ground)
dst: 距離（distance)
rst: 脚質(runstyle)
wth: 天気(weather)
cnd: コンディション(condition)
ang: 角度(angle)
slp: 坂(slope)
    dwnslp: 下り坂 / upslp: 上り坂
gls: 芝(glass)
mud: ダート(mud)

< レース >
pst: 位置(position)
vlc: 速度(velocity)
acl: 加速度(accel)
htp: 体力(hitpoint)
prm: パラメータ(上記4種+mode) (parameter)
frm: フレーム(frame)
sct: セクション(section)
slp: 坂(slope)
act_skls: 有効スキル(activate-skills)
inp: 掛かり(inpacient)
rank: 順位
itv: 他のウマとの距離(interval)
   └ top, subtop, front, side, back
subrank: 同脚質の中の順位

"""

HORSE_BODY_SIZE = 2.5  # 1バ身[m]
HORSE_LANE = 1  # ウマ幅[m]
COURSE_WIDTH = 18  # コース幅[m]
FRMPERSEC = 0.0666  # 1frごとに計算

"""
    def lastspart(
        base_target_vlc_phase2start_frm, base_vlc, rev_spd, prop_dst, 
        dst, cur_pst, 
        is_inp, is_pacedown, is_dwnslp_aclmode, cur_vlc, grd, cnd, phase, rev_gut,
        cur_htp, rst
        ):

        PROP_DST_DICT = {"S": 1.05, "A": 1.00, "B": 0.9, "C":0.8, "D":0.6, "E":0.4, "F":0.2, "G":0.1}
        lastspart_target_vlc = (base_target_vlc_phase2start_frm + 0.01 * base_vlc) + 1.05 * math.sqrt(500.0 * rev_spd) * PROP_DST_DICT[prop_dst] * 0.002

        # 予想残り時間[s] を、60m地点までの残り距離とラストスパート目標速度から算出する
        predict_last_sec = ((dst-60) - cur_pst) / lastspart_target_vlc
        #  HP消費量/s
        htpsetting = HtpSetting()
        
        consumption_htp_presec = htpsetting.calc_consumption_htp_persec(is_inp, is_pacedown, is_dwnslp_aclmode, cur_vlc, base_vlc, grd, cnd, phase, rev_gut)
    
        if consumption_htp_presec * predict_last_sec > cur_htp:
            lastspart_startpoint = phase[2][0]  # phase2の開始と同時にラストスパート
            lastspart_startvlc = lastspart_target_vlc
        else:
            vlcset = VlcSetting()
            candidate_vlc_list = []
            while lastspart_target_vlc == vlcset.calc_base_target_vlc(base_vlc, rst, 2, rev_spd, prop_dst):
                lastspart_target_vlc -= 0.10
                predict_last_sec = ((dst-60) - cur_pst) / lastspart_target_vlc
                if consumption_htp_presec * predict_last_sec > cur_htp:
                    candidate_vlc_list.append(lastspart_target_vlc)
        
"""

# 他ウマとの相関関係
subrank = 0
class Interval:
    entry = 18
    subentry = 5

    def __init__(self, pst):
        self.pst = pst

    # 他のウマと自分の距離をsortで出力[entry:出走人数]
    def show_girls_interval(self, entry=entry, subentry=subentry, sub=False):
        girls_interval = [0] + [random.uniform(-20.0+self.pst, 20.0+self.pst) - self.pst for i in range(entry-1)]
        girls_subinterval = [0] + [random.uniform(-20.0+self.pst, 20.0+self.pst) - self.pst for i in range(subentry-1)]    

        girls_interval.sort()
        girls_subinterval.sort()

        return girls_interval if sub==False else girls_subinterval

    def show_rank(self):
        return self.show_girls_interval().index(0)
    def show_top(self):
        return self.show_girls_interval()[0]
    def show_subtop(self):
        return self.show_girls_interval(sub=True)[0]
    def show_frontback(self, back=False):
        rank = self.show_rank()
        if back == False:
            return self.show_girls_interval()[rank-1] if rank != 0 else 0
        if back == True:
            return self.show_girls_interval()[rank+1] if rank == self.entry else 0

class Lane:
    def __init__(self):
        pass

    def calc_lane_dst(self, start_lane):
        return (start_lane - 1) * HORSE_LANE

    min = 0
    max = random.choice([1.1, 1.2, 1.3, 1.4, 1.5])

class Sight:
    def __init__(self, pst):
        self.pst = pst
    
    def calc_sight_side(self, pst):
        interval = Interval(pst)
        sight_distance = 20
        front_distance = interval.front
        sight_side = (11.5 * front_distance / sight_distance + 2) / 2
        return sight_side

    
    def judge_overtake(self, pst):
        velocity_difference = 1
        interval = Interval(pst)
        def check_interval_front():
            return True if 1 <= interval.front <= 20 else False
        def check_current_velocity_difference():
            return True if velocity_difference >= 0 else False
        def check_predict_overtake_lt15sec():
            return True if interval.front / velocity_difference <= 15 else False
        def check_target_velocity_difference(target_vlc):
            enemy_target_vlc = 18
            return True if target_vlc > enemy_target_vlc else False
        
        if check_interval_front() and check_current_velocity_difference() and check_predict_overtake_lt15sec() and check_target_velocity_difference():
            return True
        else:
            return False

class Skl:
    def __init__(self):
        pass

    def calc_activation_prob(self, itl, mtv):
        MTV_COEFDICT = {"絶好調":1.04, "好調":1.02, "普通":1.0, "不調":0.98, "絶不調": 0.96}
        return max(20, 100-9000/(itl * MTV_COEFDICT[mtv]))
    
    def show_active_skls(self, skls_list, itl, mtv):
        for skill in skls_list:
            act_skls = []
            prob = self.calc_activation_prob(itl, mtv)
            if random.random() < prob:
                act_skls.append(skill)
            return act_skls
    
    def calc_activate_time(skl_activate_time, dst):
        return skl_activate_time * dst / 1000
    
    def calc_cooldown_time(skl_cooldown_time, dst):
        return skl_cooldown_time * dst / 1000


uma1 = Umagirl("スピード型", [861,818,586,458,456], ["A","A","A"], "逃げ", "普通", [60,0,40,60,0])
uma2 = Umagirl("スタミナ型", [809,941,584,435,418], ["A","A","A"], "逃げ", "普通", [0,60,60,0,0])


def main(uma=uma1):

    course = Course("阪神", "gls", 3200, "不良")

    spd = uma.spd  # スピード
    stm = uma.stamina  # スタミナ
    pwr = uma.power  # パワー
    gut = uma.guts  # 根性
    itl = uma.intel  # 賢さ
    mtv = uma.motivate  # やる気
    rst = uma.runstyle  # 脚質
    prop_rst = uma.prop_runstyle  # 脚質適正
    prop_dst = uma.prop_distance  # 距離適正
    prop_grd = uma.prop_ground  # バ場適正

    plc = course.place  # レース場所
    grd = course.ground  # 地面 (glass / mud)
    dst = course.distance  # 距離
    cnd = course.condition  # バ場状態

    breeding_bool = False  # 育成モード判定
    psv_skl = uma.psv_skl  # パッシブスキル(len=5)


    rev = CalcRevStatus()
    rev_spd = rev.calc_rev_spd(spd, stm, pwr, gut, itl, mtv, psv_skl, plc, grd, cnd, dst, breeding_bool)
    rev_stm = rev.calc_rev_stm(stm, mtv, psv_skl, breeding_bool)
    rev_pwr = rev.calc_rev_pwr(pwr, mtv, cnd, psv_skl, breeding_bool)
    rev_gut = rev.calc_rev_gut(gut, mtv, psv_skl, breeding_bool)
    rev_itl = rev.calc_rev_itl(itl, mtv, prop_rst, psv_skl, breeding_bool)



    ### ----- レース開始前 -----
    vlcset = VlcSetting()
    aclset = AclSetting()
    htpset = HtpSetting()
    vlcrev = VlcRev()
    aclrev = AclRev()
    htprev = HtpRev()
    race_skl = Skl()

    ### ----- レース試行開始 -----
    frm_record_list = []
    shikoukaisuu = 20
    for tryrace in range(shikoukaisuu):

        # 発動スキル選定
        active_skls = race_skl.show_active_skls(skls_list, itl, mtv)  # 発動するスキルのlist

        # 掛かりセクション選定
        inp_sct = select_inp_sct(rev_itl)

        # スタート時間決定(0.000 - 0.100s)
        st = StartTime()
        act_skls_concent= []
        starttime = st.calc_starttime(act_skls_concent)
        is_startdash_num = st.jdg_startdash(starttime)  # -1: 出遅れ / 0: 通常 / 1: スタートダッシュ
        is_startdash = True if is_startdash_num == 1 else False
    

        # 初期パラメータ
        init_pst, init_vlc, init_acl = 0, 3.0, 24.0
        init_htp = htpset.calc_init_htp(rst, rev_stm, dst)
        
        init_prm_list = [init_pst, init_vlc, init_acl, init_htp, "normal"]
        prm_list = [init_prm_list]
        last_pst, last_vlc, last_acl, last_htp, last_mode = init_prm_list


        # 初期化いろいろ
        is_startaccel = True
        is_splinting = False
        flagfrm = -100  # 存在しないフレーム(type=int)
        frm = 0

        # 設定速度
        base_vlc = vlcset.calc_base_vlc(dst)
        limit_vlc = vlcset.calc_limit_vlc(base_vlc)
        blocked_limit_vlc = vlcset.calc_blocked_limit_vlc(itv_front=0, front_vlc=0)
        min_vlc = vlcset.calc_min_vlc(rev_gut, base_vlc)

        if False:
            print("\n"+f"基本速度:{base_vlc}, 制限速度:{limit_vlc}, 最低速度:{min_vlc}")
            print(f"掛かりsection:{inp_sct}")
            print("\n"+f"スタート時間:{round(starttime,4)}[s]")



        
        ### ----- セクション開始 ----- (ex. section 1)
        for sct in range(1, 25):
            phase = show_phase(sct)
            
            # 掛かりsectionかの判定
            is_inp_sct = True if inp_sct == sct else False

            # sectionの始点と終点[m]
            sct_pst_border_dict = dict(start = calc_sct_border(dst)[sct-1], finish = calc_sct_border(dst)[sct]) 

            if False: print(f"< phase {phase} >"+"\n"+f"< section {sct} > : {sct_pst_border_dict['start']}m - {sct_pst_border_dict['finish']}m")

            ### ----- フレーム開始 -----
            
            while sct_pst_border_dict["start"] <= prm_list[frm][0] <= sct_pst_border_dict["finish"]:
                frm += 1

                """
                def calc_prm(pst, vlc, acl, htp):
                    tmp_pst = pst + vlc * FRMPERSEC + acl * (FRMPERSEC)**2
                    tmp_vlc = vlc + acl * FRMPERSEC
                    tmp_acl = acl
                    tmp_htp= htp
                    return (tmp_pst, tmp_vlc, tmp_acl, tmp_htp)
                """
                """
                target_acl = aclrev.calc_accel(rev_pwr, rst, phase, prop_grd, prop_dst, act_skls, is_startaccel)  # 仮加速度計算
                """
                """
                tmp_pst, tmp_vlc, tmp_acl, tmp_htp = calc_prm(last_pst, last_vlc, target_acl, last_htp)
                    -> 基礎値は必要ない？ 前frmのprmを引き継げば問題ないか？
                """
                
                tmp_pst, tmp_vlc, tmp_acl, tmp_htp, tmp_mode = last_pst, last_vlc, last_acl, last_htp, last_mode

                # 坂の有無
                slope_type_num = 0
                is_upslp = True if slope_type_num == 1 else False
                is_dnslp = True if slope_type_num == -1 else False

                # boolステータスチェック
                is_inp = is_inp_sct
                is_pacedown = True if tmp_mode == "pacedown" else False
                is_dwnslp_aclmode = False
                is_startdash = is_startdash
            
                # スキルの発動状態
                is_vlcskl_activated = False
                is_aclskl_activated = False

                # ポジションキープモード
                moderev = Mode()
                itv = Interval(last_pst)
                tmp_mode = moderev.show_mode(dst, rst, subrank, itv.show_top(), is_inp, itv.show_frontback(back=True), rev_itl, is_vlcskl_activated)  # 現在のモード

                # 下り坂加速モード
                ang = 0
                is_downslope_aclmode = False
                

                base_target_vlc = vlcset.calc_base_target_vlc(sct, base_vlc, rst, phase, rev_spd, rev_itl, prop_dst)
                target_vlc = vlcset.calc_target_vlc(rst, base_target_vlc, tmp_mode, is_upslp, is_dnslp, is_downslope_aclmode, ang, rev_pwr)

                
                rev_splinting = vlcrev.calc_gut_lastsplinting(rev_gut) if is_splinting else 0
                
                # スキル補正
                act_skls = race_skl.show_active_skls(skls_list, itl, mtv)
                rev_act_skls = dict(vlc=0, acl=0, htp=0)
                sklrev_vlc = tmp_vlc + rev_act_skls["vlc"]
                sklrev_acl = tmp_acl + rev_act_skls["acl"]
                sklrev_htp = tmp_htp + rev_act_skls["htp"]

                # 実際のパラメータ
                abs_target_acl = aclrev.calc_accel(rev_pwr, rst, phase, prop_grd, prop_dst, act_skls, is_startaccel) # 仮加速度計算
                target_acl = abs_target_acl if tmp_vlc <= target_vlc else abs_target_acl*(-1)
                current_acl = target_acl + rev_act_skls["acl"]

                current_vlc = tmp_vlc + current_acl * FRMPERSEC + rev_act_skls["vlc"] + rev_splinting

                # スタート時の加速度上昇判定・最低速度保証等
                if current_vlc > limit_vlc:
                    if is_startaccel == True:
                        current_vlc = limit_vlc
                        is_startaccel = False
                        flagfrm = frm

                if frm == flagfrm+1:
                    current_vlc = min_vlc

                if current_vlc > target_vlc and tmp_htp <= 0:
                    current_vlc = target_vlc


                current_pst = tmp_pst + current_vlc * FRMPERSEC + current_acl * (FRMPERSEC)**2   # tmp_pst = pst + vlc * FRMPERSEC + acl * (FRMPERSEC)**2

                htp_consumption = htprev.calc_consumption_htp_persec(is_inp, is_pacedown, is_dwnslp_aclmode, current_vlc, base_vlc, grd, cnd, phase, rev_gut)
                current_htp = max(tmp_htp - htp_consumption, 0)
                current_mode = tmp_mode

                if False:
                    print("\n"+f"{itv.show_rank()}位, 先頭と{abs(round(itv.show_top(), 4))}[m]差")


                if False: 
                    print("\n"+f"目標速度: {round(target_vlc, 4)}", f"体力減少: {round(htp_consumption,4)}/{init_htp}")
                    print(f"frame: {frm}({round(frm * FRMPERSEC + starttime, 3)}[s])", f"{round(current_pst,4)}[m]", f"{round(current_vlc,4)}[m/s]", f"{round(current_acl,4)}[m/s^2]", f"HP:{round(current_htp,4)}", f"mode:{current_mode}", sep="\t")
                prm_list.append([current_pst, current_vlc, current_acl, current_htp, current_mode])
            
                last_pst, last_vlc, last_acl, last_htp, last_mode = current_pst, current_vlc, current_acl, current_htp, current_mode
        frm_record_list.append(len(prm_list))

    for i in range(len(frm_record_list)):
        if False: print(f"{i+1}回目", f"{round(frm_record_list[i] * FRMPERSEC, 4)}[s]", sep="\t")
    if tryrace == shikoukaisuu-1: print(f"{uma.name}_average: {np.average(frm_record_list)}")
    rounded_prm_list = []
    for prms in prm_list:
        rounded_prm_list.append([round(prms[n], 3) for n in range(len(prms)-1)])
    prm_numpylist = np.array(rounded_prm_list)
    pst_list = prm_numpylist[:, 0]
    vlc_list = prm_numpylist[:, 1]
    acl_list = prm_numpylist[:, 2]
    htp_list = prm_numpylist[:, 3]
    frm_list = range(len(prm_list))


    fig = plt.figure() # Figureオブジェクトを作成
    ax_pst = fig.add_subplot(111) # figに属するAxesオブジェクトを作成
    ax_vlc = ax_pst.twinx()
    # ax_acl = ax_vlc.twinx()
    ax_htp = ax_pst.twinx()

    ax_pst.plot(frm_list, pst_list, label='position', color="orange")
    ax_vlc.plot(frm_list, vlc_list, label='velolcity', color="green")
    # ax_acl.plot(frm_list, acl_list, label='accel', color="pink") -> 必要なし
    ax_htp.plot(frm_list, htp_list, label='hitpoint', color="blue")

    ax_pst.set_xlim(-20, len(frm_list)+20)
    ax_vlc.set_ylim(min_vlc-2.0, min_vlc*1.5)
    ax_vlc.spines["right"].set_position(('outward', 40.0))

    plt.legend()
    plt.show()


    """
    import matplotlib.pyplot as plt
    import numpy as np

    # データ生成
    x = np.linspace(0, 10, 100)
    y = x + np.random.randn(100) 

    # Figureの初期化
    fig = plt.figure(figsize=(12, 8)) #...1

    # Figure内にAxesを追加()
    ax = fig.add_subplot(111) #...2
    ax.plot(x, y, label="test") #...3

    # 凡例の表示
    plt.legend()

    # プロット表示(設定の反映)
    plt.show()
    """

if __name__ == "__main__":
    main(uma1)
    main(uma2)

    sys.exit()