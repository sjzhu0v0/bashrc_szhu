# Slurm Documentation Prompt

```text
Describe the Slurm-related parts of this repository for a user who wants to submit and monitor batch jobs.

Focus on:
- The `submit` Bash function in `_include/_submit`
- The `slurm_env/` wrapper scripts
- The `shistory` and `swhich` helpers in `_include/_shistory`
- The queue helpers `sqqq` and `sqqqq`
- How command files are converted into Slurm job arrays
- How job names, partitions, time limits, dependencies, and array ranges are handled
- Where submission history and generated cache files are stored
- What site-specific paths or assumptions the user must know

Explain the workflow in practical terms:
1. Prepare a command file with one shell command per line.
2. Choose a wrapper from `slurm_env/`.
3. Run `submit`.
4. Monitor with `squeue`, `shistory`, or `swhich`.

Include concrete example commands, and mention any limitations or hard-coded assumptions.
```
