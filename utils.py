from dotenv import load_dotenv
import os
import csv

load_dotenv()

DATASET_TEST = os.environ.get("DATASET_TEST_PATH")
DATASET_TRAIN = os.environ.get("DATASET_TRAIN_PATH")


def read_csv(file_path):
    with open(file_path, mode="r", newline="") as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)
        print(f"Header: {header}")
        row_count = 0
        for row in csv_reader:
            row_count += 1
            print(row)
            if row_count == 5:
                break


read_csv(DATASET_TEST)
read_csv(DATASET_TRAIN)
