import pandas as pd
import xlsxwriter
import re
import csv


def split(txt, seps):
    default_sep = seps[0]

    # we skip seps[0] because that's the default separator
    for sep in seps[1:]:
        txt = txt.replace(sep, default_sep)
    return [i.strip() for i in txt.split(default_sep)]

row = 0
col = 0

xdf = pd.read_excel("inputfile.xlsx", engine="openpyxl", keep_default_na=False)
xdf.dropna()
xdf.set_index('Spalte1', inplace=True)


df = pd.read_csv("inputfile.csv", keep_default_na=False, skip_blank_lines=True)
names = pd.read_csv("inputfile.csv", sep=',', parse_dates=[0],
                    usecols=[0], keep_default_na=False)


names.dropna()
items = names.items()

# replace all of commas with spaces
# so we can reformat our file
second_list = []
with open("inputfile.csv", newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        row = [x.replace(',', ' ') for x in row if x]
        second_list.append(row)

final_list = []
regex = "(([0]?[1-9]|[1|2][0-9]|[3][0|1])[./-]([0]?[1-9]|[1][0-2])[./-]([0-9]{4}|[0-9]{2}))"

# go through our reformated second list
# replace any mispelled dates to convert to correct format
# find our dates through the created regex 
# re-format for dates and add to final list
for i in range(len(second_list)):
    row = second_list[i]
    if i > 0:
        new_row = []
        for item in row:
            item = item.replace("..", ".")
            item = item.replace(":", ".")
            m = re.findall(regex, item)
            if m:
                date_list = [i[0] for i in m]

                for date in date_list:
                    new_row.append(date)
        final_list.append(new_row)


xdf['merged_column'] = xdf[xdf.columns[1:]].apply(
    lambda x: ','.join(x.dropna().astype(str)), axis=1
)
xdf['merged_column'] = xdf.apply(lambda x: x.str.replace(',', ''))
xdf['merged_column'] = xdf.apply(lambda x: x.str.replace('..', '.'))
xdf['merged_column'] = xdf.apply(lambda x: x.str.replace(':', '.'))
xdf = xdf.drop(xdf.columns[0:8], axis=1)

df_listoflists = []
for index in range(len(xdf.index)):
    date_row = final_list[index]
    full_list = xdf['merged_column'][index]
    new_row = []
    if len(date_row) > 0:
        new_row = split(full_list, date_row)
        new_row = new_row[1:]

        for i in range(len(new_row)):
            date = date_row[i]
            date = date.replace('/', '.')
            date = date.replace('-', '.')
            item = [new_row[i]]
            item.insert(0, date)

            new_row[i] = item
    df_listoflists.append(new_row)

# fix names, in case there is no first name add unknown
# and insert them to the list we are going to return
# add corresponding date and prescription to the name
df_final_list = []
for i in range(len(xdf.index)):
    name = xdf.index[i]
    name = name.split()
    if len(name) > 1:
        first_name = name[1]
    else:
        first_name = "unknown"
    last_name = name[0]

    row = df_listoflists[i]

    for item in row:
        item.insert(0, first_name)
        item.insert(0, last_name)

        df_final_list.append(item)


df = pd.DataFrame(df_final_list, columns = ['Last Name', 'First Name', 'Date', 'Prescription'])


df.to_excel("output.xlsx")
