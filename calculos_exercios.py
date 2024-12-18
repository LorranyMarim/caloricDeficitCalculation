import tkinter as tk
from tkinter import messagebox

def validaSexo(s):
    """Valida se o sexo é 'F' ou 'M'."""
    if len(s) != 1 or (s.lower() not in ["f", "m"]):
        return False
    return True

def validaPerfilAtividade(pa):
    """Valida se o perfil de atividade está entre 1 e 5."""
    try:
        pa = int(pa)
        if pa not in [1, 2, 3, 4, 5]:
            return False
        return True
    except ValueError:
        return False

def calculoTMB(s, p, a, i):
    """Calcula a Taxa Metabólica Basal (TMB)."""
    if s.lower() == "f":
        calc = 447.593 + (9.247 * p) + (3.098 * a) - (4.330 * i)
    elif s.lower() == "m":
        calc = 88.362 + (13.397 * p) + (4.799 * a) - (5.677 * i)
    return calc

def calculoTDEE(tm, ta):
    """Calcula o Gasto Energético Diário Total (TDEE) com base no perfil de atividade."""
    if ta == 1:
        return tm * 1.2
    elif ta == 2:
        return tm * 1.375
    elif ta == 3:
        return tm * 1.55
    elif ta == 4:
        return tm * 1.725
    elif ta == 5:
        return tm * 1.9

def planoExercicio(p):
    """Calcula as calorias queimadas em diferentes velocidades e tipos de exercício e retorna o resultado como texto."""
    met_dict_corrida = {
        "v8": {"kmH": 8, "met": 8.3},
        "v10": {"kmH": 10, "met": 9.8},
        "v12": {"kmH": 12, "met": 11.0},
        "v14": {"kmH": 14, "met": 13.3}
    }
    
    met_dict_musculacao = {
        "leve": {"met": 3.5},
        "moderada": {"met": 6.0},
        "intensa": {"met": 8.0}
    }
    
    resultado = "~~Corrida~~\n"
    for chave, valores in met_dict_corrida.items():
        calorias_queimadas = valores["met"] * p * 1
        resultado += f"Ritmo: {valores['kmH']} km/h | 01:00h duração | {calorias_queimadas:.2f} queima calórica\n"
    
    resultado += "\n~~Musculação~~\n"
    for chave, valores in met_dict_musculacao.items():
        calorias_queimadas_musculacao = valores["met"] * p * 1
        resultado += f"Musculação {chave.capitalize()} | 01:00h duração | {calorias_queimadas_musculacao:.2f} queima calórica\n"

    return resultado

