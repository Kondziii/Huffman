class TreeNode:
    def __init__(self, letter, frequency, leftNode=None, rightNode=None):
        self.letter = letter
        self.frequency = frequency
        self.leftNode = leftNode
        self.rightNode = rightNode

    def __lt__(self, other):
        return self.frequency < other.frequency




