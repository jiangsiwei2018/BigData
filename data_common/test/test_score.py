# coding=utf-8

# 第一题
score = [
    ['std_id', 'math', 'physics', 'chemistry', 'program', 'english', 'avg'],
    [201, 65, 58, 75, 80, 80, 72],
    [202, 92, 66, 0, 0, 0, 0],
    [203, 0, 0, 0, 0, 0, 0],
    [204, 0, 0, 0, 0, 0, 0],
    [205, 0, 0, 0, 0, 0, 0],
    [206, 0, 0, 0, 0, 0, 0],
    [207, 0, 0, 0, 0, 0, 0],
    [208, 0, 0, 0, 0, 0, 0],
    [209, 0, 0, 0, 0, 0, 0],
    [210, 0, 0, 0, 0, 0, 0],
    [211, 0, 0, 0, 0, 0, 0],
    [212, 0, 0, 0, 0, 0, 0],
    ['avg_all', 66, 0, 0, 0, 0, 0]
]

# 7.

for i in range(14):
    std_id = score[i][0]
    for j in range(7):
        std_score = score[i][j]
        if 1 <= i <= 12 and j != 0:
            print(f'score[{i}][{j}] {std_id} {std_score}')

for i in range(14):
    row = ''
    for j in range(7):
        cell = score[i][j]
        row += '%10s' % str(cell)
    print(row)
###########################################################
# 第二题
avg_score = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
for i in range(1, 12):
    std_id = score[i][0]
    std_score = score[i][1:6]
    std_avg = sum(std_score) / 5
    avg_score[0][i - 1] = std_id
    avg_score[1][i - 1] = std_avg

print(avg_score)
for j in range(11):
    print(f'{avg_score[0][j]}\t{avg_score[1][j]}')
###########################################################
# 第三题
course_avg_score = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]

for j in range(1, 6):
    course_avg_score[0][j - 1] = score[0][j]
    course_sum = 0
    for i in range(1, 13):
        course_sum += score[i][j]
    course_avg_score[1][j - 1] = course_sum /12
print(course_avg_score)

for j in range(5):
    print(f'{course_avg_score[0][j]}\t{course_avg_score[1][j]}')

###########################################################
# 第4题
mean_sum = 0
for j in range(5):
    mean_sum += course_avg_score[1][j]
# 平均值
mean = mean_sum / 5

import math
std_sum = 0
for j in range(5):
    err = course_avg_score[1][j] - mean
    std_sum += err * err
# 方差
var = std_sum / (5-1)
# 标准差
std_err = math.sqrt(var)
print(f'mean: {mean}\tvar: {var}\tstd_err: {std_err}')