class File : 

    def __init__(self,name,taille,creation_date,accesse_path):
        self.name = name
        self.taille = taille
        self.date = creation_date
        self.path = accesse_path

class Node : 
    def __init__(self,file):
        self.key = file.name 
        self.file = file
        self.left = None
        self.right = None
        self.height = 1

class AVLTree : 
    def __init__(self):
        self.root = None
    
    def _get_height(self, node):
        if node is None:
            return 0
        return node.height

    def _get_balance(self, node):
        if node is None:
            return 0
        return self._get_height(node.left)-self._get_height(node.right)
    
    def _right_rotate(self, z):
        y = z.left
        T3 = y.right

        # Rotation
        y.right = z
        z.left = T3

        
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        # On retourne la nouvelle racine de ce sous-arbre
        return y

    def _left_rotate(self, z):
        y = z.right
        T2 = y.left

        # Rotation
        y.left = z
        z.right = T2

        # Mise à jour des hauteurs
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y
    
    def insert(self, root, fichier):
        # 1. Insertion normale (BST)
        if not root:
            return Node(fichier)
        elif fichier.name < root.key:
            root.left = self.insert(root.left, fichier)
        else:
            root.right = self.insert(root.right, fichier)

        # 2. Mise à jour de la hauteur
        root.height = 1 + max(self._get_height(root.left), self._get_height(root.right))

        # 3. Calcul du facteur d'équilibre
        balance = self._get_balance(root)

        # 4. CAS DE DÉSÉQUILIBRE

        # Cas LL (Left-Left) -> Rotation Droite
        if balance > 1 and fichier.name < root.left.key:
            return self._right_rotate(root)

        # Cas RR (Right-Right) -> Rotation Gauche
        if balance < -1 and fichier.name > root.right.key:
            return self._left_rotate(root)

        # Cas LR (Left-Right) -> Rotation Gauche sur l'enfant puis Droite sur le parent
        if balance > 1 and fichier.name > root.left.key:
            root.left = self._left_rotate(root.left)
            return self._right_rotate(root)

        # Cas RL (Right-Left) -> Rotation Droite sur l'enfant puis Gauche sur le parent
        if balance < -1 and fichier.name < root.right.key:
            root.right = self._right_rotate(root.right)
            return self._left_rotate(root)

        return root
    
    def search(self, root, name):
       
        if root is None or root.key == name:
            return root

        if name < root.key:
            return self.search(root.left, name)

        return self.search(root.right, name)
    
    def display_sorted(self, root):
        if root is None:
            return

        # 1. D'abord on visite le sous-arbre GAUCHE (les plus petits)
        self.display_sorted(root.left)

        # 2. Ensuite on traite la RACINE (le fichier actuel)
        f = root.file
        print(f"[Fichier] {f.name} \t| {f.taille} \t| {f.date} \t| {f.path}")

        # 3. Enfin on visite le sous-arbre DROIT (les plus grands)
        self.display_sorted(root.right)


    def _get_min_value_node(self, root):
        if root is None or root.left is None:
            return root
        return self._get_min_value_node(root.left)
    
    def delete(self, root, key):
        # --- ÉTAPE 1 : Suppression standard BST ---
        
        if not root:
            return root

        # Recherche du nœud à supprimer
        elif key < root.key:
            root.left = self.delete(root.left, key)
        elif key > root.key:
            root.right = self.delete(root.right, key)
            
        else:
            # On a trouvé le nœud ! (root.key == key)
            
            # Cas A & B : Pas d'enfant ou un seul enfant
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp

            # Cas C : Deux enfants
            # On cherche le successeur (le plus petit du côté droit)
            temp = self._get_min_value_node(root.right)

            # On copie les infos du successeur dans le nœud actuel
            root.key = temp.key
            root.file = temp.file # Important : on copie aussi le fichier !

            # On supprime l'ancien successeur (qui est maintenant un doublon)
            root.right = self.delete(root.right, temp.key)

        # Si l'arbre n'avait qu'un seul nœud et qu'il est supprimé
        if root is None:
            return root

        # --- ÉTAPE 2 : Mise à jour de la hauteur ---
        root.height = 1 + max(self._get_height(root.left), self._get_height(root.right))

        # --- ÉTAPE 3 : Vérification de l'équilibre ---
        balance = self._get_balance(root)

        # --- ÉTAPE 4 : Rotations (si déséquilibré) ---
        
        # Cas LL
        if balance > 1 and self._get_balance(root.left) >= 0:
            return self._right_rotate(root)

        # Cas LR
        if balance > 1 and self._get_balance(root.left) < 0:
            root.left = self._left_rotate(root.left)
            return self._right_rotate(root)

        # Cas RR
        if balance < -1 and self._get_balance(root.right) <= 0:
            return self._left_rotate(root)

        # Cas RL
        if balance < -1 and self._get_balance(root.right) > 0:
            root.right = self._right_rotate(root.right)
            return self._left_rotate(root)

        return root
    
    # --- 3. APPLICATION TERMINALE (INTERFACE) ---

