## Question 1 : Etant donné la structure et le constructeur suivants, trouvez la méthode
## d’insertion: 
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        node = Node(value)
        tmp = self.root
        if(self.root != None):
             while(1):
                 if(tmp.value>value):
                     if(tmp.left== None):
                         tmp.left = node
                         break
                     else:
                         tmp = tmp.left 
                 else:
                    if(tmp.right == None):
                        tmp.right = node
                        break
                    else:
                        tmp = tmp.right                             
        else:
            self.root = node
    
    def Contains(self,value):
        tmp = self.root
        if self.root is None:
            return False

        while tmp is not None:
            if tmp.value == value:
                return True                  
            elif tmp.value > value:
                tmp = tmp.left   
            else:
                tmp = tmp.right  

        return False 
    
    def __r_insert(self, current_node, value):
        
        if current_node is None:
            return Node(value) # On crée le nœud et on le retourne
        
        
        if value < current_node.value:
           
            current_node.left = self.__r_insert(current_node.left, value)
        elif value > current_node.value:
            
            current_node.right = self.__r_insert(current_node.right, value)
        
        return current_node
    
    def r_insert(self, value):

        if self.root is None:
            self.root = Node(value)
        else:
            self.__r_insert(self.root, value)
    
    def __r_contains(self, current_node, value):

        if current_node is None:
            return False
        
        if value == current_node.value:
            return True
        
        if value < current_node.value:
            return self.__r_contains(current_node.left, value)
        else:
            return self.__r_contains(current_node.right, value)

    def r_contains(self, value):
        return self.__r_contains(self.root, value)


my_tree = BinarySearchTree()
my_tree.r_insert(2)
my_tree.r_insert(1)
my_tree.r_insert(3)

print('Root:', my_tree.root.value)
print('Root -> Left:', my_tree.root.left.value)
print('Root -> Right:', my_tree.root.right.value)

# Test de la recherche
print("\nContient 3 ?", my_tree.r_contains(3))
print("Contient 99 ?", my_tree.r_contains(99))



