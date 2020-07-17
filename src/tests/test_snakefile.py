from collections import defaultdict
from pathlib import Path
from typing import Any
from typing import Callable
from typing import Dict

import snakemake
from py._path.local import LocalPath as TmpDir


class SnakemakeLogger:
    """Returns a log handler for snakemake that tracks which rules were run and how many times"""

    def __init__(self) -> None:
        self.rule_count: Dict[str, int] = defaultdict(lambda: 0)

    @property
    def log_handler(self) -> Callable[[Dict[str, Any]], None]:
        """Returns a log handler for use with snakemake."""

        def fn(d: Dict[str, Any]) -> None:
            if d["level"] != "run_info":
                return
            # NB: skip the first two and last lines
            for counts_line in d["msg"].split("\n")[2:-1]:
                counts_line = counts_line.strip()
                count, job = counts_line.split("\t")
                assert int(count) > 0, counts_line
                self.rule_count[job] += int(count)

        return fn


def test_snakefile(tmpdir: TmpDir) -> None:
    # Create input files
    workdir: Path = Path(tmpdir) / "working"
    workdir.mkdir()
    filenames = [
        "genome.fasta",
        "foo.reads1.fastq.gz",
        "foo.reads2.fastq.gz",
        "bar.reads1.fastq.gz",
        "bar.reads2.fastq.gz",
    ]
    for filename in filenames:
        path: Path = workdir / filename
        with path.open("w"):
            pass

    # Build the logger
    logger: SnakemakeLogger = SnakemakeLogger()

    # Get the path to the snakefile
    src_dir: Path = Path(__file__).absolute().parent.parent
    snakefile: Path = src_dir / "Snakefile"

    # Run Snakemake
    result: bool = snakemake.snakemake(
        snakefile=str(snakefile),
        resources={"mem_gb": 8},
        workdir=str(workdir),
        lint=True,
        dryrun=True,
        quiet=True,
        log_handler=[logger.log_handler],
        ignore_ambiguity=True,
    )

    # Check the results
    assert result, "Snakemake did not complete successfully"
    rules: Dict[str, int] = {
        "align": 2,
        "all": 1,
        "sam_to_bam": 2,
        "index_bam": 1,
    }

    for rule, count in logger.rule_count.items():
        assert rule in rules, rule
        assert count == rules[rule], f"{rule}: {rules[rule]}"
