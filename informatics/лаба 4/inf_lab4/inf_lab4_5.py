import json
import csv


with open('D:\ITMO\informatics\лаба 4\schedule.json', 'r', encoding='utf-8') as file:
    schedule = json.load(file)

rows = []
for day in schedule:
    for lesson_key in schedule[day]:
        lesson = schedule[day][lesson_key]

        row = {
            'day_of_week': day,
            'lesson_number': lesson_key,
            'time_from': lesson['time']['from'],
            'time_to': lesson['time']['to'],
            'weeks': ','.join(map(str, lesson['time']['week'])),
            'classroom': lesson['location']['classroom'],
            'campus': lesson['location']['campus'],
            'title': lesson['title'],
            'teacher': lesson['teacher'],
            'lesson-format': lesson['lesson-format']
        }
        rows.append(row)

headers = ['day_of_week', 'lesson_number', 'time_from', 'time_to', 'weeks',
           'classroom', 'campus', 'title', 'teacher', 'lesson-format']

with open('D:\ITMO\informatics\лаба 4\out5.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    writer.writerows(rows)
