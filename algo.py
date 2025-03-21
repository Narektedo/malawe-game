
import copy

def play(board: list[list[int]], player: int, cell: int) -> int:
    """Joue un coup sur le plateau en distribuant les graines et retourne le nombre de graines collectées.
    param board: plateau de jeu
    param player: joueur actif
    param cell: case à jouer
    return: nombre de graines collectées
    """
    
    lenght = len(board[player]) - 1  # Dernière case du joueur
    seeds = board[player][cell]  # Nombre de graines à semer
    board[player][cell] = 0  # On prend toutes les graines de cette case

    position_player = player
    collected = 0  # Graines collectées

    while seeds > 0:  # Tant qu'il reste des graines à semer
        cell += 1  # On avance d'une case

        # Si on atteint la fin du tableau, on change de camp
        if cell > lenght:
            position_player = 1 - position_player  # Changement de joueur
            cell = 0  # Repartir du début

        # On sème une graine
        board[position_player][cell] += 1
        seeds -= 1  #on seme une graine donc on la retire

# On capture les graines si il y a entre 2 et 3 graines dans la case (dans les cases consécutives) et que dans les cases ennemies
    while position_player == 1 - player and board[position_player][cell] in [2, 3]:
        collected += board[position_player][cell]
        board[position_player][cell] = 0
        cell -= 1  # On recule pour voir si on peut continuer à capturer

        # On ne capture pas sur la ligne du joueur actif
        if cell < 0:
            position_player = player  # On revient à la ligne du joueur actif donc on change la variable et casse la boucle

    return collected  # Nombre total de graines collectées


def is_end(board, player: int) -> bool:
    """Fonction qui assure la fin de la partie si un joueur n'a plus de graines
    param board: plateau de jeu
    param player: joueur actif
    return : True si le jeu est fini et que le joueur n'a plus de graines, False sinon"""
    if sum(board[player]) == 0:
      #  print(f"Le camp du joueur {player} n'a plus de graines après ce coup.")
        return True
    return False
        
 
def has_valid_move(board, player: int) -> bool:
    """Vérifie si le joueur a au moins un coup valide qui ne rend pas l'adversaire affamé.
    param board: plateau de jeu
    param player: joueur actif
    return: True si un coup valide existe, False si la seule option est d'affamer l'adversaire"""
    
    ennemy = 1 - player  # Définir l'adversaire

    for cell in range(len(board[player])):  # Parcourir toutes les cases du joueur
        if board[player][cell] > 0:  # Vérifier si la case contient des graines
            
            board_copy = copy.deepcopy(board)  # Copier le plateau avant de jouer
            play(board_copy, player, cell)  # Simuler le coup

            if not is_end(board_copy, ennemy):  
                # Vérifier si l'adversaire a encore des graines après le coup
                return True  # Au moins un coup valide existe

    return False  # Aucun coup valide trouvé




def enum(board: list[list[int]], player: int, depth: int) -> list[tuple[list[int], int]]:
    """Énumère toutes les suites de coups possibles et retourne une liste de tuples avec les mouvements et le score final.
    param board: plateau de jeu
    param player: joueur actif
    param depth: nombre de coups à regarder en avant
    return: liste de tuples avec tout les mouvements et les scores finaux possibles
    """
    
    ennemy = 1 - player  # L'adversaire est l'autre joueur

    # Base case : Si on atteint la profondeur maximale ou si le jeu est terminé
    if depth == 0 or is_end(board, player):
        return [([], 0)]  # Retourne une séquence vide avec un score de 0
    
    moves = []  # Liste des mouvements possibles
    for cell in range(len(board[player])):  # Parcours des cases du joueur actuel
        if board[player][cell] > 0:  # Si la case a des graines à semer
            board_copy = copy.deepcopy(board)  # Faire une copie du plateau
            collect = play(board_copy, player, cell)  # Jouer le coup (retourne le nombre de graines collectées)
            if is_end(board_copy, ennemy):
                if has_valid_move(board, player):
                    print(f"Le joueur {player} veut affamer son adversaire alors qu'il a d'autres coups possibles")
                    continue


            # Si c'est l'adversaire qui collecte, on inverse le score
            if player == 1:  
                collect = -collect

            # Vérification si le jeu est terminé après le coup

            # Récursion pour les coups suivants
            next_moves = enum(board_copy, 1 - player, depth - 1)

            # Accumuler les graines collectées du coup actuel et des coups suivants
            for seq in next_moves:
                moves.append(([cell] + seq[0], collect + seq[1]))  # On additionne le score collecté
               

    return moves


def suggest(board: list[list[int]], player: int, depth: int) -> int:
    """Propose le meilleur coup possible pour un joueur donné en utilisant l'algorithme Minimax.
    param board: plateau de jeu
    param player: joueur actif
    param depth: profondeur de recherche
    return: le meilleur coup à jouer"""

    _, best_move = min_max(board, player, depth) #on garde que le meilleur coup

    return best_move

# Initialisation du minimax
def min_max(board: list[list[int]], player: int, depth: int, total_1 =0, total_2 = 0) -> int:
    """Algorithme Minimax qui cherche le meilleur coup pour le joueur 1 et le coup qui réduit le plus les pertes chez le joueur deux et
      retourne le score et le meilleur coup possible en fonction d'une profondeur donnée.
    param board: plateau de jeu
    param player: joueur actif
    param depth: profondeur de recherche
    param total_1: score du joueur 1
    param total_2: score du joueur 2
    return: score et meilleur coup possible
    """    
    # cas de base si la profondeur est atteint ou si le jeu prends fin
    if depth == 0 or is_end(board, player):

        #on retourne la différence des scores des deux joueurs
        return (total_1 - total_2, -1)

    if player == 0:
        #on definit un score très très bas inatteignable
        best_score = -1000
        best_move = -1
        #on regarde chaque coup possible
        for cell in range(len(board[player])):
            if board[player][cell]>0: # si il y a des graines
                board_copy = copy.deepcopy(board) # on copie pour pas que les changements affectent le plateau de jeu
                collect = play(board_copy, player, cell) #on joue le coup et récupère le nombre de graines collectées

                if is_end(board_copy, 1-player): #si la partie finie
                    if has_valid_move(board, player): #on vérifie si il y a un autre coup possible qui n'affame pas le joueur adverse
                        print(f"Le joueur {player} veut affamer son adversaire alors qu'il a d'autres coups possibles")
                        continue

                #récursion pour les coups suivants
                score, _ = min_max(board_copy, 1-player, depth-1, total_1 + collect, total_2)

                #on garde le meilleur score
                if score > best_score:
                    best_score = score
                    best_move = cell

        return best_score ,best_move
    
    else:
        #on définit un score très très haut inatteugnable
        best_score = 1000
        best_move = -1
    #on regarde chaque coup possible
    for cell in range (len(board[player])):
            if board[player][cell]>0: #si il y a des graines
                board_copy = copy.deepcopy(board) #on copie pour pas que les changements affectent le plateau de jeu
                collect = play(board_copy, player, cell) #on joue le coup et récupère le nombre de graines collectées

                if is_end(board_copy, 1-player): #si la partie finie
                    if has_valid_move(board, player): #on vérifie si il y a un autre coup possible qui n'affame pas le joueur adverse
                        print(f"Le joueur {player} veut affamer son adversaire alors qu'il a d'autres coups possibles")
                        continue
                score, _ = min_max(board_copy, 1-player, depth-1, total_1, total_2 + collect)

                #on garde le meilleur score
                if score < best_score:
                    best_score = score
                    best_move = cell
    return best_score, best_move

    

