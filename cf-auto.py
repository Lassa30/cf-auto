from os import system
import os
import argparse
import difflib
import re

# TODO: after creating a prototype think about refactoring and installation of a script

parser = argparse.ArgumentParser(description="Codeforces automatization tool.")

subparsers = parser.add_subparsers(dest="command")

TEMPLATE_PATH = "cf_template.cpp"
BUILD_OPTIONS = "-Wall -g0 -O0 --std=c++20"
DEFINE_MULTILINE_TEST = "-DMULTILINE_TEST"


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


def get_sample_test(problem_dir):
	'''Fetches sample test for a problem. Running cf-auto create <problem> is required.'''
	contest_id, problem_letter = extract_problem_from_path(problem_dir)

	print("Fetching tests for problem:", contest_id, problem_letter)
	# TODO: parse "codeforces.com/contest/<contest_id>/<problem_letter>"
	# TODO: if the problem has multiline tests THEN add "-DMULTILINE_TEST" to "BUILD_OPTIONS"


def get_problem_list(contest_id):
	# TODO: fetch actual problem list for a given contest.
	fetched_problems = ["A", "B", "C", "D"]

	return fetched_problems


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
	practice_problem_dir = f"./practice/{contest_id}_{problem_letter}"
	contest_problem_dir = f"./{contest_id}/{problem_letter}"

	practice_dir_is_valid = os.path.isdir(practice_problem_dir)
	contest_dir_is_valid = os.path.isdir(contest_problem_dir)

	if practice_dir_is_valid and contest_dir_is_valid:
		print("Problem directory isn't unique:")
		print("(1) ", practice_problem_dir, "\n", "(2) ", contest_problem_dir, sep='')

		option = int(input("Choose on of given options: type 1 or 2\n"))
		if option == 1:
			return practice_problem_dir
		elif option == 2:
			return contest_problem_dir
		
		print("Invalid option is choosen.")
		return None
	elif contest_dir_is_valid or practice_dir_is_valid:
		return practice_problem_dir if practice_dir_is_valid else contest_problem_dir
	else:
		print(f"No valid directory is found for a problem {contest_id}{problem_letter}")
		return None



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
		argument("mode", help="[contest] C | [problem] P"),
		argument("contest", help="contest ID", type=str),
		argument("problem", help="problem letter", nargs='?', default="", type=str)
	],
	parent = subparsers
)
def create(args):
	'''Creates a structured folders and parses test samples into "in.txt"'''

	practice_mode_on = args.mode == 'P'
	contest_id       = args.contest
	problem_letter   = args.problem if args.problem != "" else None

	if (practice_mode_on and problem_letter is None):
		print("No full problem name provided -- unable to create a problem directory.")
		return
		
	parent_dir = "practice" if practice_mode_on else contest_id
	if (not os.path.exists(parent_dir)):
			system(f"mkdir {parent_dir}")

	problems = \
		[problem_letter.upper()] if practice_mode_on else get_problem_list(contest_id)

	for problem_letter in problems:
		problem_name = contest_id + problem_letter
		parent_dir_sufix = contest_id + "_" + problem_letter if practice_mode_on else problem_letter

		problem_dir = os.path.join(parent_dir, parent_dir_sufix)
		
		files = \
			["in.txt","out.txt","ans.txt",f"{problem_name}.cpp"]
		files_to_create = \
			" ".join([os.path.join(problem_dir, file) for file in files])
		
		if (not os.path.exists(problem_dir)):
			system(f"mkdir {problem_dir}")
			system(f"touch {files_to_create}")
			if not TEMPLATE_PATH is None and os.path.exists(TEMPLATE_PATH):
				system(f"cat {TEMPLATE_PATH} > {os.path.join(problem_dir, f"{problem_name}.cpp")}")
			get_sample_test(problem_dir)
		else:
			print(f"The directory {problem_dir} already exists. Nothing is changed.")
			break


	# TODO: get sample tests by implementing get_sample_test function
	

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

