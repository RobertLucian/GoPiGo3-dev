import json
import argparse
from collections import OrderedDict

global parser
def parseArguments():
    parser = argparse.ArgumentParser(description="Read commits and determine the next release number along with creating the changelog.")
    parser.add_argument("release", metavar="last-release", type=str,
                       help="the last release value")
    parser.add_argument("commit", metavar="commit-filename", type=str,
                        help="name of the file containing the summary & body of each commit")
    parser.add_argument("output", metavar="changelog-output", type=str,
                        help="json-ready file to be sent to github for releasing the next version")
    parser.add_argument('--verbose', '-v', action='count', default = 0,
                        help="up to 2 levels of verbosity")
    args = parser.parse_args()

    return args.release, args.commit, args.output, args.verbose


def analyzeCommits(filename):
    logs = []
    changelogs = OrderedDict(
        type = [],
        scope = [],
        summary = [],
        body = [],
        breakingchange = [],
        size = 0
    )

    with open(filename) as log:
        found_at_sign = None
        found_body = False
        stop_adding_body = False
        found_breakingchange = False

        for line in log:
            logs.append(line)

            if "@" in line:
                title, short_summary = line.split("@")[1].split(":")
                type_commit = title[0:title.find("(")]
                scope_commit = title[title.find("(") + 1:title.find(")"):]
                short_summary = short_summary.lstrip().rstrip()

                changelogs["type"].append(type_commit)
                changelogs["scope"].append(scope_commit)
                changelogs["summary"].append(short_summary)
                changelogs["breakingchange"].append("")
                changelogs["size"] += 1

                found_at_sign = True
                found_body = False
                stop_adding_body = False
                stop_adding_to_breakingchange = False
                found_breakingchange = False

            elif found_at_sign is not None:
                if line != "\r\n" and line != "\n":
                    if found_body is False:
                        found_body = True
                        line = line.lstrip().rstrip()
                        changelogs["body"].append(line)
                    else:
                        if stop_adding_body is False:
                            line = line.lstrip().rstrip()
                            changelogs["body"][-1] += " " + line
                        else:
                            line = line.lstrip().rstrip()
                            if "BREAKING CHANGE" in line:
                                found_breakingchange = True
                                line = line.split(":")[1].lstrip()
                            if found_breakingchange is True and stop_adding_to_breakingchange is False:
                                if len(changelogs["breakingchange"][-1]) > 0:
                                    changelogs["breakingchange"][-1] += " "
                                changelogs["breakingchange"][-1] += line
                else:
                    stop_adding_body = found_body
                    if found_breakingchange is True:
                        stop_adding_to_breakingchange = True

    return changelogs

def nextRelease(last_release, commits):
    # getting rid of the 'v' letter in front of the version
    last_release = last_release[1:]

    major, minor, patch = map(lambda x: int(x), last_release.split('.'))

    breakingchange_list = list(filter(lambda x: len(x) > 0, commits["breakingchange"]))

    if len(breakingchange_list) > 0:
        major += 1
        minor = 0
        patch = 0
    elif "feature" in commits["type"]:
        minor += 1
        patch = 0
    elif len(commits["type"]) > 2:
        patch += 1

    return "v{}.{}.{}".format(major, minor, patch)

def makeChangelog(commits):
    apparitions = OrderedDict()
    apparitions["feature"] = []
    apparitions["fix"] = []
    apparitions["breakingchange"] = []
    apparitions["docs"] = []
    apparitions["refactor"] = []
    apparitions["test"] = []
    apparitions["chore"] = []

    size = commits["size"]

    for index in range(size):
        apparitions[commits["type"][index]].append(index)

    breakingchange_apparitions = list(enumerate(commits["breakingchange"]))
    for supposed_occurrence in breakingchange_apparitions:
        if len(supposed_occurrence[1]) > 0:
            apparitions["breakingchange"].append(supposed_occurrence[0])

    changelog = ""
    for key, value in apparitions.items():
        if len(value) > 0:
            if key != "breakingchange":
                changelog += "### {}\n\n".format(key.title())
                for index_item in value:
                    changelog += "* **{}**: {} **->** {}\n".format(commits["scope"][index_item],
                                                        commits["summary"][index_item],
                                                        commits["body"][index_item])
            else:
                changelog += "### Breaking Change\n"
                for index_item in value:
                    changelog += "* {}\n".format(commits["breakingchange"][index_item])
            changelog += "\n"

    return changelog

def main():
    last_release, commit_filename, output_filename, verbosity = parseArguments()

    commits = analyzeCommits(commit_filename)
    new_release = nextRelease(last_release, commits)

    if last_release != new_release:
        changelog = makeChangelog(commits)

        if verbosity == 0:
            print(new_release)
        elif verbosity == 1:
            print("old release: {}".format(last_release))
            print("new release: {}".format(new_release))
        if verbosity == 2:
            print("commits organized: ")
            print(json.dumps(commits, indent=2, sort_keys=False))
            print("changelog: ")
            print(changelog)

        github_json_data = dict(
            tag_name = new_release,
            target_commitish = "master",
            name = new_release,
            body = changelog,
            draft = False,
            prerelease = False
        )
        github_data_json_dump = json.dumps(github_json_data, indent=2, sort_keys=False)
        with open(output_filename, "w") as f:
            f.write(github_data_json_dump)

if __name__ == "__main__":
    main()
