import queue
from functools import reduce


class NaryTreeNode(object):

    def __init__(self, value, children = None):
        if not children:
            children = []
        self.__val__ = value
        self.__children__ = children

    def get_value(self):
        return self.__val__

    def add_child(self, child):
        self.__children__.append(child)

    def get_child(self, value):
        for child in self.__children__:
            if child.__val__ == value:
                return child
        else:
            return KeyError('No child with value: ', value)
    
    def __iter__(self):
        for child in self.__children__:
            yield child


    def remove_child(self, value):
        for i in range(len(self.__children__)):
            child = self.__children__[i]
            if child.__val__ == value:
                del self.__children__[i]
                print('Child with value: ', value, ' deleted')
        else:
            print('No child with value: ', value)

class BTreeNode(object):

    def __init__(self, value, left=None, right=None):
        self.__val = value
        self.__left = left
        self.__right = right

    def get_left(self):
        return self.__left
    
    def get_right(self):
        return self.__right
    
    def get_value(self):
        return self.__val

    def add_left(self, node):
        self.__left = node
    
    def add_right(self, node):
        self.__right = node

    def remove_left(self):
        self.__left = None
    
    def remove_right(self):
        self.__right = None

    def __iter__(self):
        if self.__left:
            yield self.__left
        if self.__right:
            yield self.__right

    def level_order_traversal(self):
        rep_string = "BTree: "
        q = queue.SimpleQueue()
        q.put(self)
        while not q.empty():
            node = q.get()
            rep_string += str(node.get_value()) + ", "
            for child in node:
                q.put(child)
        return rep_string

    def __repr__(self):
        return self.level_order_traversal()

    def __str__(self):
        return self.level_order_traversal()

class Trie(object):

    def __init__(self, root=None, words=None):
        if not root:
            root = TrieNode()
        self.__root = root
        if not words:
            words = []
        for word in words:
            self.add_word(word.lower())

    def add_word(self, word, value=None):
        node = self.__root
        for char in word:
            if not node.has_child(char):
                node.add_child(char)
            node = node.get_child(char)
        node.set_value(value)

    def get_root(self):
        return self.__root

    def get_value(self, key):
        node = self.__root
        for char in key:
            if node.has_child(char):
                node = node.get_child(char)
            else:
                return None
        return node.get_value()
    
    def delete(self, key):
        return self.__delete(self.__root, key, 0)

    def __delete(self, node, key, d):
        if d == len(key):
            node.set_value(None)
        else:
            c = key[d]
            if node.has_child(c) and self.__delete(node.get_child(c), key, d+1):
                node.delete_child(c)
            return node.get_value() is None and not node.has_children()

class TrieNode(object):

    def __init__(self, value=None, char=None, children=None):
        self.__val = value
        self.__char = char
        if not children:
            children = [None]*26
        self.__children = children

    def get_char(self):
        return self.__char

    def get_children(self):
        return self.__children

    def has_children(self):
        return len(list([child for child in self.__children if child])) > 0

    def set_value(self, value):
        self.__val = value
    
    def get_value(self):
        return self.__val
    
    def __get_index(self, char):
        return ord(char) - 96 - 1

    def has_child(self, char):
        index = self.__get_index(char)
        return bool(self.__children[index])

    def get_child(self, char):
        index = self.__get_index(char)
        return self.__children[index]

    def add_child(self, char):
        index = self.__get_index(char)
        self.__children[index] = TrieNode(char=char)

    def delete_child(self, char):
        index = self.__get_index(char)
        del self.__children[index]

    def __iter__(self):
        for child in self.__children:
            if child:
                yield child



def print_level_order_traversal(root, method):
    if not root:
        return
    q = queue.SimpleQueue()
    q.put(root)
    while not q.empty():
        node = q.get()
        print('Node: ', method(node))
        for child in node:
            q.put(child)

def in_order(node):
    # Left, Root, Right
    if node.get_left():
        in_order(node.get_left())
    print('Node: ', node.get_value())
    if node.get_right():
        in_order(node.get_right())

def pre_order(node):
    # Root, Left, Right
    print('Node: ', node.get_value())
    if node.get_left():
        pre_order(node.get_left())
    if node.get_right():
        pre_order(node.get_right())

def post_order(node):
    # Left, Right, Root
    if node.get_left():
        post_order(node.get_left())
    if node.get_right():
        post_order(node.get_right())
    print('Node: ', node.get_value())



def print_btree_traversals(root):
    print("\nBTree In-order Traversal")
    in_order(root)
    print("\nPre-order Traversal")
    pre_order(root)
    print("\nPost-order Traversal")
    post_order(root)

def create_new_nary_tree():
    root = NaryTreeNode(1)
    root.add_child(NaryTreeNode(2))
    root.add_child(NaryTreeNode(3))
    root.add_child(NaryTreeNode(4))
    root.get_child(2).add_child(NaryTreeNode(5))
    root.get_child(2).add_child(NaryTreeNode(6))
    root.get_child(2).add_child(NaryTreeNode(7))
    root.get_child(3).add_child(NaryTreeNode(8))
    root.get_child(4).add_child(NaryTreeNode(9))
    root.get_child(4).add_child(NaryTreeNode(10))
    root.get_child(4).add_child(NaryTreeNode(11))
    return root

def create_new_btree():
    root = BTreeNode(1)
    root.add_left(BTreeNode(2))
    root.add_right(BTreeNode(3))
    root.get_left().add_left(BTreeNode(4))
    root.get_left().add_right(BTreeNode(5))
    return root

def create_new_trie():
    trie = Trie(words='Peter Piper picked a pack of pickled peppers'.split(' '))
    return trie

def main():
    nary_root = create_new_nary_tree()
    print("N-ary Tree Level Order Traversal: ")
    print_level_order_traversal(nary_root, NaryTreeNode.get_value)

    b_root = create_new_btree()
    print(b_root)
    print_btree_traversals(b_root)

    print("\nTrie: ")
    trie = create_new_trie()
    print_level_order_traversal(trie.get_root(), TrieNode.get_char)
    trie.add_word('piper', 5)
    trie.add_word('pterodactyl', 1)
    trie.add_word('pick', 10)
    trie.add_word('picked', 15)
    print(trie.get_value('piper'))
    print(trie.get_value('pterodactyl'))
    print(trie.get_value('peter'))
    print(trie.get_value('asshole'))
    print(trie.get_value('pick'), trie.get_value('picked'))
    trie.delete('pick')
    print(trie.get_value('pick'), trie.get_value('picked'))
    trie.add_word('pick', 11)
    print(trie.get_value('pick'), trie.get_value('picked'))
    trie.delete('picked')
    print(trie.get_value('pick'), trie.get_value('picked'))
    

if __name__ == "__main__":
    main()