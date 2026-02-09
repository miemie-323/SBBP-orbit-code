# https://rhodesmill.org/skyfield/earth-satellites.html
from skyfield.api import EarthSatellite, load
from skyfield.api import wgs84
from skyfield.api import EarthSatellite, load
from skyfield.iokit import parse_tle_file
from datetime import datetime, timedelta
import math
import pandas as pd  # 引入 pandas 用于读取 Excel 文件
from sko.GA import GA
import time  # 添加时间模块


def is_nan(num):
    return math.isnan(num)

excel_data = pd.read_excel('4338-1107-stkcompute.xlsx', header=None)
excel_data_next = pd.read_excel('4338-1108-stkcompute.xlsx', header=None)

ts = load.timescale()
bluffton = wgs84.latlon(32.061667, 118.777778)

start_time = datetime.strptime("2024-11-08 10:01:00", "%Y-%m-%d %H:%M:%S")  # 设定起始时间
end_time = start_time + timedelta(minutes=10)
time_step = timedelta(milliseconds=1000)

def error_analyze(bstar):

    current_time = start_time
    # 初始化误差变量
    az_degrees_error = 0.0
    alt_degrees_error = 0.0
    az_degrees_error_next = 0.0
    alt_degrees_error_next = 0.0

    row_index = 0

    bstar = round(bstar[0])

    file_path = "4338-qi-1106.txt"
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    line2 = lines[1]
    lines[1] = line2[:54] + str(bstar) + line2[59:]
    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines(lines)

    while current_time <= end_time:
        current_time += time_step

        t = ts.utc(current_time.year, current_time.month, current_time.day,
                   current_time.hour, current_time.minute,
                   current_time.second + current_time.microsecond / 1_000_000)

        strTime = (f"{current_time.year}-"
                   f"{current_time.month:02d}-"
                   f"{current_time.day:02d} "
                   f"{(current_time.hour + 8):02d}:"
                   f"{current_time.minute:02d}:"
                   f"{current_time.second + current_time.microsecond / 1_000_000:06.3f}")

        listID = []

        with open('4338-qi-1106.txt', 'r') as file:
            while True:
                try:
                    lines = iter(file)
                    line0 = next(lines)
                    line1 = next(lines)
                    line2 = next(lines)
                    result = line2.split(" ")
                    satellite = EarthSatellite(line1, line2, result[1], ts)

                    difference = satellite - bluffton
                    topocentric = difference.at(t)
                    alt, az, distance = topocentric.altaz()
                    listID.append(str(result[1]))
                    listID.append(str(line1))
                    listID.append(str(line2))

                except StopIteration:
                    break

        startms_time = current_time
        endms_time = startms_time + timedelta(seconds=1)
        timems_step = timedelta(milliseconds=100)
        currentms_time = startms_time

        while currentms_time < endms_time:
            currentms_time += timems_step

            tms = ts.utc(currentms_time.year, currentms_time.month, currentms_time.day,
                         currentms_time.hour, currentms_time.minute,
                         currentms_time.second + currentms_time.microsecond / 1_000_000)
            strmsTime = (f"{currentms_time.year}-"
                         f"{currentms_time.month:02d}-"
                         f"{currentms_time.day:02d} "
                         f"{(currentms_time.hour + 8):02d}:"
                         f"{currentms_time.minute:02d}:"
                         f"{currentms_time.second + currentms_time.microsecond / 1_000_000:06.3f}") #将 currentms_time 格式化为字符串，便于存储和后续使用。
            list = [strmsTime]

            for i in range(0, len(listID), 3):
                sub_list = listID[i:i + 3]
                line1 = sub_list[1]
                line2 = sub_list[2]
                satellite = EarthSatellite(line1, line2, sub_list[0], ts)
                difference = satellite - bluffton
                topocentric = difference.at(tms)
                alt, az, distance = topocentric.altaz()

                list.extend([str(sub_list[0]), str(az.degrees), str(alt.degrees)]) #******
                resultLines = ','.join(list)
            actual_az = excel_data.iloc[row_index, 1]
            actual_alt = excel_data.iloc[row_index, 2]
            actual_az_next = excel_data_next.iloc[row_index, 1]
            actual_alt_next = excel_data_next.iloc[row_index, 2]

            az_error = az.degrees - actual_az
            alt_error = alt.degrees - actual_alt
            az_error_next = az.degrees - actual_az_next
            alt_error_next = alt.degrees - actual_alt_next

            if abs(az_error) > 300:
                az_error = 360.0 - abs(az_error)
            if abs(az_error_next) > 300:
                az_error_next = 360.0 - abs(az_error_next)

            print(resultLines)
            az_degrees_error += az_error  # 1107总方位角误差
            alt_degrees_error += alt_error  # 总高度角误差
            az_degrees_error_next += az_error_next  # 1108总方位角误差
            alt_degrees_error_next += alt_error_next  # 总高度角误差

            row_index += 1

    total_error = az_degrees_error + alt_degrees_error   #当前时刻的总误差，方位角误差和俯仰角误差相加。
    total_error_next = az_degrees_error_next + alt_degrees_error_next #下一个时刻的总误差，将下一个时刻的方位角误差和俯仰角误差相加。
    # print(az_degrees_error)
    # print(alt_degrees_error)
    print(az_degrees_error_next)
    print(alt_degrees_error_next)
    print("\n")

    return az_degrees_error, alt_degrees_error, total_error, total_error_next


# def opt_target(po):
#     az_degrees_error, alt_degrees_error, total_error, total_error_next = error_analyze(po)
#     return -total_error
#
#
# ga = GA(func=opt_target, n_dim=1, size_pop=4, max_iter=2000, prob_mut=0.05,
#         lb=[11000], ub=[16000], precision=1e-5)
#
# best_start_end, max_gsnr, best_x, best_y = ga.run()
# print('best_x:', best_x, '\n', 'best_y:', best_y)
# print('best_start_end:', best_start_end, '\n', 'max_gsnr:', max_gsnr)


error_analyze([14167])
#error_analyze([15818])
