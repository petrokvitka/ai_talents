import pandas as pd
import glob
import json
import os

fields = ["filename", "class", "fill", "x", "y", "width", "height"]
classes = ["glass", "cup", "plate"]
acceptable_fills = ["0", "30", "100"]

def json_to_csv(output_name, input_dir):
    df = {}

    for fn in sorted(glob.glob(os.path.join(input_dir, "*.json"))):
        f = open(fn)
        json_obj = json.load(f)
        for key in json_obj:

            if json_obj[key]["filename"] == "0001.jpg.png":
                filename = "00001.png"
            else:
                filename = json_obj[key]["filename"]

            #if not filename.startswith("Unknown"):
            #    break

            if not len(json_obj[key]["regions"]) == 0:

                for r in json_obj[key]["regions"]:
                    attributes = json_obj[key]["regions"][r]["region_attributes"]

                    if "Type" in attributes:
                        c = attributes["Type"].lower().strip()
                    elif "type" in attributes:
                        c = attributes["type"].lower().strip()

                    if c not in ["glass", "cup"]:
                        break

                    if "Fill" in attributes:
                        f = attributes["Fill"].lower().strip()
                    elif "fill" in attributes:
                        f = attributes["fill"].lower().strip()

                    # exclude fill levels that are actually classes
                    if f in classes:
                        break

                    if f not in acceptable_fills:
                        break

                    shape_attributes = json_obj[key]["regions"][r]["shape_attributes"]

                    if filename in df:
                        df[filename]["class"].append(str(c))
                        df[filename]["fill"].append(str(f))
                        df[filename]["x"].append(str(shape_attributes["x"]))
                        df[filename]["y"].append(str(shape_attributes["y"]))
                        df[filename]["width"].append(str(shape_attributes["width"]))
                        df[filename]["height"].append(str(shape_attributes["height"]))
                    else:
                        df[filename] = {"class": [str(c)],
                                        "fill": [str(f)],
                                        "x": [str(shape_attributes["x"])],
                                        "y": [str(shape_attributes["y"])],
                                        "width": [str(shape_attributes["width"])],
                                        "height": [str(shape_attributes["height"])]}

    output = []
    output.append(fields)
    for f in df:
        for i in range(len(df[f]["class"])):
            output.append([f, df[f]["class"][i], df[f]["fill"][i], df[f]["x"][i], df[f]["y"][i], df[f]["width"][i], df[f]["height"][i]])

    output_file = pd.DataFrame(output)
    output_file.to_csv(output_name, index = False, header = False)


def separate_classes(input_csv):
    df = pd.read_csv(input_csv, index_col = False)
    print(input_csv, "shape:", df.shape)

    test = df[(df["fill"] == 0) & (df["class"] == "cup")].sample(frac = 0.2)
    test = test.append(df[(df["fill"] == 30) & (df["class"] == "cup")].sample(frac = 0.2))
    test = test.append(df[(df["fill"] == 100) & (df["class"] == "cup")].sample(frac = 0.2))
    test = test.append(df[(df["fill"] == 0) & (df["class"] == "glass")].sample(frac = 0.2))
    test = test.append(df[(df["fill"] == 30) & (df["class"] == "glass")].sample(frac = 0.2))
    test = test.append(df[(df["fill"] == 100) & (df["class"] == "glass")].sample(frac = 0.2))

    train = pd.concat([df, test, test]).drop_duplicates(keep = False)
    print("Test dataset", test.shape)
    print("Train dataset", train.shape)

    train.to_csv(os.path.splitext(input_csv)[0] + "_train.csv", index = False)
    test.to_csv(os.path.splitext(input_csv)[0] + "_test.csv", index = False)


json_to_csv("tdb_m.csv", "TDB_M")
separate_classes("tdb_m.csv")

json_to_csv("tdb_s1.csv", "TDB_S/1")
separate_classes("tdb_s1.csv")

json_to_csv("tdb_s2.csv", "TDB_S/2")
separate_classes("tdb_s2.csv")

json_to_csv("tdb_s3.csv", "TDB_S/3")
separate_classes("tdb_s3.csv")

json_to_csv("tdb_s4.csv", "TDB_S/4")
separate_classes("tdb_s4.csv")

# now save the names of each subset to temporary file
# tail -n+2 tdb_m_test.csv | cut -d, -f1 > "test.csv"

# now create folders with needed images only
# for i in $(cat test.csv); do temp="${i%\"}"; temp="${temp#\"}"; cp TDB_M/$temp Test; done
