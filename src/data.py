import csv
from pathlib import Path

from tqdm import tqdm


def parse_data(line):
    return [float(d) for d in line.split("\t")]


def parse_comment(line):
    data, comment = line.split("#* ")
    comment = comment.replace("/", ".")  # Replace / with . for filenames
    data = parse_data(data.rstrip())
    return comment, data


def make_newfile(current_file, data):
    columns = [
        "Time (s)",
        "Venous (mmHg)",
        "FAP (mmHg)",
        "Arterial - Pigtail (mmHg)",
        "Swan (mmHg)",
        "EKG (mV)",
    ]
    with open(current_file, "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(columns)
        writer.writerow(data)


def get_total(rawfile):
    with open(rawfile, "r") as f:
        total = len(f.readlines())
        return total


if __name__ == "__main__":

    datapath = Path().resolve() / "data/"
    rawfile = datapath / "raw/429_Group_3.txt"
    outfile = datapath / "processed/"

    in_comment = False
    comment_idx = 0
    total = get_total(rawfile)

    with open(rawfile, "r") as f:

        for line in tqdm(f, total=total):
            line = line.rstrip()

            if "=" in line:
                continue  # Skip lines containing metadata
            elif "#*" in line:
                # Turn every comment into a new file
                in_comment = True
                comment_idx += 1
                comment, data = parse_comment(line)
                current_file = outfile / f"{comment_idx}. {comment}.csv"
                make_newfile(current_file, data)
                continue

            if not in_comment:
                continue  # Skip lines unaffiliated with a comment

            with open(current_file, "a") as csvfile:
                data = parse_data(line)
                writer = csv.writer(csvfile)
                writer.writerow(data)
