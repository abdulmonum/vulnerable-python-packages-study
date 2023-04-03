import sys, os
import subprocess
import json
import csv
from time import sleep


TOP_DIR = "/home/s33khan/Documents/woc_project/vulnerable-python-packages-study/output/requirements"
CSV_PATH = "/home/s33khan/Documents/woc_project/vulnerable-python-packages-study/output/data.csv"
HEADER = ["Project","Author","Time","Timezone","Scanned Packages","Packages Count", "Vulnerabilities Count", "Vulnerability ID","Vulnerable Package","Vulnerable Spec","Analyzed Version","CVE"]

def escape_file_path(filepath):

    filepath = filepath.replace(" ", "\\ ")
    filepath = filepath.replace(">", "\\>")
    filepath = filepath.replace("<", "\\<")
    filepath = filepath.replace(")", "\\)")
    filepath = filepath.replace("(", "\\(")
    filepath = filepath.replace("'", "\\'")


    return filepath

def get_scanned_packages_with_verisons(obj):
    
    return_string = ""

    for package in obj:
        if return_string != "":
            return_string = return_string + "_"
        return_string = return_string + obj[package]["name"] + ":" + obj[package]["version"]

    return return_string

def addRowToCSV(row):
    global CSV_PATH

    with open(CSV_PATH, "a") as f:
        writer = csv.writer(f)

        writer.writerow(row)

def main():
    global TOP_DIR, HEADER


    # Extracting project names
    project_names = os.listdir(TOP_DIR)


    count = 0
    non_empty = 0

    addRowToCSV(HEADER)

    for project_name in project_names:
        


        commit_infos = os.listdir(TOP_DIR + "/" + project_name)

        if commit_infos == []:
            count = count + 1
            continue

        

        for commit_info in commit_infos:

            time = commit_info.split("_")[0]
            timezone = commit_info.split("_")[1]
            author = commit_info.split("_")[2]

            while(1):
                try:
                    stream = os.popen("cat " + TOP_DIR + "/" + project_name + "/" + escape_file_path(commit_info) + " | safety check --stdin --output json")
                    output = stream.read()
                    obj = json.loads(output)
                    break

                except:
                    print("Safety did not return correct data: " + output)
                    print("project name: " + project_name)
                    print("commit info: " + commit_info)
                    sleep(10)

            scanned_packages = get_scanned_packages_with_verisons(obj["scanned_packages"])
            packages_count = obj["report_meta"]["packages_found"]
            vulnerabilities_count = obj["report_meta"]["vulnerabilities_found"]


            for vuln in obj["vulnerabilities"]:
                vuln_id = vuln["vulnerability_id"]
                vuln_package = vuln["package_name"]
                vuln_spec = vuln["vulnerable_spec"]
                analyzed_version = vuln["analyzed_version"]
                cve = vuln["CVE"]

                row = [project_name, author, time, timezone, scanned_packages, packages_count, vulnerabilities_count, vuln_id, vuln_package, vuln_spec, analyzed_version, cve]

                addRowToCSV(row)

            if int(vulnerabilities_count) == 0:
                row = [project_name, author, time, timezone, scanned_packages, packages_count, vulnerabilities_count]

                addRowToCSV(row)


            

        
        print("Project " + str(count) + " Done...")
        print("Project Name: " + project_name)
        count = count + 1


    
    

if __name__ == "__main__":
    try:

        main()
    
    except KeyboardInterrupt:
        print(f'\nUnexpected Error: {KeyboardInterrupt}.\nShutting Down...')
        
        sys.exit(0)
