#!/usr/bin/python
# -*- coding: utf-8 -*-

class node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

max_len = 0

def MaxDistance(root):
    if not root:
        return 0
        
    global max_len
    ld = MaxDistance(root.left)
    rd = MaxDistance(root.right)
    height = max(ld, rd) + 1
    if (ld + rd + 2) > max_len:
        max_len = ld + rd + 2

    return height

def Link(tree, parent, left, right):
    if left != -1:
        tree[parent].left = tree[left]
    
    if right != -1:
        tree[parent].right = tree[right]

if __name__ == "__main__":
    root = []
    for x in range(0, 10):
        n = node(x)
        root.append(n)
    
    Link(root, 0, 1, 2)
    Link(root, 1, 3, 4)
    Link(root, 2, 5, 6)
    Link(root, 3, 7, 8)
    Link(root, 5, 9, -1)
    
    MaxDistance(root[0])
    print(max_len)
