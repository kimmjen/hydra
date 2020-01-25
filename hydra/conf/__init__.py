# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass, field
from typing import Any, List, Optional

from omegaconf import MISSING

from hydra.core.structured_config_store import StructuredConfigStore


@dataclass
class Hydra:
    @dataclass
    class RunDir:
        dir: str = MISSING

    @dataclass
    class SweepDir:
        dir: str = MISSING
        subdir: str = MISSING

    # Normal run output configuration
    run: RunDir = RunDir()
    # Multi-run output configuration
    sweep: SweepDir = SweepDir()
    # Logging configuration for Hydra
    hydra_logging: Any = MISSING
    # Logging configuration for the job
    job_logging: Any = MISSING
    # Sweeper configuration
    sweeper: Any = MISSING
    # Launcher configuration
    launcher: Any = MISSING
    # Program Help template
    help: Any = MISSING
    # Hydra's Help template
    hydra_help: Any = MISSING

    # Output directory for produced configuration files and overrides.
    # E.g., hydra.yaml, overrides.yaml will go here. Useful for debugging
    # and extra context when looking at past runs.
    output_subdir: str = ".hydra"

    # Those lists will contain runtime overrides
    @dataclass
    class Overrides:
        # Overrides for the hydra configuration
        hydra: List[str] = field(default_factory=lambda: [])
        # Overrides for the task configuration
        task: List[str] = field(default_factory=lambda: [])

    overrides: Overrides = Overrides()

    @dataclass
    # job runtime information will be populated here
    class Job:
        # Job name, can be specified by the user (in config or cli) or populated automatically
        name: str = MISSING

        # Concatenation of job overrides that can be used as a part
        # of the directory name.
        # This can be configured in hydra.job.config.override_dirname
        override_dirname: str = MISSING

        # Job ID in underlying scheduling system
        id: str = MISSING

        # Job number if job is a part of a sweep
        num: str = MISSING

        # The config file name used by the job (without the directory, which is a part of the search path)
        config_file: Optional[str] = MISSING

        @dataclass
        # Job config
        class Config:
            @dataclass
            # configuration for the ${hydra.job.override_dirname} runtime variable
            class OverrideDirname:
                kv_sep: str = "="
                item_sep: str = ","
                exclude_keys: List[str] = field(default_factory=lambda: [])

            override_dirname: OverrideDirname = OverrideDirname()

        config: Config = Config()

    job: Job = Job()

    # populated at runtime
    @dataclass
    class Runtime:
        version: str = MISSING
        cwd: str = MISSING

    runtime: Runtime = Runtime()

    # Can be a boolean, string or a list of strings
    # If a boolean, setting to true will set the log level for the root logger to debug
    # If a string, it's interpreted as a the list [string]
    # If a list, each element is interpreted as a logger to have logging level set to debug.
    # Typical command lines to manipulate hydra.verbose:
    # hydra.verbose=true
    # hydra.verbose=[hydra,__main__]
    # TODO: good use case for Union support in OmegaConf
    verbose: Any = False


s = StructuredConfigStore.instance()
s.store(group="hydra/schema", name="hydra", path="hydra", node=Hydra)
