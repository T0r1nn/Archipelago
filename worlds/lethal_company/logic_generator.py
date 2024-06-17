from .options import CustomContent
from .imported import data
from json import loads, JSONDecodeError


def GetImportedData(custom_content_diff: CustomContent):
    data_copy = Copy(data)

    try:
        json_diff_string = custom_content_diff.value
        json_diff = loads(json_diff_string)
    except JSONDecodeError:
        return data_copy

    if type(json_diff) is not dict:
        return data_copy

    if "moons" in json_diff.keys():
        [data_copy["moons"].append(moon) for moon in json_diff.get("moons")]
    if "store" in json_diff.keys():
        [data_copy.get("store").append(shop_item) for shop_item in json_diff.get("store")]
    if "scrap" in json_diff.keys():
        data_copy["scrap"] = json_diff.get("scrap")
    if "bestiary" in json_diff.keys():
        data_copy["bestiary"] = json_diff.get("bestiary")

    return data_copy


def Copy(input_data):
    copied_data = {}
    for key, value in input_data.items():
        if value is dict:
            copied_data[key] = Copy(value)
        elif value is list:
            copied_data[key] = value.copy()
        else:
            copied_data[key] = value
    return copied_data
