# imports
import random
import os
import subprocess
import time

# Constants

TEXT_FILE_PATH = "text.txt"

COAUTHOR_1 = "Co-authored-by: matg890517-art <mat.g.890517@gmail.com>"
COAUTHOR_2 = "Co-authored-by: anthonycastro0405 <second-co-author-yukitanaka7070@gmail.com>"

COMMIT_MESSAGE = f"""
Added a small change to {TEXT_FILE_PATH}

## Type of change
<!-- Please select the desired item checkbox and change it from `[ ]` to `[x]` and then delete the irrelevant options. -->
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Improvement (refactoring and improving code)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Description
<!--
  Please include a summary of the change and which issue is fixed. 
  Please also include relevant motivation and context. 
  List any dependencies that are required for this change.
-->

## Additional context
<!-- e.g. Fixes #(issue) -->


{COAUTHOR_1}
{COAUTHOR_2}"""

# First Make a new branch with a meaningful name that dont looks like its a random branch

def gen_branch_name():
    # get a dictionary of words
    word_1 = ["space", "moon", "star", "planet", "galaxy", "universe", "comet", "asteroid", "blackhole", "wormhole", "nebula", "quasar", "pulsar", "supernova", "darkmatter", "lightyear", "gravity", "orbit", "cosmos", "void", "dimension", "time", "energy", "matter", "radiation", "singularity", "eventhorizon", "spacetime", "multiverse", "paralleluniverse", "extraterrestrial", "alien", "lifeform", "intelligence", "civilization", "technology", "robotics", "artificialintelligence", "machinelearning", "neuralnetwork", "quantumcomputing"]
    word_2 = ["exploration", "discovery", "adventure", "journey", "mission", "expedition", "voyage", "quest", "odyssey", "pilgrimage", "safari", "crusade", "trek", "sojourn", "wanderlust", "roaming", "traveling", "wandering", "drifting", "floating", "gliding", "soaring", "flying", "hovering", "levitating", "ascending", "descending", "climbing", "scaling", "mountaineering"]
    word_3 = ["explorer", "adventurer", "traveler", "wanderer", "nomad", "pilgrim", "journeyman", "wayfarer", "roamer", "drifter", "globetrotter", "voyager", "pioneer", "trailblazer", "pathfinder", "navigator", "scout", "seeker", "quester", "expeditionist", "explorator", "discoverer", "investigator", "researcher", "scientist", "scholar", "academic", "intellectual", "thinker", "philosopher", "theorist", "visionary", "futurist", "innovator", "inventor", "creator", "artist", "designer", "engineer"]
    
    # generate a random number of 4 digits
    
    suffix = random.randint(1000, 9999)
    
    # generate a random word with the first, secon, and third word and the suffix
    branch_name = f"{random.choice(word_1)}-{random.choice(word_2)}-{random.choice(word_3)}-{suffix}"
    
    return str(branch_name)

#  Now create a branch with that name
def create_branch(branch_name):
    # check if the branch already exists
    branches = subprocess.check_output(["git", "branch"]).decode("utf-8").split("\n")
    if branch_name in branches:
        print(f"Branch {branch_name} already exists")
        return False
    
    # create the branch
    subprocess.call(["git", "checkout", "-b", branch_name])
    print(f"Branch {branch_name} created")
    return True

# create a function to switch to a specific branch
def switch_branch(branch_name):
    # check if the branch exists
    branches = subprocess.check_output(["git", "branch"]).decode("utf-8").split("\n")
    if branch_name not in branches:
        print(f"Branch {branch_name} does not exist")
        return False
    
    # switch to the branch
    subprocess.call(["git", "checkout", branch_name])
    print(f"Switched to branch {branch_name}")
    return True

# a function to run a command in the terminal and also print the output
def run_command(command):
    # run the command
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    # print the output
    print(result.stdout)
    
    # check if there was an error
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    
    return True

# create a function to create a file with the name text.txt
def create_file(file_path):
    # check if the file already exists
    if os.path.exists(file_path):
        print(f"File {file_path} already exists")
        return False
    
    # create the file
    with open(file_path, "w") as f:
        f.write("This is a test file")
    
    print(f"File {file_path} created")
    return True

# make a function to add a small change to the text file
def add_change_to_text_file(file_path):
    # check if the file exists
    create_file(file_path)

    # add a small change to the file
    with open(file_path, "a") as f:
        f.write("\nThis is a small change")
    
    print(f"Small change added to {file_path}")
    return True


def main():
    # generate a branch name
    branch_name = gen_branch_name()
    
    # create the branch
    create_branch(branch_name)

    
    # add a small change to the text file
    add_change_to_text_file(TEXT_FILE_PATH)
    
    # add the file to git
    run_command("git add .")
    
    # commit the changes with a message
    subprocess.run(["git", "commit", "-m", COMMIT_MESSAGE], check=True)
    
    # push the changes to the remote repository
    run_command(f"git push origin {branch_name}")
    
    # create a pull request with the changes to the new branch and the main branch
    run_command(f'gh pr create --base main --head {branch_name} --fill')
    
    #  merge the pull request
    run_command(f'gh pr merge {branch_name} --squash')
    
    run_command("git checkout main")

if __name__ == "__main__":
    loopturns = int(input("How many times do you want to run the script? "))
    # time delay to prevent rate limiting max 100 seconds
    time_delay = int(input("How long do you want to wait between runs? (in seconds) "))
    if time_delay < 100:
        time_delay = 100
    for i in range(loopturns):
        main()
        print(f"Finished run {i+1} of {loopturns}")
        if i < loopturns - 1:
            print(f"Waiting {time_delay} seconds before next run")
            time.sleep(time_delay)