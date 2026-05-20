#!/usr/bin/env python3
import os
import argparse

def group_files_by_size(list_file, max_group_size_mb, output_prefix="group"):
    """
    Group file paths listed in a text file based on a maximum group size.

    :param list_file: Text file containing file paths, one per line
    :param max_group_size_mb: Maximum size per group (in MB)
    :param output_prefix: Prefix for output group files
    """
    max_group_size = max_group_size_mb * 1024 * 1024  # Convert MB to bytes

    # Read file list
    with open(list_file, "r", encoding="utf-8") as f:
        files = [line.strip() for line in f if line.strip()]

    groups = []
    current_group = []
    current_size = 0

    for file_path in files:
        if not os.path.exists(file_path):
            print(f"[WARNING] File does not exist: {file_path}")
            continue

        file_size = os.path.getsize(file_path)

        # If the file does not fit, start a new group
        if current_size + file_size > max_group_size and current_group:
            groups.append(current_group)
            current_group = []
            current_size = 0

        current_group.append(file_path)
        current_size += file_size

    # Add the last group
    if current_group:
        groups.append(current_group)

    # Write output files
    for idx, group in enumerate(groups, 1):
        out_name = f"{output_prefix}_{idx}.txt"
        with open(out_name, "w", encoding="utf-8") as f:
            f.write("\n".join(group))

        print(f"Generated {out_name}, containing {len(group)} files")

    print(f"\nTotal {len(groups)} groups created.")


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Group file paths by total size limit."
    )
    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Input text file containing file paths (one per line)"
    )
    parser.add_argument(
        "-s", "--size",
        type=int,
        required=True,
        help="Maximum size per group in MB"
    )
    parser.add_argument(
        "-o", "--output-prefix",
        default="group",
        help="Prefix for output group files (default: group)"
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    group_files_by_size(
        list_file=args.input,
        max_group_size_mb=args.size,
        output_prefix=args.output_prefix
    )

