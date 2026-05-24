# bashrc_szhu

Personal Bash environment helpers for ALICE/O2 work on a Slurm cluster. The repository provides a `.bashrc_szhu` entry point, shell helper functions, reusable interactive/container environment snippets, Slurm array wrappers, and a few small command-line utilities.

## Layout

- `.bashrc_szhu` - main shell entry point. It prints a short system summary, exports project paths, sources all files in `_include/`, and prepends `bin/` to `PATH`.
- `_include/` - Bash functions and completions loaded by `.bashrc_szhu`.
- `bash_env/` - snippets used by the `start` helper to enter interactive Slurm or Singularity environments.
- `slurm_env/` - Slurm batch wrapper scripts used by `submit`.
- `bin/` - executable helper scripts for environment setup, queue monitoring, package updates, compilation, and file-list utilities.

## Installation

Clone this repository to the path expected by `.bashrc_szhu`:

```bash
git clone git@github.com:sjzhu0v0/bashrc_szhu.git /u/tcheng/.bashrc_szhu.d
```

Then source the entry point from `~/.bashrc` or create a symlink:

```bash
source /u/tcheng/.bashrc_szhu.d/.bashrc_szhu
```

The current configuration assumes these site-specific paths exist:

- `/u/tcheng/.bashrc_szhu.d`
- `/lustre/alice/users/tcheng/szhu/submit`
- `/lustre/alice/users/tcheng/szhu/share/cert`
- `/lustre/alice/users/tcheng/szhu/packages/AnalysisFramework`
- `/lustre/alice/users/tcheng/szhu/packages/QA`
- `/lustre/alice/users/szhu/share/lib`
- `/lustre/alice/users/szhu/opt/lib64`
- `/lustre/alice/users/szhu/opt/include`
- `/u/szhu/node_modules`

## Shell Helpers

### `mecho`

Print colored status messages.

```bash
mecho success "done"
mecho warning "check this"
mecho error "failed"
```

Supported modes are `success`, `warning`, `error`, `info`, `notice`, `debug`, and `trace`.

### `start`

Source an environment snippet from `bash_env/`.

```bash
start gcc14
start o2phys_local
```

Only file names under `bash_env/` are accepted. Bash completion is provided for available snippets.

### `submit`

Submit a command list as a Slurm job array through a wrapper from `slurm_env/`.

```bash
submit [-p partition] [-n job_name] [-t time_limit] [-a array_spec] [--dependency dependency_spec] <slurm_env> <command_file> [ncommands_onefile]
```

Examples:

```bash
submit gcc14 commands.txt
submit -p main -n qa_run -t 04:00:00 gcc14_2 commands.txt
submit o2phys_local commands.txt 20
```

If `-n` is omitted, the job name is derived from the command file name. Submissions are recorded in `${SZHU_SUBMIT_DIR}/history_submission`.

### `shistory`, `swhich`, and `sresubmit`

Look up previous submissions from the submission history and resubmit saved jobs.

```bash
shistory qa_run
swhich qa_run
sresubmit qa_run
sresubmit qa_run -n qa_run_retry -t 04:00:00 -p main
```

`shistory` resolves the job ID and calls `sacct`; `swhich` prints the stored submission command. Both commands match the exact `-n <job_name>` field in the history file. `sresubmit` records the resubmit request in the same history file, finds the most recent exact job-name match, rebuilds the original `submit` command, and applies any optional overrides for `-p`, `-n`, `-t`, `-a`, `--dependency`, or positional submit arguments.

### `unset_proxy`

Unset proxy-related environment variables and set JAliEn token certificate paths from `${SZHU_CERT_DIR}`.

## `bin/` Commands

- `init_lcg_el9` - source this Bash setup inside an EL9 LCG/CERN SFT environment.
- `init_lcg_el9_34` - similar LCG setup with an inline `mecho` definition.
- `init_o2phys` - configure local O2Physics paths and JAliEn token variables.
- `env_o2phys` - enter an `alienv` O2Physics version, defaulting to `VO_ALICE@O2Physics::daily-20260311-0000-1`.
- `update_qa` - run `git pull` in the configured AnalysisFramework and QA package directories.
- `fast_compile` - update packages, enter the ALICE Alma9 Singularity image, initialize LCG, and run `make all`.
- `sqqq` - run `squeue -u tcheng`.
- `sqqqq` - refresh `squeue -u tcheng` every 60 seconds.
- `file_size.py` - compute the total size of files listed in a text file.
- `file_batch_splitter.py` - split a file list into groups capped by total size.

Python utility examples:

```bash
file_size.py -f files.txt -u GB
file_batch_splitter.py -i files.txt -s 10240 -o batch
```

## Environment Snippets

`bash_env/` files are intended to be used with `start`:

- `gcc14` - allocate a Slurm session and enter the ALICE Alma9 Singularity image with CVMFS and Lustre mounted.
- `gcc14_noReservation` - enter the ALICE Alma9 Singularity image directly.
- `o2phys_build` - start an interactive build shell with a high-memory scratch container mount.
- `o2phys_local` and `o2phys_local2` - start interactive O2Physics container sessions with local scratch/Lustre mounts.

## Slurm Wrappers

`slurm_env/` files execute one line from a command list according to `SLURM_ARRAY_TASK_ID`:

- `gcc14`, `gcc14_2`, and `gcc14_2_highMem` - run commands in the ALICE Alma9 Singularity image after LCG initialization.
- `o2phys_local` and `o2phys_local2` - run commands inside the local O2Physics container with `alienv enter O2Physics/latest`.

Wrappers use `OUT_DIR/%a` and `ERR_DIR/%a` for Slurm output/error paths, so create those directories where the job is submitted if needed.

## Notes

This repository is intentionally site-specific. Before using it on another account or cluster, review `.bashrc_szhu`, `bash_env/`, and `slurm_env/` for hard-coded usernames, Lustre paths, CVMFS paths, container images, Slurm partitions, reservations, and certificate locations.
