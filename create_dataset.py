import pandas as pd
import glob
import json
import os
import cv2

import sys
import matplotlib.pyplot as plt

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


def separate_train_test(input_csv):
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


#json_to_csv("tdb_m.csv", "TDB_M")
#separate_train_test("tdb_m.csv")

#json_to_csv("tdb_s1.csv", "TDB_S/1")
#separate_train_test("tdb_s1.csv")

#json_to_csv("tdb_s2.csv", "TDB_S/2")
#separate_train_test("tdb_s2.csv")

#json_to_csv("tdb_s3.csv", "TDB_S/3")
#separate_train_test("tdb_s3.csv")

#json_to_csv("tdb_s4.csv", "TDB_S/4")
#separate_train_test("tdb_s4.csv")

# now save the names of each subset to temporary file
# tail -n+2 tdb_m_test.csv | cut -d, -f1 > "test.csv"

# now create folders with needed images only
# for i in $(cat test.csv); do temp="${i%\"}"; temp="${temp#\"}"; cp TDB_M/$temp Test; done


def crop_separate_classes(input_dir, img_count, output_dir):

    for fill_level in acceptable_fills:
        new_dir = os.path.join(output_dir, fill_level)
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
            print("Created a new directory", new_dir)
        #else:
            #print("The directory {}  will be overwritten.".format(new_dir))

    for f in os.listdir(input_dir):
        if f.endswith(".csv"):
            df = pd.read_csv(os.path.join(input_dir, f))

            count = 0

            for index, row in df.iterrows():

                if os.path.exists(os.path.join(input_dir, row['filename'])):
                    #print("working with file:", row['filename'])

                    image = cv2.imread(os.path.join(input_dir, row['filename']), cv2.COLOR_BGR2RGB)

                    crop_image = image[int(row['y']) : int(row['y']) + int(row['height']),
                                        int(row['x']): int(row['x']) + int(row['width'])]

                    if not 0 in crop_image.shape:

                        #plt.imshow(crop_image)
                        #plt.show()

                        # resize to the shape 32x32
                        resized_image = cv2.resize(crop_image, (32, 32), interpolation = cv2.INTER_AREA)

                        gray_image = cv2.cvtColor(resized_image, cv2.COLOR_RGB2GRAY)

                        final_image_name = os.path.join(output_dir, str(row['fill']), str(img_count)) + ".jpg"
                        cv2.imwrite(final_image_name, gray_image)

                        img_count += 1

                else:
                    print("file {} from {} does not exist".format(row['filename'], os.path.join(input_dir, f)))

                #count += 1

                #if count == 40:
                #    sys.exit()

    return(img_count)


    #df = pd.read_csv(os.path, index_col = False)
    #print(input_csv, "shape:", df.shape)

#img_count = 0
#img_count = crop_separate_classes("../test_train_data/TDB_M_test", img_count, "../test_train_data/test")
#img_count = crop_separate_classes("../test_train_data/TDB_S1_test", img_count, "../test_train_data/test")
#img_count = crop_separate_classes("../test_train_data/TDB_S2_test", img_count, "../test_train_data/test")
#img_count = crop_separate_classes("../test_train_data/TDB_S3_test", img_count, "../test_train_data/test")
#img_count = crop_separate_classes("../test_train_data/TDB_S4_test", img_count, "../test_train_data/test")


#img_count = crop_separate_classes("../test_train_data/TDB_M_train", img_count, "../test_train_data/train")
#img_count = crop_separate_classes("../test_train_data/TDB_S1_train", img_count, "../test_train_data/train")
#img_count = crop_separate_classes("../test_train_data/TDB_S2_train", img_count, "../test_train_data/train")
#img_count = crop_separate_classes("../test_train_data/TDB_S3_train", img_count, "../test_train_data/train")
#img_count = crop_separate_classes("../test_train_data/TDB_S4_train", img_count, "../test_train_data/train")


#for file in $(ls -p | grep -v / | tail -2000); do mv $file ./100; done


def object_detection(input_dir, output_dir, appendix, max_number):

    count = 0

    for f in os.listdir(input_dir):
        if f.endswith(".csv"):
            df = pd.read_csv(os.path.join(input_dir, f))

            for index, row in df.iterrows():

                if os.path.exists(os.path.join(input_dir, row['filename'])):

                    image = cv2.imread(os.path.join(input_dir, row['filename']), cv2.COLOR_BGR2RGB)

                    if 0 not in image.shape:
                        file_df = df[df['filename'] == row['filename']]

                        full_height = image.shape[0]
                        full_width = image.shape[1]

                        rows = []

                        for index2, row2 in file_df.iterrows():
                            one_row = []
                            h = int(row2['height'])/2
                            y = int(row2['y']) + h

                            w = int(row2['width'])/2
                            x = int(row2['x']) + w

                            y = y / full_height
                            x = x / full_width
                            h = h / full_height
                            w = w / full_width

                            if row2['class'] == "cup":
                                one_row = [0, x, y, w, h]

                            elif row2['class'] == "glass":
                                one_row = [1, x, y, w, h]

                            rows.append(one_row)

                        txt_name = os.path.splitext(row['filename'])[0] + ".txt"
                        final_txt_name = os.path.join(output_dir, "labels", appendix, txt_name)

                        txt_file = open(final_txt_name, 'w')
                        for r in rows:
                            txt_file.write(' '.join([str(x) for x in r]) + '\n')
                        txt_file.close()

                        if os.path.exists(final_txt_name):
                            gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
                            final_img_name = os.path.join(output_dir, "images", appendix, str(row['filename']))
                            cv2.imwrite(final_img_name, gray_image)

                            count += 1
                            print(count)

                            if count == max_number:
                                return("done")


done = object_detection("../test_train_data/TDB_M_train", "../objects_detection/new/", "train", 240)
done = object_detection("../test_train_data/TDB_M_train", "../objects_detection/new/", "val", 60)

# ~/aitalents/objects_detection/yolov5$ python train.py --batch 16 --img 80 --epochs 3 --data ../new_data_yaml.yml --cfg ./models/yolov5s.yaml --weights '' --name cups_glasses

#(object_detection) anastasiia@anastasiia-HP-ProBook-440-G3:~/aitalents/objects_detection/yolov5$ python train.py --batch 16 --img 200 --epochs 300 --data ../new_data_yaml.yml --cfg ./models/yolov5s.yaml --weights '' --name cups_glasses
