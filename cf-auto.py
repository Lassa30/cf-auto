import os
import argparse
from typing import Optional
from cf import utils
from cf.scrapper import init_scrapper


parser = argparse.ArgumentParser(description="Codeforces automatization tool.")
subparsers = parser.add_subparsers(dest="command")
scrapper = init_scrapper()


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
        argument("problem", help="problem letter", nargs="?", default="", type=str),
    ],
    parent=subparsers,
)
def create(args):
    '''Creates a structured folders and parses test samples into "in.txt"'''

    contest_id = args.contest
    problem_id: Optional[str] = args.problem if args.problem != "" else None

    if args.mode == "P" and problem_id is None:
        print("No full problem name provided -- unable to create a problem directory.")
        return

    match (args.mode):
        case "C":
            utils.create_contest(contest_id, scrapper)
        case "P":
            utils.create_practice_problem(contest_id, problem_id, scrapper)
        case _:
            print(f'Wrong create mode: {args.mode}. Expected "P" or "C".')


@subcommand(
    [
        argument("contest", help="contest ID", type=str),
        argument("problem", help="problem letter", type=str),
    ],
    parent=subparsers,
)
def run(args):
    """Build and run a file if it exists."""

    contest_id = args.contest
    problem_id = args.problem.upper()

    problem_dir = utils.find_valid_directory(contest_id, problem_id)
    if not problem_dir:
        print("error in find_valid_directory")
        return
    sep = "_" if (problem_dir.find("practice") != -1) else ""

    problem_name = sep.join((contest_id, problem_id))
    problem_path = os.path.join(problem_dir, problem_name)

    input_file, output_file, answer_file = utils.get_in_out_ans(problem_dir)
    utils.build_and_run(problem_path, input_file, answer_file)
    utils.check_solution(output_file, answer_file)


def main():
    try:
        args = parser.parse_args()
        if args.command is None:
            parser.print_help()
        else:
            args.func(args)
    except Exception as e:
        raise e
    finally:
        scrapper.driver_quit()


if __name__ == "__main__":
    main()
