import pandas as pd
import json

# data = open(r'C:\Users\smithm7\PycharmProjects\sec_edgar\Lib\JSONFile000104746915001106.json')
#
# data = json.load(data)
#
# print("Datatype after deserialization : "
#       + str(type(data)))
#
# print(data)


with open(r'C:\Users\smithm7\PycharmProjects\sec_edgar\Lib\JSONFile000104746915001106.json', 'r') as file:
    df = pd.DataFrame.from_dict(json.load(file))

df.set_index(['@id'], inplace=True)

print(df.head())
