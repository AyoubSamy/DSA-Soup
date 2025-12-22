# ------------------------------------------
# AVL TREE IMPLEMENTATION
# ------------------------------------------
class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 0

    # hauteur d’un nœud
    def height(node):
        if node is None:
            return -1
        return node.height

# Question 1 : facteur d'équilibre
    def balance_factor(node):
        if node is None:
            return 0
        return Node.height(node.left) - Node.height(node.right)
    
# Question 2.1 : rotation droite
    def rotate_right(z):
        y = z.left
        T2 = y.right

        y.right = z
        z.left = T2

        z.height = 1 + max(Node.height(z.left), Node.height(z.right))
        y.height = 1 + max(Node.height(y.left), Node.height(y.right))

        return y

# Question 2.2 : rotation gauche
    def rotate_left(z):
        y = z.right
        T2 = y.left

        # rotation
        y.left = z
        z.right = T2

        # mise à jour des hauteurs
        z.height = 1 + max(Node.height(z.left), Node.height(z.right))
        y.height = 1 + max(Node.height(y.left), Node.height(y.right))

        # nouvelle racine
        return y

    # Question 3 : insertion AVL
    def insert(node, key):

        if node is None:
            return Node(key)

        if key < node.key:
            node.left = Node.insert(node.left, key)
        elif key > node.key:
            node.right = Node.insert(node.right, key)
        else:
            return node  

        node.height = 1 + max(Node.height(node.left),
                              Node.height(node.right))

        balance = Node.balance_factor(node)

        if balance > 1 and key < node.left.key:
            return Node.rotate_right(node)

        if balance < -1 and key > node.right.key:
            return Node.rotate_left(node)

        if balance > 1 and key > node.left.key:
            node.left = Node.rotate_left(node.left)
            return Node.rotate_right(node)

        if balance < -1 and key < node.right.key:
            node.right = Node.rotate_right(node.right)
            return Node.rotate_left(node)

        return node

    # Question 6 : affichage infixe
    def inorder(node):
        if node is not None:
            Node.inorder(node.left)
            print(node.key, end=" ")
            Node.inorder(node.right)

    def print_tree(node, level=0, prefix="Root: "):
        if node is not None:
        # Affiche la droite en premier
            Node.print_tree(node.right, level + 1, "R---- ")
            # Affichage du nœud courant
            indent = "  " * (level - 1) + ("|---- " if level > 0 else "")
            print(indent + prefix + str(node.key))
            # Affiche la gauche
            Node.print_tree(node.left, level + 1, "L---- ")



# test final

root = None
values = [10, 20, 30, 40, 50, 25]
for v in values:
    root = Node.insert(root, v)
print("Affichage infixe (trié) :")
Node.inorder(root) # Résultat attendu : 10 20 25 30 40 50
print("\n\nArbre AVL (structure hiérarchique) :")
Node.print_tree(root)