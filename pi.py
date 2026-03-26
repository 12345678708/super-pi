import mpmath as mp
import time
import threading
import tkinter as tk
from tkinter import ttk, filedialog

done = False
stop_flag = False

# Fenêtre
root = tk.Tk()
root.title("π ULTIME FINAL")
root.geometry("480x340")
root.configure(bg="#1e1e1e")

nb_var = tk.StringVar(value="200000")
file_path = tk.StringVar(value="pi.txt")

# UI
tk.Label(root, text="π - Calcul ultime", fg="white", bg="#1e1e1e", font=("Arial", 14)).pack(pady=10)

tk.Label(root, text="Décimales :", fg="white", bg="#1e1e1e").pack()
tk.Entry(root, textvariable=nb_var).pack()

tk.Label(root, text="Fichier :", fg="white", bg="#1e1e1e").pack()
tk.Entry(root, textvariable=file_path, width=40).pack()

def choose_file():
    path = filedialog.asksaveasfilename(defaultextension=".txt")
    if path:
        file_path.set(path)

tk.Button(root, text="📁 Choisir", command=choose_file).pack(pady=5)

progress = ttk.Progressbar(root, length=380, mode='determinate')
progress.pack(pady=10)

percent_label = tk.Label(root, text="0 %", fg="white", bg="#1e1e1e")
percent_label.pack()

time_label = tk.Label(root, text="Temps restant: -", fg="white", bg="#1e1e1e")
time_label.pack()

status_label = tk.Label(root, text="Prêt", fg="white", bg="#1e1e1e")
status_label.pack(pady=5)

# Boutons
def start():
    global done, stop_flag
    done = False
    stop_flag = False
    threading.Thread(target=compute, daemon=True).start()

def stop():
    global stop_flag
    stop_flag = True
    status_label.config(text="⛔ Arrêt demandé")

tk.Button(root, text="▶️ Lancer", command=start, bg="#333", fg="white").pack(pady=5)
tk.Button(root, text="⏹ Arrêter", command=stop, bg="#550000", fg="white").pack()

# Calcul intelligent
def compute():
    global done

    try:
        n = int(nb_var.get())
    except:
        status_label.config(text="❌ Nombre invalide")
        return

    status_label.config(text="Calcul en cours...")

    mp.mp.dps = n
    pi = ""

    start_time = time.time()

    # calcul en blocs
    block_size = 10000
    total_blocks = n // block_size

    with open(file_path.get(), "w") as f:

        for i in range(total_blocks):
            if stop_flag:
                status_label.config(text="⛔ Arrêté")
                done = True
                return

            current_digits = (i + 1) * block_size
            mp.mp.dps = current_digits
            pi = str(mp.pi)

            # sauvegarde
            f.seek(0)
            f.write(pi)
            f.flush()

            # progression réelle
            p = (current_digits / n) * 100
            progress['value'] = p
            percent_label.config(text=f"{int(p)} %")

            # temps restant
            elapsed = time.time() - start_time
            est_total = elapsed / (p/100)
            remaining = max(est_total - elapsed, 0)
            time_label.config(text=f"Temps restant: {int(remaining)} s")

            root.update()

    # final
    f.write(str(mp.pi))
    status_label.config(text="✅ Terminé !")
    progress['value'] = 100
    percent_label.config(text="100 %")
    done = True

root.mainloop()
