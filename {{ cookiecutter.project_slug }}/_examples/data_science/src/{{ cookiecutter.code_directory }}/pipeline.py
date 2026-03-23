"""High-level orchestration for inference and evaluation.

These functions are the primary entry-points for students, usable both
from notebooks and from the CLI.
"""
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

from {{ cookiecutter.code_directory }}.evaluation import get_evaluator
from {{ cookiecutter.code_directory }}.inference import get_inference_strategy
from {{ cookiecutter.code_directory }}.io import load_inputs, load_outputs, save_outputs
from {{ cookiecutter.code_directory }}.settings import DATA_DIR

logger = logging.getLogger(__name__)

DEFAULT_INPUT = DATA_DIR / "input"
DEFAULT_OUTPUT_DIR = DATA_DIR / "output"
DEFAULT_EXPECTED_OUTPUT = DATA_DIR / "expected_outputs.json"


def run_inference(strategy_name, input_path=DEFAULT_INPUT, base_output_dir=DEFAULT_OUTPUT_DIR, params=None) -> Path:
    """Load inputs, run a strategy, save outputs and metadata.

    Args:
        strategy_name: Name of the InferenceStrategy subclass to use.
        input_path: Path to the input data.
        base_output_dir: Base output directory.  A timestamped subdirectory
            will be created under ``base_output_dir / strategy_name``.
        params: Optional dict of keyword arguments to pass to the strategy
            constructor.

    Returns:
        The path to the run directory.
    """
    logger.info("Loading input data from %s", input_path)
    inputs = load_inputs(input_path)

    logger.info("Running strategy: %s", strategy_name)
    strategy_cls = get_inference_strategy(strategy_name)
    strategy = strategy_cls(**(params or {}))

    # Run inference on each input
    outputs = {}
    for key, value in inputs.items():
        outputs[key] = strategy.do_inference(value)

    # Create timestamped output directory
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    run_dir = base_output_dir / strategy_name / timestamp
    run_dir.mkdir(parents=True, exist_ok=True)

    # Save outputs
    save_outputs(outputs, run_dir)
    logger.info("Saved %d outputs to %s", len(outputs), run_dir)

    # Save metadata
    metadata = strategy.metadata()
    metadata_path = run_dir / "metadata.json"
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)
    logger.info("Saved metadata to %s", metadata_path)

    return run_dir


def run_evaluation(evaluator_name, run_dir, expected_path) -> Path:
    """Run an evaluator, saving results into the same directory as outputs.

    Writes ``evaluation.json`` and any plots directly into *run_dir*
    (no nested subdirectory).

    Args:
        evaluator_name: Name of the AbstractEvaluator subclass to use.
        run_dir: Path to the inference run directory (contains outputs).
        expected_path: Path to the expected/ground-truth outputs.

    Returns:
        The path to the run directory.
    """
    logger.info("Running evaluator: %s", evaluator_name)
    evaluator_cls = get_evaluator(evaluator_name)
    evaluator = evaluator_cls()

    predicted = load_outputs(run_dir)
    actual = load_outputs(expected_path)

    results = evaluator.evaluate_all(predicted, actual)

    # Save evaluation results
    with open(run_dir / "evaluation.json", "w") as f:
        json.dump(results, f)
    logger.info("Saved evaluation results to %s", run_dir)

    # Save plots
    plots = evaluator.make_plots(results)
    for name, fig in plots.items():
        fig.savefig(run_dir / f"{name}.png")
        logger.info("Saved plot %s.png to %s", name, run_dir)

    return run_dir


def run_pipeline(strategy_name, evaluator_name, input_path=DEFAULT_INPUT,
                 *, expected_path, base_output_dir=DEFAULT_OUTPUT_DIR, params=None) -> Path:
    """Run inference followed by evaluation.

    Args:
        strategy_name: Name of the InferenceStrategy subclass to use.
        evaluator_name: Name of the AbstractEvaluator subclass to use.
        input_path: Path to the input data.
        expected_path: Path to the expected/ground-truth outputs.
        base_output_dir: Base output directory.
        params: Optional dict of keyword arguments to pass to the strategy
            constructor.

    Returns:
        The path to the run directory.
    """
    run_dir = run_inference(strategy_name, input_path, base_output_dir, params=params)
    run_evaluation(evaluator_name, run_dir, expected_path)
    return run_dir
