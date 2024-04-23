import json

with open('../data/01.json', 'r') as f:
        data = json.load(f)

# print(type(data))

author_book = {}
week_data = {i: {} for i in range(1, 54)}
month_data = {i: {} for i in range(1, 13)}  
season_data = {i: {} for i in range(1, 5)}
year_data = {}
data = data["RECORDS"]

def daytoweek(month: int, day: int) -> int:
        month_day = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        cnt = 0
        for i in range(month - 1):
            cnt += month_day[i]
        cnt += day
        return cnt // 7 + 1
    

for obj in data:
    if "著者" not in obj or "图书书名" not in obj or "事件时间" not in obj or "事件类型" not in obj:
         continue
    author = obj["著者"]
    # print(author)
    book = obj["图书书名"]
    event_time = int(obj["事件时间"])
    event_type = obj["事件类型"]

    # print(event_type)

    if event_type != "借阅" and event_type != "续借（web端）" and event_type != "续借（pc端）":
        continue

    # print("at line 36")

    if author is None or book is None or event_time is None:
        continue
    
    # print("at line 41")

    if book not in author_book:
        author_book[book] = author
        # print("add book: ", book, " author: ", author)

    if book not in year_data:
        year_data[book] = 1
    else:   
        year_data[book] += 1
    
    month = (event_time // 100) % 100
    day = event_time % 100
    season = month // 4 + 1
    week = daytoweek(month, day)

    if book not in season_data[season]:
        season_data[season][book] = 1
    else:
        season_data[season][book] += 1

    if book not in month_data[month]:
        month_data[month][book] = 1
    else:
        month_data[month][book] += 1
    
    if book not in week_data[week]:
        week_data[week][book] = 1
    else:
        week_data[week][book] += 1

sorted_year_data = sorted(year_data.items(), key=lambda x: x[1], reverse=True)
sorted_april_data = sorted(season_data[4].items(), key=lambda x: x[1], reverse=True)
sorted_second_quarter_data = sorted(season_data[2].items(), key=lambda x: x[1], reverse=True)
sorted_week_data = sorted(week_data[17].items(), key=lambda x: x[1], reverse=True)
sorted_year_data = dict(sorted_year_data[: 5])
sorted_april_data = dict(sorted_april_data[: 5])
sorted_second_quarter_data = dict(sorted_second_quarter_data[: 5])
sorted_week_data = dict(sorted_week_data[: 5])

selected_author_book = {}
for book in sorted_year_data:
    selected_author_book[book] = author_book[book]

for book in sorted_april_data:
    selected_author_book[book] = author_book[book]

for book in sorted_second_quarter_data:
    selected_author_book[book] = author_book[book]

for book in sorted_week_data:
    selected_author_book[book] = author_book[book]

print(sorted_year_data)
print(sorted_april_data)
print(sorted_second_quarter_data)
print(sorted_week_data)

print(selected_author_book)
'''
Output:
    {'明朝那些事儿': 396, '三体': 205, '机器学习': 191, '红楼梦': 169, '数值分析': 168}
    {'福尔摩斯探案大全集': 30, '明朝那些事儿': 28, '神雕侠侣': 25, '三体': 24, '机器学习': 22}
    {'明朝那些事儿': 134, '机器学习': 60, '三体': 57, '卡拉马佐夫兄弟': 57, '天龙八部': 52}
    {'生物信息学': 16, '三体': 12, '明朝那些事儿': 11, '数值分析': 8, '人工智能': 7}
'''