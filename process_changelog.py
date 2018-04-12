import json
import argparse
import re
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
    summary = OrderedDict(
        type = [],
        scope = [],
        summary = [],
        body = [],
        breakingchange = [],
        size = 0
    )

    # example of a element stored in the json file
    # {
    #   "commit-hash": "11d07df4ce627d98bd30eb1e37c27ac9515c75ff",
    #   "abbreviated-commit-hash": "11d07df",
    #   "author-name": "Robert Lucian CHIRIAC",
    #   "author-email": "robert.lucian.chiriac@gmail.com",
    #   "author-date": "Sat, 27 Jan 2018 22:33:37 +0200",
    #   "subject": "@fix(automation): patch versions aren't released",
    #   "sanitized-subject-line": "fix-automation-patch-versions-aren-t-released",
    #   "body": "Nothing else to add. Fixes #24.",
    #   "commit-notes": ""
    # }
    with open(filename) as filelog:
        changelog = json.load(filelog)

        for index in range(len(changelog)):
            subject = changelog[index]["subject"].replace('\n',' ').lstrip().rstrip()
            body = changelog[index]["body"].lstrip().rstrip()

            # pattern sample: "@fix(automation): patch versions aren't released"
            pattern_subject = re.compile("^(@)(\w*)([(])(\w*)([):]{2})(\s)(.*)$")
            components_subject = pattern_subject.findall(subject)

            if len(components_subject) > 0:
                # it means we found the pattern in the subject of the commit message
                # and take out the tuple out of the list
                components_subject = components_subject[0]
                summary["type"].append(components_subject[1])
                summary["scope"].append(components_subject[3])
                summary["size"] += 1

    return summary

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
    elif len(commits["type"]) > 0:
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
