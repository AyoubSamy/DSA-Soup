import os
import sys
from huffman import (
    read_fichier,
    calculer_frequence,
    initialiser_heap,
    construire_arbre,
    generer_codes,
    encoder_texte,
    decoder_texte,
    calculer_taux_compression_et_gain,
    visualiser_arbre
)


class HuffmanCLI:
    def __init__(self):
        self.texte_original = ""
        self.texte_encode = ""
        self.arbre_huffman = None
        self.codes = {}
        self.fichier_path = ""
        
    def clear_screen(self):
        """Efface l'écran du terminal"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def afficher_menu_principal(self):
        """Affiche le menu principal"""
        self.clear_screen()
        print("=" * 60)
        print(" " * 15 + "COMPRESSION HUFFMAN - CLI")
        print("=" * 60)
        print("\n[1] Charger un fichier texte")
        print("[2] Afficher le texte original")
        print("[3] Afficher les fréquences des caractères")
        print("[4] Compresser le texte")
        print("[5] Décompresser le texte")
        print("[6] Afficher la table des codes")
        print("[7] Afficher les statistiques de compression")
        print("[8] Visualiser l'arbre de Huffman")
        print("[9] Sauvegarder le texte encodé")
        print("[10] Charger et décompresser un texte encodé")
        print("[0] Quitter")
        print("=" * 60)
    
    def charger_fichier(self):
        """Charge un fichier texte"""
        print("\n" + "=" * 60)
        print("CHARGEMENT D'UN FICHIER")
        print("=" * 60)
        
        chemin = input("\nEntrez le chemin du fichier (ou appuyez sur Entrée pour 'fichier.txt'): ").strip()
        
        if not chemin:
            chemin = "fichier.txt"
        
        try:
            self.texte_original = read_fichier(chemin)
            self.fichier_path = chemin
            print(f"\n✓ Fichier '{chemin}' chargé avec succès!")
            print(f"  Nombre de caractères: {len(self.texte_original)}")
            
            # Réinitialiser les données de compression
            self.texte_encode = ""
            self.arbre_huffman = None
            self.codes = {}
            
        except FileNotFoundError:
            print(f"\n✗ Erreur: Le fichier '{chemin}' n'existe pas!")
        except Exception as e:
            print(f"\n✗ Erreur lors du chargement: {str(e)}")
        
        input("\nAppuyez sur Entrée pour continuer...")
    
    def afficher_texte_original(self):
        """Affiche le texte original"""
        print("\n" + "=" * 60)
        print("TEXTE ORIGINAL")
        print("=" * 60)
        
        if not self.texte_original:
            print("\n⚠ Aucun fichier chargé!")
        else:
            print(f"\nFichier: {self.fichier_path}")
            print(f"Taille: {len(self.texte_original)} caractères\n")
            print("-" * 60)
            print(self.texte_original)
            print("-" * 60)
        
        input("\nAppuyez sur Entrée pour continuer...")
    
    def afficher_frequences(self):
        """Affiche les fréquences des caractères"""
        print("\n" + "=" * 60)
        print("FRÉQUENCES DES CARACTÈRES")
        print("=" * 60)
        
        if not self.texte_original:
            print("\n⚠ Aucun fichier chargé!")
        else:
            frequence = calculer_frequence(self.texte_original)
            print(f"\nNombre de caractères uniques: {len(frequence)}\n")
            print("-" * 60)
            print(f"{'Caractère':<15} {'Fréquence':<15} {'Pourcentage'}")
            print("-" * 60)
            
            total = len(self.texte_original)
            for char, freq in sorted(frequence.items(), key=lambda x: x[1], reverse=True):
                pourcentage = (freq / total) * 100
                if char == '\n':
                    char_display = "'\\n'"
                elif char == ' ':
                    char_display = "' ' (espace)"
                elif char == '\t':
                    char_display = "'\\t'"
                else:
                    char_display = f"'{char}'"
                
                print(f"{char_display:<15} {freq:<15} {pourcentage:.2f}%")
            
            print("-" * 60)
        
        input("\nAppuyez sur Entrée pour continuer...")
    
    def compresser_texte(self):
        """Compresse le texte avec l'algorithme de Huffman"""
        print("\n" + "=" * 60)
        print("COMPRESSION DU TEXTE")
        print("=" * 60)
        
        if not self.texte_original:
            print("\n⚠ Aucun fichier chargé!")
            input("\nAppuyez sur Entrée pour continuer...")
            return
        
        try:
            print("\n" \
            " Compression en cours...")
            
            # Calculer les fréquences
            frequence = calculer_frequence(self.texte_original)
            
            # Construire l'arbre de Huffman
            heap = initialiser_heap(frequence)
            self.arbre_huffman = construire_arbre(heap)
            
            # Générer les codes
            self.codes = generer_codes(self.arbre_huffman)
            
            # Encoder le texte
            self.texte_encode = encoder_texte(self.texte_original, self.codes)
            
            print("\n✓ Compression réussie!")
            print(f"  Taille originale: {len(self.texte_original)} caractères ({len(self.texte_original) * 8} bits)")
            print(f"  Taille encodée: {len(self.texte_encode)} bits")
            
            taux, gain = calculer_taux_compression_et_gain(self.texte_original, self.texte_encode)
            print(f"  Taux de compression: {taux:.4f}")
            print(f"  Gain de compression: {gain:.4f} ({gain * 100:.2f}%)")
            
        except Exception as e:
            print(f"\n✗ Erreur lors de la compression: {str(e)}")
        
        input("\nAppuyez sur Entrée pour continuer...")
    
    def decompresser_texte(self):
        """Décompresse le texte encodé"""
        print("\n" + "=" * 60)
        print("DÉCOMPRESSION DU TEXTE")
        print("=" * 60)
        
        if not self.texte_encode or not self.arbre_huffman:
            print("\n⚠ Veuillez d'abord compresser un texte!")
            input("\nAppuyez sur Entrée pour continuer...")
            return
        
        try:
            print("\nDécompression en cours...")
            
            texte_decode = decoder_texte(self.texte_encode, self.arbre_huffman)
            
            print("\n✓ Décompression réussie!")
            
            # Vérifier si le décodage est correct
            if texte_decode == self.texte_original:
                print("  ✓ Le texte décodé est identique à l'original!")
            else:
                print("  ✗ ATTENTION: Le texte décodé diffère de l'original!")
            
            print(f"\nTexte décodé ({len(texte_decode)} caractères):")
            print("-" * 60)
            print(texte_decode)
            print("-" * 60)
            
        except Exception as e:
            print(f"\n✗ Erreur lors de la décompression: {str(e)}")
        
        input("\nAppuyez sur Entrée pour continuer...")
    
    def afficher_codes(self):
        """Affiche la table des codes de Huffman"""
        print("\n" + "=" * 60)
        print("TABLE DES CODES DE HUFFMAN")
        print("=" * 60)
        
        if not self.codes:
            print("\n⚠ Veuillez d'abord compresser un texte!")
        else:
            print(f"\nNombre de codes: {len(self.codes)}\n")
            print("-" * 60)
            print(f"{'Caractère':<15} {'Code binaire':<20} {'Longueur'}")
            print("-" * 60)
            
            for char, code in sorted(self.codes.items(), key=lambda x: len(x[1])):
                if char == '\n':
                    char_display = "'\\n'"
                elif char == ' ':
                    char_display = "' ' (espace)"
                elif char == '\t':
                    char_display = "'\\t'"
                else:
                    char_display = f"'{char}'"
                
                print(f"{char_display:<15} {code:<20} {len(code)} bits")
            
            print("-" * 60)
            
            # Calculer la longueur moyenne
            longueur_moyenne = sum(len(code) for code in self.codes.values()) / len(self.codes)
            print(f"\nLongueur moyenne des codes: {longueur_moyenne:.2f} bits")
        
        input("\nAppuyez sur Entrée pour continuer...")
    
    def afficher_statistiques(self):
        """Affiche les statistiques de compression"""
        print("\n" + "=" * 60)
        print("STATISTIQUES DE COMPRESSION")
        print("=" * 60)
        
        if not self.texte_encode or not self.arbre_huffman:
            print("\n⚠ Veuillez d'abord compresser un texte!")
        else:
            taille_originale_bits = len(self.texte_original) * 8
            taille_encodee_bits = len(self.texte_encode)
            taux, gain = calculer_taux_compression_et_gain(self.texte_original, self.texte_encode)
            
            print(f"\nFichier: {self.fichier_path}")
            print("\n" + "-" * 60)
            print("TAILLE DES DONNÉES:")
            print("-" * 60)
            print(f"  Texte original:")
            print(f"    - Caractères: {len(self.texte_original)}")
            print(f"    - Bits (8 bits/char): {taille_originale_bits}")
            print(f"    - Octets: {taille_originale_bits // 8}")
            print(f"\n  Texte encodé:")
            print(f"    - Bits: {taille_encodee_bits}")
            print(f"    - Octets (approximatif): {taille_encodee_bits // 8}")
            
            print("\n" + "-" * 60)
            print("COMPRESSION:")
            print("-" * 60)
            print(f"  Taux de compression: {taux:.4f} ({taux * 100:.2f}%)")
            print(f"  Gain de compression: {gain:.4f} ({gain * 100:.2f}%)")
            print(f"  Espace économisé: {taille_originale_bits - taille_encodee_bits} bits")
            # print(f"  Ratio: {taille_originale_bits / taille_encodee_bits:.2f}:1")
            
            print("\n" + "-" * 60)
        #    print("CODES:")
        #    print("-" * 60)
        #    print(f"  Nombre de caractères uniques: {len(self.codes)}")
        #    longueur_moyenne = sum(len(code) for code in self.codes.values()) / len(self.codes)
        #    print(f"  Longueur moyenne des codes: {longueur_moyenne:.2f} bits")
        #    longueur_min = min(len(code) for code in self.codes.values())
        #    longueur_max = max(len(code) for code in self.codes.values())
        #    print(f"  Longueur minimale: {longueur_min} bit(s)")
        #    print(f"  Longueur maximale: {longueur_max} bits")
        #    
            print("-" * 60)
        
        input("\nAppuyez sur Entrée pour continuer...")
    
    def visualiser_arbre(self):
        """Visualise l'arbre de Huffman"""
        print("\n" + "=" * 60)
        print("VISUALISATION DE L'ARBRE")
        print("=" * 60)
        
        if not self.arbre_huffman:
            print("\n⚠ Veuillez d'abord compresser un texte!")
        else:
            try:
                print("\n Génération de l'arbre...")
                
                dot = visualiser_arbre(self.arbre_huffman)
                output_path = 'arbre_huffman_cli'
                dot.render(output_path, format='png', cleanup=True)
                
                print(f"\n✓ Arbre généré avec succès!")
                print(f"  Fichier: {output_path}.png")
                print(f"  Chemin complet: {os.path.abspath(output_path)}.png")
                
                # Essayer d'ouvrir l'image automatiquement
                try:
                    if os.name == 'nt':  # Windows
                        os.system(f'start {output_path}.png')
                    elif os.name == 'posix':  # Linux/Mac
                        os.system(f'xdg-open {output_path}.png 2>/dev/null || open {output_path}.png')
                    print("  L'image devrait s'ouvrir dans votre visionneuse par défaut.")
                except:
                    print("  Ouvrez manuellement le fichier pour voir l'arbre.")
                    
            except Exception as e:
                print(f"\n✗ Erreur lors de la visualisation: {str(e)}")
        
        input("\nAppuyez sur Entrée pour continuer...")
    
    def sauvegarder_texte_encode(self):
        """Sauvegarde le texte encodé dans un fichier"""
        print("\n" + "=" * 60)
        print("SAUVEGARDER LE TEXTE ENCODÉ")
        print("=" * 60)
        
        if not self.texte_encode:
            print("\n⚠ Veuillez d'abord compresser un texte!")
            input("\nAppuyez sur Entrée pour continuer...")
            return
        
        nom_fichier = input("\nNom du fichier de sortie (ou Entrée pour 'encoded.bin'): ").strip()
        if not nom_fichier:
            nom_fichier = "encoded.bin"
        
        try:
            with open(nom_fichier, 'w', encoding='utf-8') as f:
                f.write(self.texte_encode)
            
            print(f"\n✓ Texte encodé sauvegardé dans '{nom_fichier}'")
            print(f"  Taille: {len(self.texte_encode)} bits")
            
        except Exception as e:
            print(f"\n✗ Erreur lors de la sauvegarde: {str(e)}")
        
        input("\nAppuyez sur Entrée pour continuer...")
    
    def charger_et_decompresser(self):
        """Charge un texte encodé et le décompresse"""
        print("\n" + "=" * 60)
        print("CHARGER ET DÉCOMPRESSER")
        print("=" * 60)
        
        if not self.arbre_huffman:
            print("\n⚠ Vous devez d'abord créer un arbre de Huffman en compressant un texte!")
            input("\nAppuyez sur Entrée pour continuer...")
            return
        
        nom_fichier = input("\nNom du fichier encodé: ").strip()
        
        try:
            with open(nom_fichier, 'r', encoding='utf-8') as f:
                texte_encode = f.read()
            
            print("\n Décompression en cours...")
            texte_decode = decoder_texte(texte_encode, self.arbre_huffman)
            
            print(f"\n✓ Décompression réussie!")
            print(f"\nTexte décodé ({len(texte_decode)} caractères):")
            print("-" * 60)
            print(texte_decode)
            print("-" * 60)
            
        except FileNotFoundError:
            print(f"\n✗ Erreur: Le fichier '{nom_fichier}' n'existe pas!")
        except Exception as e:
            print(f"\n✗ Erreur: {str(e)}")
        
        input("\nAppuyez sur Entrée pour continuer...")
    
    def run(self):
        """Lance l'application CLI"""
        while True:
            self.afficher_menu_principal()
            
            choix = input("\nChoisissez une option (0-10): ").strip()
            
            if choix == '1':
                self.charger_fichier()
            elif choix == '2':
                self.afficher_texte_original()
            elif choix == '3':
                self.afficher_frequences()
            elif choix == '4':
                self.compresser_texte()
            elif choix == '5':
                self.decompresser_texte()
            elif choix == '6':
                self.afficher_codes()
            elif choix == '7':
                self.afficher_statistiques()
            elif choix == '8':
                self.visualiser_arbre()
            elif choix == '9':
                self.sauvegarder_texte_encode()
            elif choix == '10':
                self.charger_et_decompresser()
            elif choix == '0':
                self.clear_screen()
                print("\n" + "=" * 60)
                print(" " * 20 + "Au revoir!")
                print("=" * 60 + "\n")
                sys.exit(0)
            else:
                print("\n⚠ Option invalide! Veuillez choisir entre 0 et 10.")
                input("\nAppuyez sur Entrée pour continuer...")


def main():
    """Fonction principale"""
    app = HuffmanCLI()
    app.run()


if __name__ == "__main__":
    main()