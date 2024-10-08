"""Pipeline example"""
{% if cookiecutter.cluster == 'yes' %}from pathlib import Path

import submitit
{% endif %}
from {{ cookiecutter.code_directory }}.preprocess_util_lib_example import REPO_ROOT, save_random_dataframe

if __name__ == "__main__":
    {% if cookiecutter.cluster == 'yes' %}
    # code that will only be run when this file is executed as a script
    # (not if it is imported into another file as a module)
    import argparse
    import json

    # set up command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--query", help="path to json file containing query", default=None
    )
    args = parser.parse_args()
    # read in query
    if args.query is None:
        args.query = "sample.json"
    query_directory = REPO_ROOT / "config" / "query"
    if (query_directory / args.query).exists():
        query_path = query_directory / args.query
    elif Path(args.query).resolve().exists():
        query_path = Path(args.query).resolve()
    else:
        raise ValueError(
            f"Could not locate {args.query} in \
                query directory or as absolute path"
        )
    with query_path.open() as f:
        query = json.load(f)
    # set up logging and results
    name = query.get("name", query_path.stem)

    output_directory = query.get("output_directory", REPO_ROOT / "output")
    output_file = query.get("output_file")
    output_directory = Path(output_directory)
    output_directory.mkdir(parents=True, exist_ok=True)

    executor = submitit.AutoExecutor(folder=output_directory)
    # here we unpack the query dictionary and pull any
    # slurm commands that are in 'slurm' key. For these, they are the same
    # as those you use on the command line but instead of prepending with '--'
    # we prepend with 'slurm_'
    executor.update_parameters(**query.get("slurm", {}))

    with executor.batch():
        if query.get("submitit", False):
            executor.submit(
                save_random_dataframe,
                output_directory,
                output_file,
            )
        else:
            save_random_dataframe(
                output_directory,
                output_file,
            ){% else %}# This is an example of running the code as a pipeline
    # Rather than through a notebook
    output_directory = REPO_ROOT / "output"
    output_file = "sample_output.csv"
    output_directory.mkdir(parents=True, exist_ok=True)

    save_random_dataframe(
        output_directory,
        output_file,
    ){% endif %}
