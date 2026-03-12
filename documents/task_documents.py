"""Tasks for compiling the paper and presentation(s)."""

import shutil
import subprocess
from pathlib import Path

import pytask

from final_project.config import BLD, DOCUMENTS, ROOT

for fmt, produces in {
    "pdf": ROOT / "paper.pdf",
    "html": ROOT / "_build" / "html" / "index.html",
}.items():

    @pytask.task(id=f"paper-{fmt}")
    def task_compile_paper(
        paper_md: Path = DOCUMENTS / "paper.md",
        myst_yml: Path = ROOT / "myst.yml",
        refs: Path = DOCUMENTS / "refs.bib",
        figure_a: Path = BLD / "figures" / "figure_a.png",
        figure_b: Path = BLD / "figures" / "figure_b.png",
        produces: Path = produces,
    ) -> None:
        """Compile the paper from MyST Markdown using Jupyter Book 2.0."""
        fmt = produces.suffix.lstrip(".")
        subprocess.run(
            ("jupyter", "book", "build", f"--{fmt}"),
            check=True,
            cwd=ROOT.absolute(),
        )
        if fmt == "pdf":
            build_pdf = ROOT / "_build" / "exports" / "paper.pdf"
            shutil.copy(build_pdf, produces)
