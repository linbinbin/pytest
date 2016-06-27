#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This file for tree and treap"""

class TreeNode:
    def __init__(self, x):
        self.data  = x
        self.left  = None
        self.right = None

def search(node, x):
    while node:
        if node.data == x: return True
        if x < node.data:
            node = node.left
        else:
            node = node.right
    return False
    
def insert(node, x):
    if node is None: return TreeNode(x)
    elif x == node.data: return node
    elif x < node.data:
        node.left = insert(node.left, x)
    else:
        node.right = insert(node.right, x)
    return node

# 最小値を探す
def search_min(node):
    if node.left is None: return node.data
    return search_min(node.left)

# 最小値を削除する
def delete_min(node):
    if node.left is None: return node.right
    node.left = delete_min(node.left)
    return node
    
def delete(node, x):
    if node:
        if x == node.data:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                node.data = search_min(node.right)
                node.right = delete_min(node.right)
        elif x < node.data:
            node.left = delete(node.left, x)
        else:
            node.right = delete(node.right, x)
    return node

    
