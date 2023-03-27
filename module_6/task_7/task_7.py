import logging
from queue import Queue


PATH_TO_LOG: str = "./binary_tree.log"

logger = logging.getLogger("binary_tree")


class BinaryTreeNode:
    def __init__(self, number: int) -> None:
        self.number: int = number
        self.left: BinaryTreeNode | None = None
        self.right: BinaryTreeNode | None = None

    def __str__(self) -> str:
        return str(self.number)


def walk_tree(root: BinaryTreeNode) -> None:
    queue: [BinaryTreeNode] = Queue()
    queue.put(root)
    while queue.qsize() > 0:
        current_node: BinaryTreeNode = queue.get()
        logger.info(f"{current_node};{current_node.left};{current_node.right}")

        for new_root in [current_node.left, current_node.right]:
            if new_root is not None:
                queue.put(new_root)


def restore_tree(path_to_log: str) -> BinaryTreeNode:
    with open(path_to_log, 'r') as log:
        tree: dict[int, BinaryTreeNode] = {}
        root, root_left, root_right = _get_roots(log.readline())
        main_node: BinaryTreeNode = BinaryTreeNode(root)
        _set_nodes(tree, main_node, root_left, root_right)

        for line in log:
            root, root_left, root_right = _get_roots(line)
            _set_nodes(tree, tree.pop(root), root_left, root_right)

        return main_node


def _get_roots(line: str) -> tuple[int | None]:
    return tuple(map(lambda x: None if x.startswith("None") else int(x), line.split(";")))


def _set_nodes(tree: dict, node: BinaryTreeNode,
               root_left: int | None, root_right: int | None) -> None:
    _restore_node(node, root_left, root_right)
    tree[root_left] = node.left
    tree[root_right] = node.right


def _restore_node(node: BinaryTreeNode,
                  root_left: int | None, root_right: int | None) -> None:
    node.left = BinaryTreeNode(root_left) if root_left is not None else None
    node.right = BinaryTreeNode(root_right) if root_right is not None else None


def _get_test_data() -> BinaryTreeNode:
    root: BinaryTreeNode = BinaryTreeNode(1)
    root.left = node2 = BinaryTreeNode(2)
    root.right = BinaryTreeNode(10)
    node2.left = BinaryTreeNode(8)
    node2.right = BinaryTreeNode(7)
    return root


if __name__ == '__main__':
    logging.basicConfig(filename=PATH_TO_LOG,
                        filemode='w',
                        level=logging.INFO,
                        format="%(msg)s")
    walk_tree(_get_test_data())
    tree: BinaryTreeNode = restore_tree(PATH_TO_LOG)
    walk_tree(tree)
