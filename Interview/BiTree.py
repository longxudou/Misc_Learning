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