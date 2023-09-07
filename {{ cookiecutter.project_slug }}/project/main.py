from pathlib import Path

import numpy as np
import pandas as pd
import submitit

here = Path(__file__).parent
repo_root = here.parent


def save_random_dataframe(output_directory: Path, output_file: Path):
    """Creates a random dataframe and saves to csv

    Args:
        output_directory: absolute path to directory to save df in
        output_file: filename to save dataframe to in output_directory
    Returns: None.
    """
    random_df = pd.DataFrame(
        np.random.randint(0, 100, size=(100, 4)), columns=list("ABCD")
    )
    random_df.to_csv(output_directory / output_file)


if __name__ == "__main__":
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
    query_directory = here / "query"
    if (query_directory / args.query).exists():
        query_path = query_directory / args.query
    elif Path(args.query).resolve().exists():
        query_path = Path(args.query).resolve()
    else:
        raise ValueError(
            f"Could not locate {args.query} in query directory or as absolute path"
        )
    with open(query_path) as f:
        query = json.load(f)
    # set up logging and results
    name = query.get("name", query_path.stem)

    output_directory = query.get("output_directory", repo_root / "results")
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
        if query.get("cluster", False):
            job = executor.submit(
                save_random_dataframe,
                output_directory,
                output_file,
            )
        else:
            save_random_dataframe(
                output_directory,
                output_file,
            )
