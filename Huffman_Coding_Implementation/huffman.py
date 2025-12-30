import heapq
from graphviz import Digraph


####---------------------------partie 1 (Aicha Zeroual )-------------------------------------------------------

# lire le fichier.txt
def read_fichier(chemin_de_fichier):
    with open(chemin_de_fichier, 'r', encoding='utf-8') as f:
        return f.read()

#calculer la frequence de chaque caractere dans le texte
def calculer_frequence(texte):
    frequence = {}
    for char in texte:
        if char in frequence:
            frequence[char] += 1
        else:
            frequence[char] = 1
    return frequence

# creer un noeud pour chaque caractere et sa frequence
class Noeud:
    def __init__(self, caractere, frequence, gauche=None, droite=None):
        self.caractere = caractere
        self.frequence = frequence
        self.gauche = gauche
        self.droite = droite

    def __lt__(self, autre):
        return self.frequence < autre.frequence

# initialiser une liste de priorite (min-heap)
def initialiser_heap(frequence):
    heap = []
    for caractere, freq in frequence.items():
        noeud = Noeud(caractere, freq)
        heapq.heappush(heap, noeud)
    return heap

####---------------------------partie 2 (Wahyudi muhammad Irfan )-------------------------------------------------------

# construire l'arbre de Huffman
def construire_arbre(heap):
    while len(heap) > 1:
        gauche = heapq.heappop(heap)
        droite = heapq.heappop(heap)
        fusionne = Noeud(None, gauche.frequence + droite.frequence, gauche, droite)
        heapq.heappush(heap, fusionne)
    return heapq.heappop(heap)

# generer les codes de Huffman
def generer_codes(noeud, prefixe="", codes=None):
    if codes is None:
        codes = {}
    if noeud is not None:
        if noeud.caractere is not None:
            codes[noeud.caractere] = prefixe
        generer_codes(noeud.gauche, prefixe + "0", codes)
        generer_codes(noeud.droite, prefixe + "1", codes)
    return codes

# encoder le texte en utilisant les codes de Huffman
def encoder_texte(texte, codes):
    encoded_texte = ""
    for char in texte:
        encoded_texte += codes[char]
    return encoded_texte

####---------------------------partie 3 (Ayoub Samy )-------------------------------------------------------

# calculer le taux de compression et gain
def calculer_taux_compression_et_gain(texte_original, texte_encode):

    taille_originale_bits = len(texte_original) * 8

    taille_encodee_bits = len(texte_encode)
    
    taux_compression = taille_encodee_bits / taille_originale_bits
    
    gain = 1 - taux_compression
    
    return taux_compression, gain

# fonction principale pour compresser le fichier
def compresser_fichier(chemin_de_fichier):
    texte = read_fichier(chemin_de_fichier)

    frequence = calculer_frequence(texte)
    
    heap = initialiser_heap(frequence)
    
    arbre_huffman = construire_arbre(heap)

    codes = generer_codes(arbre_huffman)
    
    print("\nTable des codes de Huffman :")
    for caractere, code in codes.items():
        if caractere == '\n':
            print("'\\n' :", code)
        elif caractere == ' ':
         print("' '  :", code)
        else:
            print(f"'{caractere}' :", code)

    encoded_texte = encoder_texte(texte, codes)

    return encoded_texte

# decoder le texte encode en utilisant l'arbre de Huffman
def decoder_texte(texte_encode, arbre_huffman):
    
    texte_decode = ""
    noeud_courant = arbre_huffman
    
    for bit in texte_encode:
        if bit == '0':
            noeud_courant = noeud_courant.gauche
        else:  
            noeud_courant = noeud_courant.droite
        
        
        if noeud_courant.caractere is not None:
            texte_decode += noeud_courant.caractere
            
            noeud_courant = arbre_huffman
    
    return texte_decode

# Visualiser l'arbre de Huffman avec graphviz
def visualiser_arbre(noeud, dot=None):
    if dot is None:
        dot = Digraph()
    
    if noeud is not None:
        if noeud.caractere is not None:
            dot.node(str(id(noeud)), f"'{noeud.caractere}': {noeud.frequence}")
        else:
            dot.node(str(id(noeud)), str(noeud.frequence))
        
        if noeud.gauche is not None:
            dot.edge(str(id(noeud)), str(id(noeud.gauche)), label="0")
            visualiser_arbre(noeud.gauche, dot)
        
        if noeud.droite is not None:
            dot.edge(str(id(noeud)), str(id(noeud.droite)), label="1")
            visualiser_arbre(noeud.droite, dot)
    
    return dot



# Exemple d'utilisation

texte = read_fichier("fichier.txt")
frequence = calculer_frequence(texte)
heap = initialiser_heap(frequence)
arbre_huffman = construire_arbre(heap)

encoded_texte = compresser_fichier("fichier.txt")

decoded_texte = decoder_texte(encoded_texte,arbre_huffman)

taux, gain = calculer_taux_compression_et_gain(texte, encoded_texte)

print("Texte encodé :", encoded_texte)

print("Texte décodé :", decoded_texte)

print("Taux de compression :", taux)

print("Gain de compression :", gain)


dot = visualiser_arbre(arbre_huffman)

dot.render('arbre_huffman', format='png', cleanup=True)

print("\nArbre sauvegardé dans arbre_huffman.png")
