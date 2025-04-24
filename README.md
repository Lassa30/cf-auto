Table of contents
---
- [About](#about)
- [Usage example](#usage-example)
  - [Create files for the contest](#create-files-for-the-contest)
  - [Create one problem to practice on](#create-one-problem-to-practice-on)
  - [Demo](#demo)
- [Installation](#installation)
- [Configuration](#configuration)
  - [Parameters examples:](#parameters-examples)
- [TODOs](#todos)

# About
Here is the description you get after typing `cf-auto --help`
```bash
usage: cf-auto.py [-h] {create,run} ...

Codeforces routine tasks automation tool.

positional arguments:
  {create,run}

options:
  -h, --help    show this help message and exit

```
From this we can tell, that `cf-auto` is capable of:
- creating necessary files for the specified **contest** OR **problem**
- **compiling** and **running** your `C++` code with further comparing with fetched test cases: Right here, right now.

# Usage example
Use `cf-auto` and solve problems in one directory

## Create files for the contest
```bash
cf-auto create C 2000
```
The resulting directory has the following structure:
```
2000
├── A
│   ├── 2000A.cpp
│   ├── ans.txt
│   ├── in.txt
│   └── out.txt
├── B
│   ├── 2000B.cpp
│   ├── ans.txt
│   ├── in.txt
│   └── out.txt
├── C
│   ├── 2000C.cpp
│   ├── ans.txt
│   ├── in.txt
│   └── out.txt
etc.
```
## Create one problem to practice on
```bash
cf-auto create P 2000 A
```
And you get:
```
practice/
└── 2000_A
    ├── 2000_A.cpp
    ├── ans.txt
    ├── in.txt
    └── out.txt
```

## Demo
Coming soon...

# Installation
1. Clone the repo
```bash
git clone https://github.com/Lassa30/cf-auto.git
```
2. Install dependencies
```bash
pip install -r requirements.txt
```
3. Run `cf-auto`
```bash
python cf-auto.py --help
```

>**Optional:** 
>1. Add this alias to `~/.bashrc` to run `cf-auto` without interpreter name
>```
>alias cf-auto="python3 cf-auto.py"
>```
>2. Create a virtual environment before you install the dependencies
>```bash
>python -m venv .venv
>source .venv/bin/activate
>pip install -r requirements.txt
>```

# Configuration
> **Note:** the configuration is too simple and stupid, just hardcoded

## Parameters examples:
```python
TEMPLATE_PATH = "cf_template.cpp" # i.e. the path to your template file
BUILD_OPTIONS = "-Wall -g0 -O0 --std=c++20" # i.e. just some options for g++
```

# TODOs
- Nicer logging
- Use and test by yourself
- Add example usage
