import matplotlib.pyplot as plt
from IPython.display import display

def point_style(actual_point, applied):
    if applied[0] == 'insert' and actual_point[0] == applied[1] and actual_point[1] == applied[2]:
        return 'ro'
    else: 
        return 'bo'

def border_style(node, op_type, res):
    if op_type == 'localize' and node == res:
        return ('r', 'r--')
    else:
        return ('b', 'b--')
    
def debug_node(node, axis, applied, res):
    if node.empty():
        return
    if node.simple():
        axis.plot(node.data[0], node.data[1], point_style(node.data, applied))
        return
    b, b_ = border_style(node, applied[0], res)
    left, right, bottom, top = node.bounds
    x_mid = (left + right)/2
    y_mid = (top + bottom)/2
    axis.plot((left, left), (bottom, top), b)
    axis.plot((right, right), (bottom, top), b)
    axis.plot((x_mid, x_mid), (bottom, top), b_)
    axis.plot((left, right), (bottom, bottom), b)
    axis.plot((left, right), (top, top), b)
    axis.plot((left, right), (y_mid, y_mid), b_)
    for child in node.children.values():
        debug_node(child, axis, applied, res)
    
def debug_cqtree(tree, axis, applied=('none'), res=None):
    root = tree.root
    left, right, bottom, top = root.bounds
    debug_node(root, axis, applied, res)
    axis.set_xlim(left, right)
    axis.set_ylim(bottom, top)

def apply_operation(tree, op):
    t = op[0]
    if t == 'none':
        return
    if t == 'localize':
        return tree.localize((op[1], op[2]))
    if t == 'insert':
        return tree.insert((op[1], op[2]))
    if t == 'remove':
        return tree.remove((op[1], op[2]))
    raise Exception('Unknown command')
    
def apply_operations(tree, ops):
    for op in ops:
        apply_operation(tree, op)

def display_cqtree_dump(tree, ops, scale=3):
    fig, axes = plt.subplots(1, len(ops), figsize=(scale * len(ops), scale))
    for op, axis in zip(ops, axes):
        apply_operation(tree, op)
        debug_cqtree(tree, axis, op)
        axis.set_title("{} ({}, {})".format(*op))

viewer = None
        
class TreeViewer:
    
    def __init__(self, tree, ax, on_click):
        self.tree = tree
        self.ax = ax
        self.on_click = on_click
        ax.figure.canvas.mpl_connect('button_press_event', self.press_callback)
        
    def press_callback(self, event):
        self.do_op(event.xdata, event.ydata)
    
    def do_op(self, x, y): 
        op = (self.on_click, x, y)
        res = apply_operation(self.tree, op)
        
        self.ax.clear()
        debug_cqtree(self.tree, self.ax, op, res)
        display(self.ax.figure)

def display_cqtree_interactive(tree, scale=3, on_click='insert'):
    fig = plt.figure(1, figsize=(scale, scale))
    ax = plt.subplot(111)
    global viewer
    viewer = TreeViewer(tree, ax, on_click)
    debug_cqtree(tree, ax)