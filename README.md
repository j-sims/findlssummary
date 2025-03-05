### Summary

Parse the output of ```find /ifs -ls``` to provide a sum of file sizes per directory and file counts per directory. The summary is recursive for each directory listed.

### Installing
```curl -o findls-summary.py https://raw.githubusercontent.com/j-sims/findlssummary/refs/heads/main/findls-summary/findls-summary.py```

### Usage

#### Recommended 2-Stage
```find /ifs -ls > results.txt && python3 findls-summary.py -f results.txt ```

By performing a 2 Stage we have a cached copy of the output of the find command so if the user wants to summarize it differently the find (which can be long runnging) does not have to be re-run.

#### Alternative 1-Stage
```find /ifs -ls | python3 findls-summary.py```

One liner that pipes the output of the find command directly to the script.

#### Built-in Help
```usage: findls-summary.py [-h] [-f FILE] [-d DEPTH]

Parse 'find -ls' output and summarize disk usage.

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Input file containing 'find -ls' output. If not provided, reads from stdin.
  -d DEPTH, --depth DEPTH
                        Maximum depth to display in summary (0 for no limit).```
