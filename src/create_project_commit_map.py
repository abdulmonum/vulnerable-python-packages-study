import sys, os
from oscar import Project, Commit
import re
import pickle


def printProgress(total, current):
    if current/total >= 0.9:
        return "90% Projects Processed..."
    elif current/total >= 0.8:
        return "80% Projects Processed..."
    elif current/total >= 0.7:
        return "70% Projects Processed..."
    elif current/total >= 0.6:
        return "60% Projects Processed..."
    elif current/total >= 0.5:
        return "50% Projects Processed..."
    elif current/total >= 0.4:
        return "40% Projects Processed..."
    elif current/total >= 0.3:
        return "30% Projects Processed..."
    elif current/total >= 0.2:
        return "20% Projects Processed..."
    elif current/total >= 0.1:
        return "10% Projects Processed..."
    else:
        return "0% Projects Processed..."
            

def loadProjectNames(filepath):
    output = None

    with open(filepath, 'r') as f:
        output = f.read().splitlines()

    return output


def dumpMapToFile(filepath, output_map):
    with open(filepath, 'wb') as f:
        pickle.dump(output_map, f)


def loadMap(filepath):
    with open(filepath, 'rb') as f:
        return pickle.load(f)


def create_project_commit_map(project_names):

    project_commit_map = {}

    total_projects = len(project_names)

    current_project_number = 1
    current_outputfile_number = 1
    current_progress_string = ""

    for project_name in project_names:
        
        # Get project commits
        project_commits = [Commit(commitcd ..) for commit in Project(project_name).commit_shas]

        commits_with_requirements = []

        for project_commit in project_commits:

            # Save commits related to requirements.txt only
            filenames = []
            try:
                filenames = [filename.decode('utf-8') for filename in project_commit.changed_file_names]

            except:
                pass
            
            # Regular expression to match any filename that contains requirements in the prefix
            # along with other alphanumeric characters, hyphen, or underscore and ends with .txt
            r = re.compile('^[\w\_\-\/]*requirements[\w\_\-]*\.txt')

            if list(filter(r.match, filenames)) != []:
                commits_with_requirements.append(project_commit.sha)

        # Add project to map if there exists atleast one commit in commits_with_requirements
        if commits_with_requirements != []:
            project_commit_map[project_name] = commits_with_requirements


        # Progress logging and data dumping
        progress_string = printProgress(total_projects, current_project_number)

        if current_progress_string != progress_string:
            current_progress_string = progress_string
            print(current_progress_string)
            dumpMapToFile('/home/amonum/vulnerable-python-packages-study/output/project_commit_map_' + str(current_outputfile_number) + '.pkl', project_commit_map)
            project_commit_map.clear()
            current_outputfile_number = current_outputfile_number + 1

        current_project_number = current_project_number + 1
        print("Project Number:", current_project_number)
    
    
    print("100% Projects Processed...")   
    # return project_commit_map





def main():
    project_names = loadProjectNames('/home/amonum/vulnerable-python-packages-study/output/project_names.txt')
        
    create_project_commit_map(project_names)


    

if __name__ == "__main__":
    try:

        main()
    
    except KeyboardInterrupt:
        print(f'\nUnexpected Error: {KeyboardInterrupt}.\nShutting Down...')
        
        sys.exit(0)