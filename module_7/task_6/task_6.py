import logging
import logging_tree


logging.getLogger('a')
logging.getLogger('a.b').setLevel(logging.DEBUG)
logging.getLogger('x.c')

with open("logging_tree.txt", mode='w+') as file:
    tree: str = logging_tree.format.build_description()
    file.write(tree)
