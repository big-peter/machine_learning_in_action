

class TreeNode(object):
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.parent = parentNode
        self.children = {}
        self.nodeLink = None

    def inc(self, numOccur):
        self.count += numOccur

    def display(self, ind=1):
        print(' ' * ind, self.name, ' ', self.count)
        for child in self.children.values():
            child.display(ind + 1)

