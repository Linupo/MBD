import json

def remove_string_values(json_data):
  new_list_of_objects = []
  for obj in json_data:
    new_obj = {}
    for key, value in obj.items():
      if not isinstance(value, str):
        new_obj[key] = value
      # sometimes empty arrays ([]) seems to be assigned even after flattening
      if isinstance(value, list):
        new_obj[key] = 0
    new_list_of_objects.append(new_obj)

  return new_list_of_objects

def add_missing_features(json_data):
    features = set()
    for obj in json_data:
        features.update(obj.keys())

    # This json will be used to add missing features to the tx we want to classify
    with open("all_features.json", "w") as f:
      f.write(json.dumps(list(features)))

    for obj in json_data:
        for feature in features:
            if feature not in obj:
                obj[feature] = 0

    return json_data

def make_true_false_features_binary(objects):
  new_objects = []
  for obj in objects:
    new_obj = {}
    for key, value in obj.items():
      if isinstance(value, bool):
        value = int(value)
      new_obj[key] = value
    new_objects.append(new_obj)

  return new_objects

with open("flat_txs.json", "r") as f:
    json_data = json.load(f)

#subset
def create_subset(json_data):
  filtered_list = []
  illicit_count = 0
  licit_count = 0
  for item in json_data:
    if item["elliptic_label"] == '2' and illicit_count != 1000:
      filtered_list.append(item)
      illicit_count = illicit_count + 1
  for item in json_data:
    if item["elliptic_label"] == '1' and licit_count != 1000:
      filtered_list.append(item)
      licit_count = licit_count + 1

  return filtered_list

def modify_labels(json_data):
  casted_list = []
  for item in json_data:
    item["elliptic_label"] = int(item["elliptic_label"])
    casted_list.append(item)
  return casted_list

json_data = create_subset(json_data)
json_data = modify_labels(json_data)
json_data = remove_string_values(json_data)
json_data = add_missing_features(json_data)
json_data = make_true_false_features_binary(json_data)

with open("subset_pretrained_flat_txs.json", "w") as f:
    json.dump(json_data, f)