def menu():
    print("\n" + "="*40)
    print("   GESTIONNAIRE DE FICHIERS (AVL TREE)")
    print("="*40)
    print("1. Ajouter un fichier")
    print("2. Supprimer un fichier")
    print("3. Rechercher un fichier")
    print("4. Afficher tout (Tri alphabétique)")
    print("5. Quitter")
    print("-" * 40)

def main():
    avl = AVLTree()
    
    # Données de test initiales (Optionnel, pour ne pas partir de zéro)
    avl.root = avl.insert(avl.root, File("rapport.pdf", "2MB", "2023-10-01", "/docs"))
    avl.root = avl.insert(avl.root, File("image.png", "5MB", "2023-10-05", "/imgs"))
    avl.root = avl.insert(avl.root, File("data.csv", "10KB", "2023-09-12", "/data"))

    while True:
        menu()
        choix = input("Votre choix (1-5) : ")

        if choix == '1':
            print("\n--- Ajout d'un nouveau fichier ---")
            nom = input("Nom du fichier : ")
            taille = input("Taille (ex: 2MB) : ")
            date = input("Date (AAAA-MM-JJ) : ")
            chemin = input("Chemin d'accès : ")
            
            nouveau_fichier = File(nom, taille, date, chemin)
            avl.root = avl.insert(avl.root, nouveau_fichier) # Important: mettre à jour la racine
            print(f"✅ Fichier '{nom}' ajouté avec succès.")

        elif choix == '2':
            print("\n--- Suppression d'un fichier ---")
            nom = input("Nom du fichier à supprimer : ")
            # On vérifie d'abord si le fichier existe pour un message plus clair
            if avl.search(avl.root, nom):
                avl.root = avl.delete(avl.root, nom) # Important: mettre à jour la racine
                print(f"🗑️  Fichier '{nom}' supprimé et arbre rééquilibré.")
            else:
                print(f"❌ Erreur : Le fichier '{nom}' n'existe pas.")

        elif choix == '3':
            print("\n--- Recherche d'un fichier ---")
            nom = input("Nom du fichier à chercher : ")
            resultat = avl.search(avl.root, nom)
            if resultat:
                f = resultat.file
                print(f"\n✅ TROUVÉ :")
                print(f"   Nom    : {f.name}")
                print(f"   Taille : {f.taille}")
                print(f"   Date   : {f.date}")
                print(f"   Chemin : {f.path}")
                print(f"   (Complexité : O(log n))")
            else:
                print(f"❌ Fichier '{nom}' introuvable.")

        elif choix == '4':
            print("\n--- Liste des fichiers (Triés A-Z) ---")
            print(f"{'NOM':<23} | {'TAILLE':<13} | {'DATE'}")
            print("-" * 50)
            if avl.root is None:
                print("(Aucun fichier dans le système)")
            else:
                avl.display_sorted(avl.root)

        elif choix == '5':
            print("Fermeture du gestionnaire. Au revoir !")
            break
        
        else:
            print("Option invalide, veuillez réessayer.")

if __name__ == "__main__":
    main()
    
    


    
        