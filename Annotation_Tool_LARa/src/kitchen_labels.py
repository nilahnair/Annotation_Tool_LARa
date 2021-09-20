import os
import global_variables as g

scenarios = ["brownies", "eggs", "sandwich"]
labels_location = f"..{os.sep}labels{os.sep}"

classes_brownies: list = None
classes_eggs: list = None
classes_sandwich: list = None
attributes_brownies: list = None
attributes_eggs: list = None
attributes_sandwich: list = None
labels_brownies: list = None
labels_eggs: list = None
labels_sandwich: list = None


def make_labels():
    for scenario in scenarios:
        classes = []
        attributes_1 = []
        attributes_2 = []
        with open(f'{labels_location}X3grounding_{scenario}.txt', "rt") as labels:
            lines = labels.readlines()
            for line in lines:
                #TODO handle labels that include an amount of things e.g. put-1-empty_egg_shell-sink
                label_parts = line.strip().split("-")
                if len(label_parts) == 4:
                    try:
                        int(label_parts[1])
                        label_parts[2] = label_parts[1]+"-"+label_parts[2]
                        label_parts.pop(1)
                    except:
                        label_parts[3] = label_parts[2] + "-" + label_parts[3]
                        label_parts.pop(2)
                if label_parts[0] not in classes:
                    classes.append(label_parts[0])
                if (len(label_parts) >= 2) and (label_parts[1] not in attributes_1):
                    attributes_1.append(label_parts[1])
                if (len(label_parts) >= 3) and (label_parts[2] not in attributes_2):
                    attributes_2.append(label_parts[2])

        with open(f'{labels_location}classes_{scenario}.txt', "wt") as txt:
            txt.write(classes[0])
            for class_ in classes[1:]:
                txt.write(f",{class_}")

        with open(f'{labels_location}attributes_{scenario}.txt', "wt") as txt:
            txt.write(f"I-{attributes_1[0]}")
            for attr in attributes_1[1:]:
                txt.write(f",I-{attr}")
            for attr in attributes_2:
                txt.write(f",II-{attr}")


try:
    with open(f"{labels_location}classes_brownies.txt", "rt") as f:
        classes_brownies: list = f.read().split(",")
    with open(f"{labels_location}classes_eggs.txt", "rt") as f:
        classes_eggs: list = f.read().split(",")
    with open(f"{labels_location}classes_sandwich.txt", "rt") as f:
        classes_sandwich: list = f.read().split(",")

    with open(f"{labels_location}attributes_brownies.txt", "rt") as f:
        attributes_brownies: list = f.read().split(",")
    with open(f"{labels_location}attributes_eggs.txt", "rt") as f:
        attributes_eggs: list = f.read().split(",")
    with open(f"{labels_location}attributes_sandwich.txt", "rt") as f:
        attributes_sandwich: list = f.read().split(",")
except Exception as exception:
    make_labels()
    with open(f"{labels_location}classes_brownies.txt", "rt") as f:
        classes_brownies: list = f.read().split(",")
    with open(f"{labels_location}classes_eggs.txt", "rt") as f:
        classes_eggs: list = f.read().split(",")
    with open(f"{labels_location}classes_sandwich.txt", "rt") as f:
        classes_sandwich: list = f.read().split(",")

    with open(f"{labels_location}attributes_brownies.txt", "rt") as f:
        attributes_brownies: list = f.read().split(",")
    with open(f"{labels_location}attributes_eggs.txt", "rt") as f:
        attributes_eggs: list = f.read().split(",")
    with open(f"{labels_location}attributes_sandwich.txt", "rt") as f:
        attributes_sandwich: list = f.read().split(",")

with open(f'{labels_location}X3grounding_brownies.txt', "rt") as labels:
    labels_brownies: list = [label.strip() for label in labels.readlines()]
with open(f'{labels_location}X3grounding_eggs.txt', "rt") as labels:
    labels_eggs: list = [label.strip() for label in labels.readlines()]
with open(f'{labels_location}X3grounding_sandwich.txt', "rt") as labels:
    labels_sandwich: list = [label.strip() for label in labels.readlines()]


def get_class_and_attributes(scenario: str, label: str) -> tuple:
    """transforms the kitchen dataset label into annotation tool labels

    scenario: "brownies", "eggs" or "sandwich"
    label: a string with an annotation from the kitchen dataset"""

    if scenario not in scenarios:
        raise ValueError("Invalid scenario was given")

    classes = classes_brownies if scenario == "brownies" else \
        classes_eggs if scenario == "eggs" else classes_sandwich
    attributes = attributes_brownies if scenario == "brownies" else \
        attributes_eggs if scenario == "eggs" else attributes_sandwich

    label_parts = label.split("-")
    if len(label_parts) == 4:
        try:
            int(label_parts[1])
            label_parts[2] = label_parts[1] + "-" + label_parts[2]
            label_parts.pop(1)
        except ValueError as e:
            label_parts[3] = label_parts[2] + "-" + label_parts[3]
            label_parts.pop(2)

    class_index = None
    for i, cls in enumerate(classes):
        if cls == label_parts[0]:
            class_index = i
            break
    if class_index is None:
        raise ValueError

    attribute_vector = [0 for _ in range(len(attributes))]

    for i, attr in enumerate([a for a in attributes if "II-" not in a]):
        if attr.split("-")[1] == label_parts[1]:
            attribute_vector[i] = 1
    for i, attr in enumerate([a for a in attributes if "II-" in a]):
        if attr.split("-")[1] == label_parts[2]:
            attribute_vector[i+len([a for a in attributes if "II-" not in a])] = 1


    if sum(attribute_vector) != len(label_parts[1:]):
        raise ValueError(label_parts[1:], sum(attribute_vector), len(label_parts[1:]))

    return class_index, attribute_vector


def get_kitchen_label(scenario: str, class_index: int, attribute_vector: list) -> str:
    """transforms annotation tool labels into the kitchen dataset label

        scenario: "brownies", "eggs" or "sandwich"
        label: a string with an annotation from the kitchen dataset"""

    if scenario not in scenarios:
        raise ValueError("Invalid scenario was given")

    classes = classes_brownies if scenario == "brownies" else \
        classes_eggs if scenario == "eggs" else classes_sandwich
    attributes = attributes_brownies if scenario == "brownies" else \
        attributes_eggs if scenario == "eggs" else attributes_sandwich
    # labels = labels_brownies if scenario == "brownies" else \
    #    labels_eggs if scenario == "eggs" else labels_sandwich

    label = classes[class_index]
    for i, attr in enumerate(attribute_vector):
        if attr:
            label += f"-{attributes[i].split('-')[1]}"

    # if label not in labels:
    #    raise ValueError

    return label


if __name__ == "__main__":
    """testing conversion methods"""
    labels = [labels_brownies, labels_eggs, labels_sandwich]
    for scenario_labels, scenario in zip(labels, scenarios):
        for label in scenario_labels:
            class_, attributes = get_class_and_attributes(scenario, label)
            new_label = get_kitchen_label(scenario, class_, attributes)
            if label != new_label:
                raise ValueError(label, new_label)
