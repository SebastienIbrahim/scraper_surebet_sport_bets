import tkinter as tk
from tkinter import ttk
from find_surbet import find_surebets, display_info


def display_surebets_info(surebets_data):
    window = tk.Tk()
    window.title("Surebets Information")

    tree = ttk.Treeview(window)
    tree["columns"] = (
        "Match",
        "Bookmakers",
        "Cotes",
        "Montants de mise",
        "Mise totale",
        "Gains",
        "Gain total",
    )

    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("Match", anchor=tk.CENTER, width=150)
    tree.column("Bookmakers", anchor=tk.CENTER, width=200)
    tree.column("Cotes", anchor=tk.CENTER, width=200)
    tree.column("Montants de mise", anchor=tk.CENTER, width=200)
    tree.column("Mise totale", anchor=tk.CENTER, width=100)
    tree.column("Gains", anchor=tk.CENTER, width=200)
    tree.column("Gain total", anchor=tk.CENTER, width=100)

    tree.heading("#0", text="", anchor=tk.CENTER)
    tree.heading("Match", text="Match", anchor=tk.CENTER)
    tree.heading("Bookmakers", text="Bookmakers", anchor=tk.CENTER)
    tree.heading("Cotes", text="Cotes", anchor=tk.CENTER)
    tree.heading("Montants de mise", text="Montants de mise", anchor=tk.CENTER)
    tree.heading("Mise totale", text="Mise totale", anchor=tk.CENTER)
    tree.heading("Gains", text="Gains", anchor=tk.CENTER)
    tree.heading("Gain total", text="Gain total", anchor=tk.CENTER)

    for i, (bookmakers, surebet_info) in enumerate(surebets_data.items(), start=1):
        match = surebet_info["Match"]
        bookmakers_str = ", ".join(bookmakers)
        cotes_str = ", ".join(f"{k}: {v}" for k, v in surebet_info["Cotes"].items())
        montants_mise_str = ", ".join(
            f"{k}: {v}" for k, v in surebet_info["Montants de mise"].items()
        )
        gains_str = ", ".join(f"{k}: {v}" for k, v in surebet_info["Gains"].items())
        mise_totale = surebet_info["Mise_totale"]
        gain_total = surebet_info["Gain_total"]

        tree.insert(
            "",
            i,
            values=(
                match,
                bookmakers_str,
                cotes_str,
                montants_mise_str,
                mise_totale,
                gains_str,
                gain_total,
            ),
        )

    tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    window.mainloop()


# Exemple d'utilisation avec les nouvelles données que vous avez fournies
data = {
    "Match de test": [
        {
            "Bookmaker A": {
                "victoire_equipe_a": 20.0,
                "victoire_equipe_b": 3.0,
                "match_nul": 4.0,
            }
        },
        {
            "Bookmaker B": {
                "victoire_equipe_a": 2.2,
                "victoire_equipe_b": 3.5,
                "match_nul": 3.8,
            }
        },
        {
            "BookmakerC": {
                "victoire_equipe_a": 2.5,
                "victoire_equipe_b": 30.2,
                "match_nul": 3.0,
            }
        },
    ]
}

1/20 + 1/3 + 1/4
def find_surebets(data, total_stake=100):
    surebets = {}

    for match, bookmakers_list in data.items():
        n = len(bookmakers_list)
        
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    bookmaker_a, data_a = list(bookmakers_list[i].items())[0]
                    bookmaker_b, data_b = list(bookmakers_list[j].items())[0]
                    bookmaker_c, data_c = list(bookmakers_list[k].items())[0]
                    cote_victoire_a = data_a["victoire_equipe_a"]
                    cote_victoire_b = data_b["victoire_equipe_b"]
                    cote_match_nul = data_c["match_nul"]
                    print(i, j, k)
                    print(1 / cote_victoire_a + 1 / cote_victoire_b + 1 / cote_match_nul)

                    # Vérification d'une opportunité de surebet
                    if (
                        1 / cote_victoire_a + 1 / cote_victoire_b + 1 / cote_match_nul
                        < 1
                    ):
                        M = total_stake / (
                            1 / cote_victoire_a
                            + 1 / cote_victoire_b
                            + 1 / cote_match_nul
                        )
                        print("M", M)
                        mise_victoire_a = round(M / cote_victoire_a, 2)
                        mise_victoire_b = round(M / cote_victoire_b, 2)
                        mise_match_nul = round(M / cote_match_nul, 2)

                        gain_victoire_a = round(mise_victoire_a * cote_victoire_a, 2)
                        gain_victoire_b = round(mise_victoire_b * cote_victoire_b, 2)
                        gain_match_nul = round(mise_match_nul * cote_match_nul, 2)
                        gain_total = round(
                            gain_victoire_a + gain_victoire_b + gain_match_nul, 2
                        )

                        # Vérification des gains strictement positifs
                        if M > 0 and gain_total > total_stake:
                            surebet = {
                                "Match": match,
                                "Cotes": {
                                    "Cote victoire équipe A": cote_victoire_a,
                                    "Cote victoire équipe B": cote_victoire_b,
                                    "Cote match nul": cote_match_nul,
                                },
                                "Montants de mise": {
                                    "Mise victoire équipe A": mise_victoire_a,
                                    "Mise victoire équipe B": mise_victoire_b,
                                    "Mise match nul": mise_match_nul,
                                },
                                "Mise_totale": round(M, 2),
                                "Gains": {
                                    "Gain victoire équipe A": gain_victoire_a,
                                    "Gain victoire équipe B": gain_victoire_b,
                                    "Gain match nul": gain_match_nul,
                                },
                                "Gain_total": gain_total,
                            }
                            surebets[(bookmaker_a, bookmaker_b, bookmaker_c)] = surebet

    return surebets








total_stake = 100  # Mise totale que vous prévoyez de parier

opportunites_surebet = find_surebets(data, total_stake)
for bookmakers, surebet_info in opportunites_surebet.items():
    print("Bookmakers:", bookmakers)
    for key, value in surebet_info.items():
        if key == "Cotes" or key == "Montants de mise" or key == "Gains":
            display_info(key, value)
        else:
            print(f"{key}: {value}")
    print()

display_surebets_info(opportunites_surebet)
