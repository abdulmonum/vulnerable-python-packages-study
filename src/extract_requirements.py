import sys, os
from oscar import Project, Commit, Blob, Commit, Tree
import re
import pickle



def loadMap(filepath):
    with open(filepath, 'rb') as f:
        return pickle.load(f)

def make_proj_directory(name):
    path = "/home/amonum/vulnerable-python-packages-study/output/requirements/" + name
    try:
        os.mkdir(path)
    except:
        pass  
    return path

def extract_attributes_of_commit(commit_shas):
    attributes = Commit(commit_shas).attributes
    time = attributes[0]
    tz = attributes[1]
    author = attributes[2]
    tree = attributes[3]
    return (time, tz, author, tree)

def extract_blob_of_tree(tree_shas):
    files = Tree(tree_shas).files
    for filename, blob_shas in files.items():
        if re.search("requirements", filename.decode('utf-8')):
            # print("blob: ", blob_shas)
            data = Blob(blob_shas).data
            # print("data: ",data.decode('utf-8'))
            return data.decode('utf-8')
    return None

def write_file_to_project_folder(path, attr, data):
    if data != None:
        filename = str(attr[0]) + "_" + str(attr[1]) + "_" + str(attr[2])
        # print("filename:", filename)
        completeName = os.path.join(path, filename+".txt")
        file1 = open(completeName, "w")
        file1.write(data)
        file1.close()
    # print("should be done")   

def main():
    for x in range(4,11): 
        path = "/home/amonum/vulnerable-python-packages-study/output/project_commit_map_" + str(x) + ".pkl"
        project_commit_dict = loadMap(path)
        print(x, "pikl file ---------")
        
        for name, commits in project_commit_dict.items():
            print("Project Name:", name)
            print("Number of commits: ", len(commits))
            path = make_proj_directory(name)

            for commit in commits:
                # print("commit:", commit)
                try:
                    attr = extract_attributes_of_commit(commit)
                    data = extract_blob_of_tree(attr[3])
                    write_file_to_project_folder(path, attr, data)
                except:
                    # print("skipped")
                    pass
        # create_project_commit_map(project_names)


    

if __name__ == "__main__":
    try:

        main()
    
    except KeyboardInterrupt:
        print(f'\nUnexpected Error: {KeyboardInterrupt}.\nShutting Down...')
        
        sys.exit(0)