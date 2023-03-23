import pickle
import pprint


def loadMap(filepath):
    with open(filepath, 'rb') as f:
        return pickle.load(f)

def main():

    d = loadMap('/home/amonum/vulnerable-python-packages-study/output/project_commit_map_4.pkl')

    pp = pprint.PrettyPrinter(width=41, compact=True)
    pp.pprint(d)

main()