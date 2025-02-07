from os import system
import os
import argparse
import difflib
import re

parser = argparse.ArgumentParser(description="Codeforces automatization tool.")
subparsers = parser.add_subparsers(dest="command")

TEMPLATE_PATH = "cf_template.cpp"
BUILD_OPTIONS = "-Wall -g0 -O0 --std=c++20"


def extract_problem_from_path(problem_dir):
	split_problem_dir = os.path.split(problem_dir)
	if split_problem_dir[0] == "practice":
		split_problem_name = split_problem_dir[-1].split("_")
		contest_id = split_problem_name[-2]
		problem_letter = split_problem_name[-1]
	else:
		contest_id = split_problem_dir[-2]
		problem_letter = split_problem_dir[-1]

	return (contest_id, problem_letter)


def build_and_run(problem_path, input_file, output_file):
	build_command = f"g++ {BUILD_OPTIONS} -o {problem_path} {problem_path}.cpp"

	print("-"*60)

	system(f"\
		{build_command} && \
		(./{problem_path} < {input_file}) | tee {output_file}"
	)

	print("\n" + "-" * 60)
	return


def get_in_out_ans(problem_dir):
	input_file  = os.path.join(problem_dir, "in.txt")
	output_file = os.path.join(problem_dir, "out.txt")
	answer_file = os.path.join(problem_dir, "ans.txt")
	return input_file, output_file, answer_file


def find_valid_directory(contest_id, problem_letter):
	problem_dir = ""
	contest_problem_dir = f"./{contest_id}/{problem_letter}"

	contest_dir_is_valid = os.path.isdir(contest_problem_dir)

	if not contest_dir_is_valid:
		print(f"No valid directory is found for a problem {contest_id}{problem_letter}")
		return None

	return contest_problem_dir
		

def check_solution(output_file, answer_file):
    """Compares out.txt with ans.txt and highlights differences."""
    
    with open(output_file, "r") as f1, open(answer_file, "r") as f2:
        output_lines = f1.readlines()
        answer_lines = f2.readlines()

    output_lines = [line.rstrip() for line in output_lines]
    answer_lines = [line.rstrip() for line in answer_lines]

    if len(output_lines) != len(answer_lines):
    	has_less_lines = output_lines if len(output_lines) < len(answer_lines) else answer_lines
    	has_more_lines = output_lines if len(output_lines) > len(answer_lines) else answer_lines
    	while (len(has_less_lines) < len(has_more_lines)):
    		has_less_lines.append("<empty_line>")

    if output_lines == answer_lines:
        print("Correct answer.")
        return

    for i, (out_line, ans_line) in enumerate(zip(output_lines, answer_lines), start=1):
        if out_line != ans_line:
            print(f"Difference at line {i}:\n" + \
            	  f"\tExpected: `{ans_line}`\n" + \
            	  f"\tFound:    `{out_line}`")


def argument(*name_of_flags, **kwargs):
	return (list(name_of_flags), kwargs)


def subcommand(args=[], parent=subparsers):
	def decorator(func):
		parser = parent.add_parser(func.__name__, description=func.__doc__)
		for arg in args:
			parser.add_argument(*arg[0], **arg[1])
		parser.set_defaults(func=func)
	return decorator


@subcommand(
	[
		argument("contest", help="contest ID", type=str),
		argument("problem", help="problem letter", type=str)
	],
	parent = subparsers
)
def create(args):
	'''Creates a structured folder for a given problem.'''

	contest_id       = args.contest
	problem_letter   = args.problem.upper()

	if (not os.path.exists(contest_id)):
			system(f"mkdir {contest_id}")
			print(f"Directory: {contest_id} -- is created.")

	problem_name = contest_id + problem_letter
	problem_dir = os.path.join(contest_id, problem_letter)
		
	files = \
		["in.txt","out.txt","ans.txt",f"{problem_name}.cpp"]

	files_to_create = \
		" ".join([os.path.join(problem_dir, file) for file in files])
		
	if (os.path.exists(problem_dir)):
		print(f"The directory {problem_dir} already exists. Nothing is changed.")
		return

	system(f"mkdir {problem_dir}")
	system(f"touch {files_to_create}")

	if not TEMPLATE_PATH is None and os.path.exists(TEMPLATE_PATH):
		system(f"cat {TEMPLATE_PATH} > {os.path.join(problem_dir, f"{problem_name}.cpp")}")
		print("OK!")
	return


@subcommand(
	[
		argument("contest", help="contest ID", type=str),
		argument("problem", help="problem letter", type=str)
	],
	parent = subparsers
)
def run(args):
	'''Build and run a file if it exists.'''

	contest_id       = args.contest
	problem_letter   = args.problem.upper()

	problem_dir = find_valid_directory(contest_id, problem_letter)
	if problem_dir is None:
		return
	
	problem_name = contest_id + problem_letter.upper()
	problem_path = os.path.join(problem_dir, problem_name)

	input_file, output_file, answer_file = get_in_out_ans(problem_dir)

	build_and_run(problem_path, input_file, output_file)

	check_solution(output_file, answer_file)


def main():
	args = parser.parse_args()

	if args.command is None:
		parser.print_help()
	else:
		args.func(args)


if __name__ == "__main__":
	main()
