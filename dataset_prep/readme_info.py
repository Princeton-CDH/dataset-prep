#!/usr/bin/env python

# utility script to generate readme information based on CSV and datapackage
#

import argparse
import csv
import pathlib

import polars as pl
from frictionless import Package, Resource


def readme_info(
    dpkg_resource: Resource, filepath: pathlib.Path, field_list: bool = True
) -> None:
    # print out summary information for inclusion in a plain text readme file

    # open the data file at the specified path based on the format in the resource
    match resource.format:
        case "csv":
            df = pl.read_csv(filepath)
        case "json":
            df = pl.read_json(filepath)
        case "jsonl":
            # polars handles compression automatically
            df = pl.read_ndjson(filepath)
        case _:
            raise ValueError(f"Unsupported format: {resource.format}")

    print(f"\n\nDATA-SPECIFIC INFORMATION FOR: {dpkg_resource.path}\n\n")

    print(f"1. Number of fields: {len(df.columns)}\n")
    print(f"2. Number of rows: {df.height:,}\n")
    schema_fields = dpkg_resource.schema.fields

    assert len(schema_fields) == len(df.columns)
    field_info = {field.name: field for field in schema_fields}

    # output details about fields when requested
    if field_list:
        print("3. Field List:\n")
        for col in df.columns:
            print("%s : %s" % (col, field_info[col].description))


def data_dictionary(datapackage: Package, output_path: pathlib.Path) -> None:
    print(f"\n\nWriting data dictionary to {output_path}")
    with output_path.open("w", encoding="utf-8") as csv_datadict:
        fieldnames = [
            "Filename",
            "Variable",
            "Variable name",
            "Description",
            "Type",
            "Format",
        ]
        csvwriter = csv.DictWriter(csv_datadict, fieldnames=fieldnames)
        csvwriter.writeheader()
        for resource in datapackage.resources:
            for field in resource.schema.fields:
                csvwriter.writerow(
                    {
                        "Filename": resource.path,
                        "Variable": field.title,
                        "Variable name": field.name,
                        "Description": field.description,
                        "Type": field.type,
                        "Format": field.format,
                    }
                )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "Generate dataset info readme from datapackage and data files"
    )
    parser.add_argument("datapackage", type=pathlib.Path)
    # flag to determine whether fields be listed
    parser.add_argument(
        "--field-list",
        help="Generate field list in readme.txt format",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    parser.add_argument(
        "-dd",
        "--data-dictionary",
        help="Create a data dictionary in the specified file",
        type=pathlib.Path,
    )

    args = parser.parse_args()

    if args.data_dictionary:
        if args.data_dictionary.exists():
            print(
                f"Requested data dictionary file {args.data_dictionary} already exists"
            )
            raise SystemExit(1)

    # open the specified path as a datapackage
    datapackage = Package(args.datapackage)

    for resource in datapackage.resources:
        # resource path should be relative to the datapackage file
        datafile = args.datapackage.parent / resource.path
        print("\n\nInspecting %s...\n\n" % datafile)

        readme_info(resource, datafile, field_list=args.field_list)

    # if data dictionary is requested, create it based on info in datapackage file
    if args.data_dictionary:
        data_dictionary(datapackage, args.data_dictionary)
