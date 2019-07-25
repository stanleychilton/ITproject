import csv, os

files = os.listdir()
for x in range(0, len(files)):
    print(x+1, files[x])

i = int(input("please choose a csv file to read"))
chosenfile = files[i-1]

with open(chosenfile) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            row[0] = (row[0])[3:]
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            print(f'\t{row[0]} {row[1]} {row[2]} {row[3]}')
            line_count += 1
    print(f'Processed {line_count} lines.')