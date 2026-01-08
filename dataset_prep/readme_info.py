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
    match dpkg_resource.format:
        case "csv":
            df = pl.scan_csv(filepath)
        case "json":
            df = pl.read_json(filepath, infer_schema_length=1000)
        case "jsonl":
            # polars handles compression automatically
            df = pl.scan_ndjson(filepath)
        case _:
            raise ValueError(f"Unsupported format: {dpkg_resource.format}")

    print(f"\n\nDATA-SPECIFIC INFORMATION FOR: {dpkg_resource.path}\n\n")

    df_columns = df.collect_schema().names()
    print(f"1. Number of fields: {len(df_columns)}\n")

    # calculate total rows for lazy-loaded csv/jsonl
    if isinstance(df, pl.LazyFrame):
        num_rows = df.select(pl.len()).collect().item()
    else:
        # otherwise, use height
        num_rows = df.height
    print(f"2. Number of rows: {num_rows:,}\n")
    schema_fields = dpkg_resource.schema.fields

    # check that datapackage and data file agree
    assert len(schema_fields) == len(df_columns)
    field_info = {field.name: field for field in schema_fields}

    # output details about fields when requested
    if field_list:
        print("3. Field List:\n")
        for col in df_columns:
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


def main():
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
        # assume resource path is relative to the datapackage file
        datafile = args.datapackage.parent / resource.path
        # generate summary information for inclusion in a plain text readme file
        readme_info(resource, datafile, field_list=args.field_list)

    # if data dictionary is requested, create it based on info in datapackage file
    if args.data_dictionary:
        data_dictionary(datapackage, args.data_dictionary)


if __name__ == "__main__":
    main()
