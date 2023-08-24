data_list = [
    {'key1': 'value1', 'key2': 'value2'},
    {'key1': 'value3', 'key3': 'value3', 'key4': 'value5'},
]

def print_table(data_list):
    all_keys = set(key for data_dict in data_list for key in data_dict.keys())
    max_key_length = max(max(len(key) for key in all_keys), len("Keys"))
    table_format = "{:<{key_width}} |"

    for key in all_keys:
        table_format += " {:<15} |"

    separator = "-" * (max_key_length + 1) + "+"
    separator += "+".join(["-" * 17 for _ in all_keys])

    header = table_format.format("Keys", key_width=max_key_length)
    columns = [key for key in all_keys]
    print(header)
    print(separator)
    for data_dict in data_list:
        row = table_format.format("Data", key_width=max_key_length)
        for key in columns:
            value = data_dict.get(key, "")
            row += " {:<15} |".format(value)
        print(row)
        print(separator)

print_table(data_list)
