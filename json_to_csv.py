import glob
import json
import csv
import pandas as pd

fields = ["filename", "class", "fill"]
classes = ["glass","cup","plate"]

## use split = True if you want splitted output

def json_to_csv(split=False):
    df = []
    output_name = "csv_converted.csv"
    for fn in sorted(glob.glob("TDB_M/*.json")):
        f = open(fn)
        json_obj = json.load(f)
        for key in json_obj:
            dict_row = {"filename":json_obj[key]["filename"],"class":"null","fill":"null"}

            if len(json_obj[key]["regions"]) == 0:
                df.append(dict_row)

            else:
                temp_c = []
                temp_fill = []
                for r in json_obj[key]["regions"]:
                    if "Type" in json_obj[key]["regions"][r]["region_attributes"]:
                        c = json_obj[key]["regions"][r]["region_attributes"]["Type"].lower().strip()
                        if "Fill" in json_obj[key]["regions"][r]["region_attributes"]:
                            fill = json_obj[key]["regions"][r]["region_attributes"]["Fill"].lower().strip()
                            if fill in classes:
                                fill = 30
                    elif "type" in json_obj[key]["regions"][r]["region_attributes"]:
                        c = json_obj[key]["regions"][r]["region_attributes"]["type"].lower().strip()
                        if "fill" in json_obj[key]["regions"][r]["region_attributes"]:
                            fill = json_obj[key]["regions"][r]["region_attributes"]["fill"].lower().strip()
                            if fill in classes:
                                fill = 30
                    temp_c.append(c)
                    temp_fill.append(fill)
                    
                if (split):
                    dict_row["class"] = temp_c
                    dict_row["fill"] = temp_fill
                else:
                    dict_row["class"] = ";".join(temp_c)
                    dict_row["fill"] = ";".join(map(str, temp_fill))
                
                df.append(dict_row)
    
    df = pd.DataFrame(df)
    df = df[fields]
    df = df.drop_duplicates(subset=['filename'], keep='last')
#     print(df)
    
    if (split):
        df = df.set_index(['filename']).apply(pd.Series.explode).reset_index()
        output_name = output_name[:-4]+"_splitted.csv"
        print(output_name)
        print(df)
    
    df.to_csv(output_name,index=False,header=True, sep=",")
    

json_to_csv(True)
        
