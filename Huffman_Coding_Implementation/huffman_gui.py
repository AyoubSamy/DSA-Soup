import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
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
from PIL import Image, ImageTk


class HuffmanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Compression Huffman - Interface Graphique")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")
        
        # Variables
        self.fichier_path = tk.StringVar()
        self.texte_original = ""
        self.texte_encode = ""
        self.arbre_huffman = None
        self.codes = {}
        
        self.create_widgets()
    
    def create_widgets(self):
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # ============ Section 1: Sélection du fichier ============
        file_frame = ttk.LabelFrame(main_frame, text="1. Sélection du fichier", padding="10")
        file_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Entry(file_frame, textvariable=self.fichier_path, width=70).grid(row=0, column=0, padx=5)
        ttk.Button(file_frame, text="Parcourir", command=self.browse_file).grid(row=0, column=1, padx=5)
        ttk.Button(file_frame, text="Charger", command=self.load_file).grid(row=0, column=2, padx=5)
        
        # ============ Section 2: Texte original ============
        text_frame = ttk.LabelFrame(main_frame, text="2. Texte original", padding="10")
        text_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5, padx=5)
        
        self.text_original = scrolledtext.ScrolledText(text_frame, height=8, width=45, wrap=tk.WORD)
        self.text_original.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # ============ Section 3: Table des fréquences ============
        freq_frame = ttk.LabelFrame(main_frame, text="3. Fréquences", padding="10")
        freq_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5, padx=5)
        
        self.freq_text = scrolledtext.ScrolledText(freq_frame, height=8, width=45, wrap=tk.WORD)
        self.freq_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # ============ Section 4: Actions ============
        action_frame = ttk.LabelFrame(main_frame, text="4. Actions", padding="10")
        action_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Button(action_frame, text="Compresser", command=self.compress, width=20).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(action_frame, text="Décompresser", command=self.decompress, width=20).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(action_frame, text="Visualiser l'arbre", command=self.visualize_tree, width=20).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(action_frame, text="Afficher codes", command=self.show_codes, width=20).grid(row=0, column=3, padx=5, pady=5)
        
        # ============ Section 5: Texte encodé ============
        encoded_frame = ttk.LabelFrame(main_frame, text="5. Texte encodé (binaire)", padding="10")
        encoded_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5, padx=5)
        
        self.text_encoded = scrolledtext.ScrolledText(encoded_frame, height=8, width=45, wrap=tk.WORD)
        self.text_encoded.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # ============ Section 6: Statistiques ============
        stats_frame = ttk.LabelFrame(main_frame, text="6. Statistiques de compression", padding="10")
        stats_frame.grid(row=3, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5, padx=5)
        
        self.stats_text = scrolledtext.ScrolledText(stats_frame, height=8, width=45, wrap=tk.WORD)
        self.stats_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # ============ Section 7: Texte décodé ============
        decoded_frame = ttk.LabelFrame(main_frame, text="7. Texte décodé", padding="10")
        decoded_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.text_decoded = scrolledtext.ScrolledText(decoded_frame, height=6, width=95, wrap=tk.WORD)
        self.text_decoded.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurer la grille pour qu'elle soit responsive
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
    
    def browse_file(self):
        filename = filedialog.askopenfilename(
            title="Sélectionner un fichier texte",
            filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")]
        )
        if filename:
            self.fichier_path.set(filename)
    
    def load_file(self):
        try:
            path = self.fichier_path.get()
            if not path:
                messagebox.showwarning("Attention", "Veuillez sélectionner un fichier!")
                return
            
            self.texte_original = read_fichier(path)
            
            # Afficher le texte original
            self.text_original.delete(1.0, tk.END)
            self.text_original.insert(1.0, self.texte_original)
            
            # Calculer et afficher les fréquences
            frequence = calculer_frequence(self.texte_original)
            self.freq_text.delete(1.0, tk.END)
            for char, freq in sorted(frequence.items(), key=lambda x: x[1], reverse=True):
                if char == '\n':
                    self.freq_text.insert(tk.END, f"'\\n' : {freq}\n")
                elif char == ' ':
                    self.freq_text.insert(tk.END, f"' '  : {freq}\n")
                else:
                    self.freq_text.insert(tk.END, f"'{char}' : {freq}\n")
            
            messagebox.showinfo("Succès", "Fichier chargé avec succès!")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement: {str(e)}")
    
    def compress(self):
        try:
            if not self.texte_original:
                messagebox.showwarning("Attention", "Veuillez d'abord charger un fichier!")
                return
            
            # Calculer les fréquences
            frequence = calculer_frequence(self.texte_original)
            
            # Construire l'arbre de Huffman
            heap = initialiser_heap(frequence)
            self.arbre_huffman = construire_arbre(heap)
            
            # Générer les codes
            self.codes = generer_codes(self.arbre_huffman)
            
            # Encoder le texte
            self.texte_encode = encoder_texte(self.texte_original, self.codes)
            
            # Afficher le texte encodé
            self.text_encoded.delete(1.0, tk.END)
            self.text_encoded.insert(1.0, self.texte_encode)
            
            # Calculer et afficher les statistiques
            taux, gain = calculer_taux_compression_et_gain(self.texte_original, self.texte_encode)
            
            taille_originale_bits = len(self.texte_original) * 8
            taille_encodee_bits = len(self.texte_encode)
            
            self.stats_text.delete(1.0, tk.END)
            self.stats_text.insert(tk.END, f"Taille originale: {len(self.texte_original)} caractères\n")
            self.stats_text.insert(tk.END, f"Taille originale (bits): {taille_originale_bits} bits\n\n")
            self.stats_text.insert(tk.END, f"Taille encodée: {taille_encodee_bits} bits\n\n")
            self.stats_text.insert(tk.END, f"Taux de compression: {taux:.4f}\n")
            self.stats_text.insert(tk.END, f"Gain de compression: {gain:.4f} ({gain*100:.2f}%)\n\n")
            self.stats_text.insert(tk.END, f"Nombre de caractères uniques: {len(self.codes)}\n")
            
            messagebox.showinfo("Succès", "Compression effectuée avec succès!")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la compression: {str(e)}")
    
    def decompress(self):
        try:
            if not self.texte_encode or not self.arbre_huffman:
                messagebox.showwarning("Attention", "Veuillez d'abord compresser le texte!")
                return
            
            # Décoder le texte
            texte_decode = decoder_texte(self.texte_encode, self.arbre_huffman)
            
            # Afficher le texte décodé
            self.text_decoded.delete(1.0, tk.END)
            self.text_decoded.insert(1.0, texte_decode)
            
            # Vérifier si le décodage est correct
            if texte_decode == self.texte_original:
                messagebox.showinfo("Succès", "Décompression réussie! Le texte est identique à l'original.")
            else:
                messagebox.showwarning("Attention", "Le texte décodé diffère de l'original!")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la décompression: {str(e)}")
    
    def visualize_tree(self):
        try:
            if not self.arbre_huffman:
                messagebox.showwarning("Attention", "Veuillez d'abord compresser le texte!")
                return
            
            # Générer la visualisation
            dot = visualiser_arbre(self.arbre_huffman)
            output_path = 'arbre_huffman_gui'
            dot.render(output_path, format='png', cleanup=True)
            
            # Ouvrir une fenêtre pour afficher l'image
            self.show_tree_image(f'{output_path}.png')
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la visualisation: {str(e)}")
    
    def show_tree_image(self, image_path):
        # Créer une nouvelle fenêtre
        tree_window = tk.Toplevel(self.root)
        tree_window.title("Arbre de Huffman")
        
        # Charger et afficher l'image
        try:
            image = Image.open(image_path)
            
            # Redimensionner si nécessaire
            max_width = 800
            max_height = 600
            if image.width > max_width or image.height > max_height:
                ratio = min(max_width/image.width, max_height/image.height)
                new_size = (int(image.width * ratio), int(image.height * ratio))
                image = image.resize(new_size, Image.Resampling.LANCZOS)
            
            photo = ImageTk.PhotoImage(image)
            
            label = tk.Label(tree_window, image=photo)
            label.image = photo  # Garder une référence
            label.pack(padx=10, pady=10)
            
            # Bouton pour fermer
            ttk.Button(tree_window, text="Fermer", command=tree_window.destroy).pack(pady=5)
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'afficher l'image: {str(e)}")
            tree_window.destroy()
    
    def show_codes(self):
        try:
            if not self.codes:
                messagebox.showwarning("Attention", "Veuillez d'abord compresser le texte!")
                return
            
            # Créer une nouvelle fenêtre
            codes_window = tk.Toplevel(self.root)
            codes_window.title("Table des codes de Huffman")
            codes_window.geometry("400x500")
            
            # Frame pour le contenu
            frame = ttk.Frame(codes_window, padding="10")
            frame.pack(fill=tk.BOTH, expand=True)
            
            ttk.Label(frame, text="Caractère → Code binaire", font=('Arial', 12, 'bold')).pack(pady=5)
            
            # Texte défilant pour les codes
            codes_text = scrolledtext.ScrolledText(frame, height=20, width=40, wrap=tk.WORD)
            codes_text.pack(fill=tk.BOTH, expand=True, pady=5)
            
            # Afficher les codes triés par longueur
            for char, code in sorted(self.codes.items(), key=lambda x: len(x[1])):
                if char == '\n':
                    codes_text.insert(tk.END, f"'\\n' → {code}\n")
                elif char == ' ':
                    codes_text.insert(tk.END, f"' '  → {code}\n")
                else:
                    codes_text.insert(tk.END, f"'{char}' → {code}\n")
            
            codes_text.configure(state='disabled')
            
            # Bouton pour fermer
            ttk.Button(frame, text="Fermer", command=codes_window.destroy).pack(pady=5)
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'affichage des codes: {str(e)}")


def main():
    root = tk.Tk()
    app = HuffmanGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()