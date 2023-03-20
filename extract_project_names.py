import re
import sys

def extract_project_names(filename):
    with open(filename) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    project_names = []
    for line in content:
        project_name = ""
        if line.find("https://github.com") != -1:
            url = re.findall(r'(https?://\S+)', line)[0]
            if url.find(").*") != -1:
                continue
            project_name = url[19:-1]
            project_name = project_name.replace("/", "_")
            project_names.append(project_name)

    for i in range(4):
        project_names.pop(-1)

    return project_names


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 extract_project_names.py <filename>")
        sys.exit(1)
    filename = sys.argv[1]
    project_names = extract_project_names(filename)

    #write project_names to file "project_names.txt"
    with open("project_names.txt", "w") as f:
        for project_name in project_names:
            f.write(project_name + "\n") 

    

if __name__ == "__main__":
    main()