class Umagirl:
    def __init__(self, name, status_list, prop_list, rst, mtv, passive_skl):
        self.name = name
        self.status_list = status_list
        self.spd, self.stamina, self.power, self.guts, self.intel = status_list[0], status_list[1], status_list[2], status_list[3], status_list[4]
        self.prop = prop_list
        self.prop_ground, self.prop_distance, self.prop_runstyle = prop_list[0], prop_list[1], prop_list[2]
        self.runstyle = rst
        self.motivate = mtv
        self.psv_skl = passive_skl

class Course:
    def __init__(self, place, ground, distance, condition):
        self.place = place
        self.ground =  ground
        self.distance = distance
        self.condition = condition
