
"""
Assumes you've run CUBE up to the activitysim step to prepare inputs.

This script runs multiple ActivitySim runs sequentially from a constant list of
(scenario_name, config_dir) pairs defined at the top of the file.
"""

import os
import shutil
import sys
import time
from pathlib import Path
import argparse
from copy import deepcopy

# ---------------------------------------------------------------------
# Constants: edit these
# ---------------------------------------------------------------------

VITM2_ROOT = Path(r'C:\Projects\25-0248_VITM2_EET\v201b2')

# ROOT_CONFIG_DIR = VITM2_ROOT / r'Inputs\ABM\activitysim\configs_vlc_test'
# PARENT_SCENARIO_DIR = VITM2_ROOT / "Base" / "Y2018/Y2018_ABM_RC24v2_01"
PARENT_SCENARIO_DIR = Path(r"C:\Projects\VITM2\activitysim\test_mtc_project\tests")
ROOT_CONFIG_DIR = Path(r"C:\Projects\VITM2\activitysim\test_mtc_project\tests\configs")



# List of (scenario_name, config_dir) pairs to run in sequence
from RUN_ACTIVITYSIM_custom_config import RUNS


from pathlib import Path
from typing import Iterable, Union

def rmtree_except_files(root: Union[str, Path], exclude_filenames: Iterable[str] = ()):
    """
    Recursively delete contents under `root`, but keep any files whose *name*
    is in `exclude_filenames`. Directories are removed only if empty after deletions.

    Parameters
    ----------
    root : str | Path
        Root directory whose contents will be deleted (root itself is kept).
    exclude_filenames : iterable[str]
        Filenames to preserve (match against Path.name, not full path).
    """
    root = Path(root)
    exclude = set(exclude_filenames)

    # delete bottom-up so dirs are empty before rmdir
    for path in sorted(root.rglob("*"), reverse=True):
        if path.is_file():
            if path.name in exclude:
                continue
            path.unlink()
        elif path.is_dir():
            # Only removes empty dirs; if excluded file keeps it non-empty, this will fail safely
            try:
                path.rmdir()
            except OSError:
                # not empty (likely because an excluded file exists), or permission issues
                pass


#


if __name__ == '__main__':
    for scen, config_dir in RUNS:
        if 'base' in scen:
            template = PARENT_SCENARIO_DIR / "prototype_mtc_v151_base_template"
        elif 'project' in scen:
            template = PARENT_SCENARIO_DIR / "prototype_mtc_v151_project_template"
        else:
            raise Exception("Unknown scen: {}".format(scen))
        if (PARENT_SCENARIO_DIR / scen).is_dir():
            rmtree_except_files(PARENT_SCENARIO_DIR / scen, exclude_filenames=["activitysim.log"])
        shutil.copytree(template, PARENT_SCENARIO_DIR / scen, dirs_exist_ok=True)

    # Control behavior when a run fails
    STOP_ON_FAIL = True  # set True to abort sequence on first failure

    # -----
