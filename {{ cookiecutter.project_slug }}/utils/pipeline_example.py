"""Pipeline example"""

import os
from pathlib import Path
{% if cookiecutter.cluster == 'yes' %}import submitit{% endif %}

from utils.preprocess_util_lib_example import generate_random_dataframe, REPO_ROOT

if __name__ == "__main__":
    {% if cookiecutter.cluster == 'yes' %}
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
                generate_random_dataframe,
            )
        else:
            generate_random_dataframe()
    {% else %}
    # This is an example of running the code as a pipeline
    # Rather than through a notebook
    data_dir = Path(os.environ["DATA_DIR"])
    output_directory = data_dir / "output"
    output_file = "sample_output.csv"
    output_directory.mkdir(parents=True, exist_ok=True)

    random_df = generate_random_dataframe()
    random_df.to_csv(output_directory / output_file, index=False)
    print(f"Saved random dataframe to {output_directory / output_file}")
    {% endif %}