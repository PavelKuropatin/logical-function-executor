from domain.value import VALUES


def generate_variables(names):
    data_set = __generate_data(VALUES, len(names))
    return [
        {
            names[i]: data[i]
            for i in range(len(data))
        }
        for data in data_set
    ]


def __generate_data(values, size) -> list:
    if not size:
        return []
    data = []
    for value in values:
        ends = __generate_data(values, size - 1)
        if ends:
            for end in ends:
                data.append([value] + end)
        else:
            data.append([value])
    return data
