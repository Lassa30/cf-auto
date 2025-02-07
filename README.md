# cf-auto
A command line tool to minimize interactions with web interface and allow you to:

- create directories for a specified problem (using your template .cpp file)
- run and fetch sample tests for a specified problem (maybe in future but not yet...)

## Usage
1) Copy cf-auto script to the directory where you want to store problems.
2) Read further how to configure it

Optional: you may add the alias to "~/.bashrc" `alias cf-auto="python3 cf-auto.py"`

To insert sample tests you may use the command:
- `cat > in.txt` or `cat > out.txt` and paste what you've copied \
right into terminal.

## Configuration

There are two parameters that could be specified in "cf-auto.py" file:

- TEMPLATE_PATH = "cf_template.cpp" --> relative path to your template file.
- BUILD_OPTIONS = "-Wall -g0 -O0 --std=c++20" --> your personal options

These are values by default.