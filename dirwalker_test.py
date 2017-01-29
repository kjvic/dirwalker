import walker
import pprint
from os import listdir, getcwd

def print_dir(root):
    """
    Print function for a directory -- lists files
    and child nodes in a pretty format
    """
    ls_out = listdir(root)
    print "\nroot: {}".format(root)
    for f in ls_out:
        print "\t|___ {}".format(f)

root = getcwd()
print "TESTING PRINT_DFS"
walker.print_dfs(root)

print "TESTING WALK_DFS"
walk = walker.walk_dfs(root)
pprint.pprint(walk)
print

print "TESTING DDELTA"
root1 = root + "/root1"
root2 = root + "/root2"
walker.ddelta(root1, root2)
