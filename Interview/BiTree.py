class Node:
    def __init__(self, value=None, right=None, left=None):
        self.value=value
        self.right=right
        self.left=left

def preTravese(root):
    if root==None:
        return

    print root.value
    preTravese(root.left)
    preTravese(root.right)



root=Node('D',Node('E',Node('G',left=Node('F'))),Node('B',Node('C'),Node('A')))
# root=Node('D')

# preTravese(root)


preList = list('12473568')
midList = list('47215386')
afterList = []

def findTree(preList, midList, afterList):
    if len(preList)==0:
        return
    if len(preList)==1:
        afterList.append(preList[0])
        return

    root=preList[0]

    root_index=midList.index(root)
    findTree(preList[1:root_index+1],midList[:root_index],afterList)
    findTree(preList[root_index+1:], midList[root_index+1:], afterList)
    afterList.append(root)

findTree(preList,midList,afterList)
print afterList



class BST_Solution(object):
    def buildTree_pre(self, preorder, inorder):
        if not inorder or not preorder:
            return None

        root = TreeNode(preorder.pop(0))

        root_index = inorder.index(root.val)

        root.left = self.buildTree(preorder, inorder[:root_index])
        root.right = self.buildTree(preorder, inorder[root_index + 1:])

        return root

    def buildTree_post(self, inorder, postorder):

        if not inorder or not postorder:
            return None

        root = TreeNode(postorder.pop())

        root_index = inorder.index(root.val)

        # root.left=self.buildTree(inorder[:root_index],postorder)
        root.right = self.buildTree(inorder[root_index + 1:], postorder)
        root.left = self.buildTree(inorder[:root_index], postorder)

        return root


class Solution(object):
    def inorderTraversal(self, root):
        stack = []
        ans = []
        node = root

        while stack or node:
            if node:
                stack.append(node)
                node = node.left
            else:
                node = stack.pop()
                ans.append(node.val)
                node = node.right
        return ans

    def preorderTraversal(self, root):
        ans = []
        stack = []
        node = root

        while stack or node:
            if node:
                stack.append(node)
                ans.append(node.val)
                node = node.left
            else:
                node = stack.pop()
                node = node.right

        return ans

    def postorderTraversal(self, root):
        ans = []
        stack = []
        node = root
        while stack or node:
            if node:
                stack.append(node)
                ans.insert(0, node.val)
                node = node.right
            else:
                node = stack.pop()
                node = node.left
        return ans