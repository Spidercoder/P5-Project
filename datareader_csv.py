import pandas as pd

import idpoint
import message


def __load_data(filepath, parse_func, start, limit):
    data = []
    # Creating a dataframe that contains the specified rows of the specified csv file.
    df = pd.read_csv(filepath, header=0, skiprows=range(1, start + 1), nrows=limit)

    df_list = df.values.tolist()

    for count, row in enumerate(df_list):
        if count % 50000 == 0:
            print(count)
        data.append(parse_func(row))

    return data


def load_messages(filepath, start=0, limit=None):
    return __load_data(filepath, message.parse_csv_row, start, limit)


def load_idpoints(filepath, start=0, limit=None):
    return __load_data(filepath, idpoint.parse_csv_row, start, limit)


# Loads data from "Attack_free_dataset.csv"
def load_attack_free1(start=0, limit=None):
    return load_messages("data_csv/Attack_free_dataset.csv", start, limit)


# Loads data from "Attack_free_dataset2.csv"
def load_attack_free2(start=0, limit=None):
    return load_messages("data_csv/Attack_free_dataset2.csv", start, limit)


# Loads data from "Impersonation_attack_dataset.csv"
def load_impersonation_1(start=0, limit=None):
    return load_messages("data_csv/Impersonation_attack_dataset.csv", start, limit)


# Loads data from "170907_impersonation.csv"
def load_impersonation_2(start=0, limit=None):
    return load_messages("data_csv/170907_impersonation.csv", start, limit)


# Loads data from "170907_impersonation_2.csv"
def load_impersonation_3(start=0, limit=None):
    return load_messages("data_csv/170907_impersonation_2.csv", start, limit)


# Loads data from "DoS_attack_dataset.csv"
def load_dos(start=0, limit=None):
    return load_messages("data_csv/DoS_attack_dataset.csv", start, limit)


# Loads data from "Fuzzy_attack_dataset.csv"
def load_fuzzy(start=0, limit=None):
    return load_messages("data_csv/Fuzzy_attack_dataset.csv", start, limit)
