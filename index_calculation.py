import metpy.calc as mpcalc
from  metpy.units import units 

class Grade:
    def __init__(self):
        self.apparent_temp_grading = {5: (25, 27),
            4: (24, 28),
            3: (23, 29),
            2: (22, 30),
            1: (21, 31),
            0: (20, 32),
            -1: (19, 33),
            -2: (18, 34)}
        
        self.max_temp_grading = (22, 32)

    def grade_apparent_temp(self, apparent_temperature):
        for key, value in self.apparent_temp_grading.items():
            print(f"AT:{apparent_temperature},key:{key},value:{value}")
            low, high = value
            if (low <= apparent_temperature <= high):
                return key
        else:
            return -3
    
    def grade_max_temp(self, max_temp):
        low, high = self.max_temp_grading 
        if low < max_temp < high:
            return 5
        else:
            return 1
        
    def grade_relative_humidity(self, rel_hum):
        if 40 <= rel_hum <= 60:
            return 5
        elif 30 <= rel_hum < 40 or 60 < rel_hum <= 65:
            return 3
        else:
            return 1
    
    def grade_wind_speed(self, sfc_wind):
        if 1.5 < sfc_wind < 4:
            return 5
        elif sfc_wind < 10:
            return 3
        else:
            return 1

def calculate_holiday_index_simple(temp):
    print(temp)
    holiday_index = 0
    if (temp > 25) & (temp < 31):
        holiday_index = 1
    return holiday_index


def calculate_comfort_index_summer(tasmax, tas, rel_hum, sfc_wind):

    grader = Grade()
    # HI = mpcalc.heat_index(tas*units.degC, humidity*units.percent)
    
    DAT = mpcalc.apparent_temperature(tasmax * units.degC, rel_hum*units.percent, sfc_wind*units('m/s'),
                                     mask_undefined=False).magnitude
    
    MAT = mpcalc.apparent_temperature(tas * units.degC, rel_hum*units.percent, sfc_wind*units('m/s'),
                                     mask_undefined=False).magnitude

    DAT_grade = grader.grade_apparent_temp(DAT)
    MAT_grade = grader.grade_apparent_temp(MAT)
    MT_grade = grader.grade_max_temp(tasmax)
    RH_grade = grader.grade_relative_humidity(rel_hum)
    WS_grade = grader.grade_wind_speed(sfc_wind)
    print(DAT_grade, MAT_grade, MT_grade, RH_grade, WS_grade)
    comfort_index = 2*((4 * DAT_grade) + (MAT_grade) + (2*MT_grade) + (2*RH_grade) + WS_grade)
    
    return comfort_index

