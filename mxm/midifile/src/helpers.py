import os, os.path, sys

def getdir(fname='', toplevel='examples'):
    "returns the full path to fname in the importdata directory'"
    if __name__ == '__main__':
        filename = sys.argv[0]
    else:
        filename = __file__
    current_path = os.path.abspath(os.path.dirname(filename))
    parent_path = os.path.split(current_path)[0]
    parent_path = os.path.join(parent_path, toplevel)
    return os.path.join(parent_path, fname)

def exampledir(fname=''):
    "returns the full path to the file in the 'examples' dir."
    return getdir(fname=fname, toplevel='examples')

def testdir(fname=''):
    "returns the full path to the file in the 'tests' dir."
    return getdir(fname=fname, toplevel='tests')

