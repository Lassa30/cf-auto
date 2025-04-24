import os
from os import system
from cf import constants
from cf import scraping


def get_in_out_ans(contest_id):
    input_file = os.path.join(contest_id, "in.txt")
    output_file = os.path.join(contest_id, "out.txt")
    answer_file = os.path.join(contest_id, "ans.txt")
    return input_file, output_file, answer_file


def check_solution(output_file, answer_file):
    """Compares out.txt with ans.txt and highlights differences."""

    with open(output_file, "r") as f1, open(answer_file, "r") as f2:
        output_lines = f1.readlines()
        answer_lines = f2.readlines()

    output_lines = [line.rstrip() for line in output_lines]
    answer_lines = [line.rstrip() for line in answer_lines]

    if len(output_lines) != len(answer_lines):
        has_less_lines = (
            output_lines if len(output_lines) < len(answer_lines) else answer_lines
        )
        has_more_lines = (
            output_lines if len(output_lines) > len(answer_lines) else answer_lines
        )
        while len(has_less_lines) < len(has_more_lines):
            has_less_lines.append("<empty_line>")

    if output_lines == answer_lines:
        print("Correct answer.")
        return

    for i, (out_line, ans_line) in enumerate(zip(output_lines, answer_lines), start=1):
        if out_line != ans_line:
            print(
                f"Difference at line {i}:\n"
                + f"\tExpected: `{out_line}`\n"
                + f"\tFound:    `{ans_line}`"
            )


def find_valid_directory(contest_id, problem_letter):
    practice_contest_id = f"./practice/{contest_id}_{problem_letter}"
    contest_contest_id = f"./{contest_id}/{problem_letter}"

    practice_dir_is_valid = os.path.isdir(practice_contest_id)
    contest_dir_is_valid = os.path.isdir(contest_contest_id)

    if practice_dir_is_valid and contest_dir_is_valid:
        print("Problem contest_id isn't unique:")
        print("(1) ", practice_contest_id, "\n", "(2) ", contest_contest_id, sep="")

        option = int(input("Choose one of given options: type 1 or 2\n"))
        if option == 1:
            return practice_contest_id
        elif option == 2:
            return contest_contest_id

        print("Invalid option is choosen.")
        return None
    elif contest_dir_is_valid or practice_dir_is_valid:
        return practice_contest_id if practice_dir_is_valid else contest_contest_id
    else:
        print(
            f"No valid contest_id is found for a problem {contest_id}{problem_letter}"
        )
        return None


def extract_problem_from_path(contest_id):
    split_contest_id = os.path.split(contest_id)
    if split_contest_id[0] == "practice":
        split_problem_name = split_contest_id[-1].split("_")
        contest_id = split_problem_name[-2]
        problem_letter = split_problem_name[-1]
    else:
        contest_id = split_contest_id[-2]
        problem_letter = split_contest_id[-1]
    return (contest_id, problem_letter)


def build_and_run(problem_path, input_file, output_file):
    build_command = (
        f"g++ {constants.BUILD_OPTIONS} -o {problem_path} {problem_path}.cpp"
    )

    print("-" * 60)

    system(
        f"\
        {build_command} && \
        (./{problem_path} < {input_file}) | tee {output_file}"
    )

    print("\n" + "-" * 60)
    return


def write_to(path, text):
    try:
        with open(path, "w") as file:
            file.write(text)
    except Exception as e:
        raise e


def get_files_to_create(problem_dir, problem_name):
    files = ["in.txt", "out.txt", "ans.txt", f"{problem_name}.cpp"]
    get_file_path = lambda file: os.path.join(problem_dir, file)
    return " ".join([get_file_path(file) for file in files])


def create_practice_problem(contest_id, problem_id):
    scraper = scraping.Scraper()

    problem_name = "_".join([contest_id, problem_id])
    problem_dir = os.path.join("./practice", problem_name)
    problem_path = os.path.join(problem_dir, problem_name)
    problem_url = scraping.make_problem_url(contest_id, problem_id)

    files = get_files_to_create(problem_dir, problem_name)
    system(f"mkdir -p ./practice")

    if not os.path.exists(problem_dir):
        system(f"mkdir -p {problem_dir}")
        system(f"touch {files}")
        write_to(problem_path + ".cpp", read_from(constants.TEMPLATE_PATH))

        test_input, test_output = scraper.get_test_cases(problem_url)

        write_to(os.path.join(problem_dir, "in.txt"), test_input)
        write_to(os.path.join(problem_dir, "out.txt"), test_output)
    else:
        print("create_practice_problem", contest_id, problem_id, "is already present")


def create_contest(contest_id):
    scraper = scraping.Scraper()
    contest_url = scraping.make_contest_url(contest_id)
    problems_list = scraper.get_problem_list(contest_url)

    if not os.path.exists(contest_id):
        system(f"mkdir {contest_id}")
        for problem_id in problems_list:
            create_problem(contest_id, problem_id, scraper)
    else:
        print(f"The directory {contest_id} already exists. Nothing is changed.")


def create_problem(contest_id, problem_id, scraper: scraping.Scraper):
    problem_dir = f"{contest_id}/{problem_id}"
    problem_name: str = contest_id + problem_id

    files = get_files_to_create(problem_dir, problem_name)
    system(f"mkdir -p {problem_dir}")
    system(f"touch {files}")
    write_to(
        os.path.join(problem_dir, f"{problem_name}.cpp"),
        read_from(constants.TEMPLATE_PATH),
    )
    problem_url = scraping.make_problem_url(contest_id, problem_id)
    test_input, test_output = scraper.get_test_cases(problem_url)

    write_to(os.path.join(problem_dir, "in.txt"), test_input)
    write_to(os.path.join(problem_dir, "out.txt"), test_output)


def read_from(path):
    try:
        with open(path, "r") as file:
            return file.read()
    except Exception as e:
        raise e
