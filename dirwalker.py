# note: os.getcwd() returns the absolute path on OS X
import stat, os, pprint

"""
This module "walks" through the current working directory.

Current functionality:
- Return a dict that encodes the hierarchial structure
- Recursively print the directory, with lines indicating
parent/child relationships in the tree structure
- Recursively diff two directories
"""

def permissions_to_unix_name(st):
    """
    Translates a code given by Python into a UNIX-style permissions
    string. The output strings of this function look like the output
    lines of "ls -la"
    """
    is_dir = 'd' if stat.S_ISDIR(st.st_mode) else '-'
    dic = {'7':'rwx', '6' :'rw-', '5' : 'r-x', '4':'r--', '0': '---'}
    perm = str(oct(st.st_mode)[-3:])
    return is_dir + ''.join(dic.get(x,x) for x in perm)

def isdir(fh):
    """Returns true iff 'fh' is the name of a directory"""
    fh_st_mode = os.stat(fh)[0]
    return (fh_st_mode == 16877)

def print_dfs(root, tabstring="", ignore=list(), *args, **kwargs):
    """
    Do a depth-first traversal of the current working directory, and
    print the names of files in a tree hierarchy.
    """
    ls_out = os.listdir(root)
    for f in ls_out:
        fullpath = root + "/" + f
        cond = isdir(fullpath)
        if (cond and f not in ignore):
            print "{}\t|___ {}/".format(tabstring, f)
            if f is ls_out[-1]:
                print_dfs(fullpath, tabstring+'\t', ignore)
            else:
                print_dfs(fullpath, tabstring+'\t|', ignore)
        else:
            print "{}\t|___ {}".format(tabstring, f)

def walk_dfs(root, dir_contents=dict(), ignore=list(), *args, **kwargs):
    """
    This function does a depth-first traversal of the current working
    directory.
    """
    ls_out = os.listdir(root)
    for f in ls_out:
        dir_contents[f] = {}
        fullpath = root+"/"+f
        cond = isdir(fullpath)
        if (cond and f not in ignore):
            walk_dfs(fullpath, dir_contents[f], ignore)
    return dir_contents

def ddelta(root1, root2, tabstring="", *args, **kwargs):
    """
    Recursively diff two directories! This function accounts
    for files/subdirectories in one directory, but not the other.

    Future functionality: optionally check if directories have a file
    of the same name, but with different contents.
    """
    r1 = os.listdir(root1)
    r2 = os.listdir(root2)
    for f in r1:
        fullpath1 = root1+"/"+f
        fullpath2 = root2+"/"+f
        cond1 = isdir(fullpath1)
        cond2 = isdir(fullpath2)
        if f not in r2:
            print tabstring + "\t|___ {}".format(f)
            print_dfs(fullpath1, tabstring+'\t')

        # we know that f is in both r1 and r2...
        elif cond1:

            # f is a dir in both r1 and r2
            if cond2:
                print tabstring + "\t|___ {}".format(f)
                if f is r1[-1] and f is r2[-1]:
                    ddelta(fullpath1, fullpath2, tabstring+'\t')
                else:
                    ddelta(fullpath1, fullpath2, tabstring+'\t|')

            # f is a dir in r1 but not r2
            else:
                print tabstring + "\t|___ {}/ -> {}".format(f, f)
                if f is r1[-1]:
                    print_dfs(fullpath1, tabstring+'\t - ')
                else:
                    print_dfs(fullpath1, tabstring+'\t - |')

        # f is a dir in r2 but not r1
        elif cond2:
            print tabstring + "\t|___ {} -> {}/".format(f, f)
            if f is r2[-1]:
                print_dfs(fullpath2, tabstring+'\t + ')
            else:
                print_dfs(fullpath2, tabstring+'\t + |')

        # f is a dir in neither r1 nor r2
        else:
            "diffing {} in root1={} and root2={}".format(f, root1, root2)
