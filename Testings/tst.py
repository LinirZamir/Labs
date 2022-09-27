class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None 

def inorderTraversal(root):
    answer = []

    inorderTraversalUtil(root, answer)
    return answer

def inorderTraversalUtil(root, answer):

    if root is None:
        return

    inorderTraversalUtil(root.left, answer)
    inorderTraversalUtil(root.right, answer)
    answer.append(root.val)
    return

root = TreeNode(1)
root.left = TreeNode(2)
root.right = TreeNode(3)
root.left.left = TreeNode(4)
root.left.right = TreeNode(5)

print(inorderTraversal(root))