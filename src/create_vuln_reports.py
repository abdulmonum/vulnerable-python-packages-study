import sys, os
import subprocess
import json
import csv
from time import sleep


TOP_DIR = "/home/s33khan/Documents/woc_project/vulnerable-python-packages-study/output/requirements"
CSV_PATH = "/home/s33khan/Documents/woc_project/vulnerable-python-packages-study/output/data.csv"
HEADER = ["Project","Author","Time","Timezone","Scanned Packages","Packages Count", "Vulnerabilities Count", "Vulnerability ID","Vulnerable Package","Vulnerable Spec","Analyzed Version","CVE"]
# HEADER = ["Project","Author","Time","Timezone","Scanned Packages","Packages Count", "Vulnerabilities Count", "Vulnerability Info"]

def escape_file_path(filepath):

    filepath = filepath.replace(" ", "\\ ")
    filepath = filepath.replace(">", "\\>")
    filepath = filepath.replace("<", "\\<")
    filepath = filepath.replace(")", "\\)")
    filepath = filepath.replace("(", "\\(")
    filepath = filepath.replace("'", "\\'")

    # "1409143463_+0300_Theodoros Giannakopoulos <tyiannak@gmail.com>"
    # "1409143463_+0300_Theodoros_Giannakopoulos_tyiannak@gmail.com"

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

    # print(os.listdir(TOP_DIR))

    # Extracting project names
    project_names = os.listdir(TOP_DIR)

    # print(os.listdir(TOP_DIR + "/" + all_project_names[0]))

    count = 0
    non_empty = 0

    addRowToCSV(HEADER)

    for project_name in project_names:
        
        # print(str(count) + " " + project_name)
        # count = count + 1
        # continue

        if count < 23:
            count = count + 1
            continue

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

            # print(output)
            # print("project name: " + project_name)
            # print("commit info: " + commit_info)
            scanned_packages = get_scanned_packages_with_verisons(obj["scanned_packages"])
            packages_count = obj["report_meta"]["packages_found"]
            vulnerabilities_count = obj["report_meta"]["vulnerabilities_found"]

            # vuln_info = ""

            for vuln in obj["vulnerabilities"]:
                vuln_id = vuln["vulnerability_id"]
                vuln_package = vuln["package_name"]
                vuln_spec = vuln["vulnerable_spec"]
                analyzed_version = vuln["analyzed_version"]
                cve = vuln["CVE"]
                # advisory = vuln["advisory"].replace("\n", "")
                # advisory = advisory.replace("\r", "")

                # if vuln_info != "":
                #     vuln_info = vuln_info + ":"

                # vuln_info = vuln_info + str(vuln_id) + "_" + str(vuln_package) + "_" + str(vuln_spec) + "_" + str(analyzed_version) + "_" + str(cve)

                row = [project_name, author, time, timezone, scanned_packages, packages_count, vulnerabilities_count, vuln_id, vuln_package, vuln_spec, analyzed_version, cve]

                addRowToCSV(row)

            if int(vulnerabilities_count) == 0:
                # vuln_id = "NA"
                # vuln_package = "NA"
                # vuln_spec = "NA"
                # analyzed_version = "NA"
                # cve = "NA"
                # advisory = "NA"
                row = [project_name, author, time, timezone, scanned_packages, packages_count, vulnerabilities_count]

                addRowToCSV(row)


            

        
        print("Project " + str(count) + " Done...")
        print("Project Name: " + project_name)
        count = count + 1
        # print("scanned_packages: " + get_scanned_packages_with_verisons(obj["scanned_packages"]))


    
    # print("empty: ", empty)
    # print("non_empty: ", non_empty)

    # project_0 = os.listdir(TOP_DIR + "/" + all_project_names[0])

    # print(TOP_DIR + "/" + all_project_names[0] + "/" + project_0[0])
    # print(os.path.isfile(TOP_DIR + "/" + all_project_names[0] + "/" + project_0[0]))
    # print(TOP_DIR + "/" + all_project_names[0] + "/" + escape_file_path(project_0[0]))
    # print(os.path.isfile(TOP_DIR + "/" + all_project_names[0] + "/" + escape_file_path(project_0[0])))

    

    # print(subprocess.check_output("cat " + TOP_DIR + "/" + all_project_names[0] + "/" + "1409143463_+0300_Theodoros_Giannakopoulos_tyiannak@gmail.com.txt | safety check --stdin", stderr=subprocess.STDOUT, stdin=subprocess.PIPE, shell=True).decode("utf-8"))

    # stream = os.popen("cat " + TOP_DIR + "/" + all_project_names[0] + "/" + escape_file_path(project_0[0]) + " | safety check --stdin --output json")
    # output = stream.read()
    # print(output)

    # obj = json.loads(output)

    # print(obj["scanned_packages"])

    # print(type(output))


if __name__ == "__main__":
    try:

        main()
    
    except KeyboardInterrupt:
        print(f'\nUnexpected Error: {KeyboardInterrupt}.\nShutting Down...')
        
        sys.exit(0)