def calcular():
    """Função principal para calcular TMB, TDEE e Déficit Calórico."""
    try:
        peso = float(entry1.get())
        altura = float(entry2.get())
        idade = int(entry3.get())
        sexo = entry4.get()
        perfilAtividade = int(entry5.get())

        # Validações
        if peso <= 1 or altura < 1 or altura > 300 or idade < 1 or idade > 120:
            messagebox.showerror("Erro", "Peso deve ser maior que 1kg, altura deve ser entre 1 e 300cm e idade deve ser maior que 1 e menor que 120 anos.")
            return

        if not validaSexo(sexo):
            messagebox.showerror("Erro", "Sexo inválido. Deve ser F ou M.")
            return

        if not validaPerfilAtividade(perfilAtividade):
            messagebox.showerror("Erro", "Perfil de atividade inválido. Deve ser um número de 1 a 5.")
            return

        # Cálculos
        tmb = calculoTMB(sexo, peso, altura, idade)
        tdee = calculoTDEE(tmb, perfilAtividade)
        deficitCalorico = tdee - 500  # Para perder ~0.5kg, deve-se criar um déficit de 500 calorias/dia.

        output_text.delete(1.0, tk.END)

        output_text.tag_configure("gray", foreground="gray")

        output_text.insert(tk.END, f"=============== Resultado ===============\n")
        output_text.insert(tk.END, f"Peso: {peso} kg\n")
        output_text.insert(tk.END, f"Altura: {altura} cm\n")
        output_text.insert(tk.END, f"Idade: {idade} anos\n")
        output_text.insert(tk.END, f"Sexo: {sexo.upper()}\n\n")
        output_text.insert(tk.END, f"TMB: {tmb:,.2f} calorias/dia\n")
        output_text.insert(tk.END, f"*Taxa metabólica basal (TMB) é uma estimativa da quantidade de calorias que seu corpo precisa para manter suas funções vitais em repouso, como respiração, circulação e digestão\n\n", "gray")
        output_text.insert(tk.END, f"TDEE: {tdee:,.2f} calorias/dia\n")
        output_text.insert(tk.END, f"*Gasto Energético Diário Total (TDEE) é a quantidade de calorias que você queima por dia considerando atividades físicas\n\n", "gray")
        output_text.insert(tk.END, f"Déficit Calórico: {deficitCalorico:,.2f} calorias/dia\n")
        output_text.insert(tk.END, f"*Para perder aproximadamente ~0.5kg por semana é necessário queimar o valor calórico acima\n\n", "gray")
        output_text.insert(tk.END, f"======= Referência para Exercícios =======\n")
        output_text.insert(tk.END, planoExercicio(peso))

    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")

root = tk.Tk()
root.title("Calcular Perda Calórica")

frame_left = tk.Frame(root)
frame_left.pack(side=tk.LEFT, padx=10, pady=10, anchor='nw')

frame_right = tk.Frame(root)
frame_right.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

label1 = tk.Label(frame_left, text="Insira o peso (kg)")
label1.pack(anchor='w')
sublabel1 = tk.Label(frame_left, text="Exemplo: 58", fg="gray")
sublabel1.pack(anchor='w', pady=(0,5))  
entry1 = tk.Entry(frame_left)
entry1.pack(anchor='w')

label2 = tk.Label(frame_left, text="Insira a altura (cm)")
label2.pack(anchor='w')
sublabel2 = tk.Label(frame_left, text="Exemplo: 165", fg="gray")
sublabel2.pack(anchor='w', pady=(0,5))
entry2 = tk.Entry(frame_left)
entry2.pack(anchor='w')

label3 = tk.Label(frame_left, text="Insira sua idade")
label3.pack(anchor='w')
sublabel3 = tk.Label(frame_left, text="Exemplo: 20", fg="gray")
sublabel3.pack(anchor='w', pady=(0,5))
entry3 = tk.Entry(frame_left)
entry3.pack(anchor='w')

label4 = tk.Label(frame_left, text="Insira o sexo")
label4.pack(anchor='w')
sublabel4 = tk.Label(frame_left, text="F ou M", fg="gray")
sublabel4.pack(anchor='w', pady=(0,5))
entry4 = tk.Entry(frame_left)
entry4.pack(anchor='w')

label5 = tk.Label(frame_left, text="Perfil de atividade física")
label5.pack(anchor='w')
sublabel5 = tk.Label(frame_left, text="1: Sedentário (pouco ou nenhum exercício)\n2: Levemente ativo (exercício leve 1-3 dias por semana)\n3: Moderadamente ativo (exercício moderado 3-5 dias por semana)\n4: Muito ativo (exercício intenso 6-7 dias por semana)\n5: Extremamente ativo (trabalho físico pesado ou exercício intenso)", fg="gray", justify='left')
sublabel5.pack(anchor='w', pady=(0,5))
entry5 = tk.Entry(frame_left)
entry5.pack(anchor='w')

calcular_button = tk.Button(frame_left, text="Calcular", command=calcular)
calcular_button.pack(pady=10, anchor='w')

output_text = tk.Text(frame_right, width=40, height=20)
output_text.pack(fill=tk.BOTH, expand=True)

root.mainloop()
