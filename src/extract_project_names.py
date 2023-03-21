import re
import sys, os


# Method to parse awesome-python README and extract github project names
def extract_project_names(filename):
    with open(filename) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    project_names = []
    for line in content:
        project_name = ""
        if "https://github.com" in line:
            url = re.findall(r'(https:\/\/github\S+)', line)[0]
            if url.find(").*") != -1:
                continue
            project_name = url[19:-1].replace("/", "_")
            if(project_name[-1]) == '_' or project_name[-1] == ')':
                project_name = project_name[:-1]
            project_names.append(project_name)


    #remove irrelevant github repo links
    for i in range(2):
        project_names.pop(0)
    
    for i in range(4):
        project_names.pop(-1)

    return project_names


# Method to output content to a file
def outputToFile(filepath, content):

    with open(filepath, 'w') as f:
        f.write(content)


def main(filepath):
    
    project_names = extract_project_names(filepath)

    outputToFile('/home/amonum/vulnerable-python-packages-study/output/project_names.txt', "\n".join(project_names))




if __name__ == "__main__":
    try:
        # Input validation
        if len(sys.argv) != 2:
            print("Usage: python3 extract_project_names.py <full-path-to-file>")
            sys.exit(1)
        if os.path.exists(sys.argv[1]) == False:
            print("The following path to file does not exist:", sys.argv[1])
            print("Usage: python3 extract_project_names.py <full-path-to-file>")
            sys.exit(1)

        main(sys.argv[1])
    
    except KeyboardInterrupt:
        print(f'\nUnexpected Error: {KeyboardInterrupt}.\nShutting Down...')
        
        sys.exit(0)
