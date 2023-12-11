#****PROJET INFORMATIQUE KIMIA ET CLARA****#
import curses
stdscr = curses.initscr()
curses.noecho()
curses.start_color()
curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_WHITE)
curses.init_pair(2,curses.COLOR_BLACK,curses.COLOR_WHITE)
curses.init_pair(3,curses.COLOR_RED,curses.COLOR_WHITE)
curses.init_pair(4,curses.COLOR_WHITE,curses.COLOR_WHITE)
curses.init_pair(5,curses.COLOR_YELLOW,curses.COLOR_WHITE)
import random
import datetime

##MAP
def display_map(m,d):
    for i in range(len(m)):
        for j in range(len(m[i])):
            if m[i][j]==0:
                print(d[0], end="")
            else:
                print(d[1], end="")
        print(" ")

map = [[0,0,0,1,1],
[0,0,0,0,1],
[1,1,0,0,0],
[0,0,0,0,0]]

dico = {0:' ',1:'█'}

#print(display_map(map,dico))

## CREATION PERSONNAGE
def create_perso(départ):
    d={}
    d["Argent"]=0
    d["char"]="☻"
    d["x"]=départ[0]
    d["y"]=départ[1]
    return d


#print(perso)

##2.2
def fusion(d,p):      #on va fusionner notre dictionnaire de personnage et notre
    d1 = d.copy()     #dico des information sur la carte pour une faciliter d'accèes aux informations
    d1.update(p)
    return d1
#print(fusion(dico,perso))

def display_map_char(m,p,d):
    d1 = fusion(d,p)
    for i in range(len(m)):
        for j in range(len(m[i])):
            if j==p['x'] and i==p['y']:
                stdscr.addstr(i,j,p['char'])
            else:
                stdscr.addstr(i,j,d[m[i][j]])#parce qu'on à deja les indices avec les i,j
            #else:
               #print(d[1], end="")
        #print(" ")

#print(display_map_char(map,dico,perso))
    
#print(perso)

##DEPLACEMENT DU PERSONNAGE
def update_p(letter,p,m):
    if (letter in ["z","q","s","d"]):
        if letter == "z"and p['x']-1 >= 0 and m[p["x"]-1][p["y"]]!=1:
            p['x']-=1
        elif letter =="s" and p['x']+1 < len(m) and m[p["x"]+1][p["y"]]!=1:
            p['x']+=1
        elif letter=="d"and p['y']+1 < len(m[0]) and m[p["x"]][p["y"]+1]!=1:
            p['y']+=1
        elif letter=="q"and p['y']-1 >= 0 and m[p["x"]][p["y"]-1]!=1:
            p['y']-=1
    else:
        stdscr.addstr(len(m) + 2, 0,"erreur, vous n'avez pas indiqué un caractère dans {z,q,s,d}")
    return p

#On crée une fonction choisir symbole qui choisir de manière aléatoire un symbole parmis les élement de notre liste
def choisir_symbole():
    symboles = ["$", "£", "€"]
    symbole_choisi = random.choice(symboles)
    return symbole_choisi

##Fonction créer trou qu'on utilise plus mais qui nous a permis d'avoir l'idée pour implémenter le trou 
def creer_trou(random_map):
    t={}
    x = random.randint(0, len(random_map[0]) - 1)
    y = random.randint(0, len(random_map) - 1)
    while random_map[y][x] != 0:
        x = random.randint(0, len(random_map[0]) - 1)
        y = random.randint(0, len(random_map) - 1)
    t["x"],t["y"]=x,y
    return t

def creates_object(nb_objects,m):
    obj_position=set()
    while len(obj_position) < nb_objects:
        i = random.randint(0,len(m)-1)
        j = random.randint(0,len(m[0])-1)
        if m[i][j] == 0:
            obj_position.add((i,j))
    return obj_position
#print(object)

def display_map_char_object (m,p,d,objects,dico_valeur_objects):
    for i in range(len(m)):
        for j in range(len(m[i])):
            if j==p['y'] and i==p['x']:
                stdscr.addstr(i,j,p['char'],curses.color_pair(2))
            elif (i,j)in objects:
                stdscr.addstr(i,j,dico_valeur_objects[(i,j)],curses.color_pair(1))
            elif(m[i][j]==3):
                if len(objects)==0:
                    stdscr.addstr(i,j,'X',curses.color_pair(3))
                else:
                    stdscr.addstr(i,j,' ',curses.color_pair(4))
            elif(m[i][j]==2):
                stdscr.addstr(i,j,' ',curses.color_pair(4))
            elif(m[i][j]==4):
                stdscr.addstr(i,j,'@',curses.color_pair(3)) #Piège Invisible
            else:
                stdscr.addstr(i,j,d[m[i][j]],curses.color_pair(5))
    stdscr.addstr(len(m) + 1, 0,f"Argent: {p['Argent']}")

##FONCTION UPDATE OBJECT 
def update_object(p,objects,dico_valeur_objects):
    if (p['x'], p['y']) in objects:
        if dico_valeur_objects[(p['x'], p['y'])]=="$": #Si le perso ramasse un '$' alors on ajoute 1 à l'argent total
            p["Argent"]+=1
        elif dico_valeur_objects[(p['x'], p['y'])]=="£": #Si le perso ramasse un '£' alors on ajoute 3 à l'argent total
            p["Argent"]+=3
        elif dico_valeur_objects[(p['x'], p['y'])]=="€":#Si le perso ramasse un '€' alors on ajoute 5 à l'argent total
            p["Argent"]+=5
        objects.discard((p['x'], p['y']))

    return objects

##FONCTION GENERATE RANDOM MAP
def generate_random_map(size_map,proportion_wall):
    mapran=[[0 for i in range(size_map[0])] for j in range(size_map[1])] #On crée une matrice vide au début 
    nbrelementtot=0
    for i in range(len(mapran)):
        for j in range(len(mapran[0])):
            nbrelementtot+=1  #On compte le nombre d'élement au total dans la matrice exemple(matrice(40,10)-->400 élement)
    nbrmurs=0
    #boucle while pour verifier que le proportion nombre d"element aléatoirmement ajouté est inférieur à la proporttion
    while nbrmurs/nbrelementtot<proportion_wall:
        i,j=random.randint(0,len(mapran)-1),random.randint(0,len(mapran[0])-1)
        mapran[i][j]=1 #on met un 1 dans la matrice, il y mettra un mur lors de la conversion avec le dictionnaire
        nbrmurs+=1
    entreepasmise=True
    while entreepasmise:
        k,l=random.randint(0,len(mapran)-1),random.randint(0,len(mapran[0])-1) #coordonées de l'entrée
        if mapran[k][l]!=1:
            mapran[k][l]=2
            entreepasmise=False
    sortiepasmise=True
    while sortiepasmise:
        k,l=random.randint(0,len(mapran)-1),random.randint(0,len(mapran[0])-1) #coordonées de la sortie
        if mapran[k][l]!=1 and mapran[k][l]!=2:
            mapran[k][l]=3
            sortiepasmise=False         
    troupasmis=True
    while troupasmis:
        k,l=random.randint(0,len(mapran)-1),random.randint(0,len(mapran[0])-1) #coordonées du trou
        if mapran[k][l]==1:
            mapran[k][l]=4
            troupasmis=False  
    return mapran

#FONCTION CREATE NEW LEVEL

def create_new_level(perso,newmap,objects,size_map,proportion_wall,nb_objects,dico_valeur_objects):
    newmap=generate_random_map(size_map,proportion_wall)#notre nouvelle map est une map générée aléatoirement 
    objects=creates_object(nb_objects,newmap) #on crée des objets a des nouvelles positions
    dico_valeur_objects={}
    for i in objects:
        dico_valeur_objects[i]=choisir_symbole() #on ajoute des nouvelle valeur dans notre dictionnaire; des nouveaux objets donc 
    #On recherche dans newmap(la nouvelle map) la position de l'entrée 
    for i in range(len(newmap)):
        for j in range(len(newmap[0])):
            if newmap[i][j]==2:
                perso["x"],perso["y"]=i,j
                break #pour qu'il arrete dès qu'il a fini vu que pas besoin de plus, apres on l'a mis nnul part ailleurs onc j'ai peut qu'elle pense que c'est pas nous mdrrr
    return newmap,objects,dico_valeur_objects
    
proportion_wall=0.09 #proportion de mur en fonction de la taile de la map 

size_map=(40,10) #taille de la map: 40 de long et 10 de large
nb_objects=5 #on choisi le nombre d'objet qu'on veut sur chaque map 
objectif=40 #On place un objectif de 50 pour l'exemple


objects = creates_object(nb_objects,map)
dico_valeur_objects={}#On crée ce dictionnaire qui à chaque positon d'argent(clé) associe le symbole {(2,3):"Eur", (4,5):"Dollar"}
for i in objects: #comme ça on est sur d'avoir des symboles différents ou non sur notre map
    dico_valeur_objects[i]=choisir_symbole()
random_map=generate_random_map(size_map,proportion_wall)
for i in range(len(random_map)):
    for j in range(len(random_map[i])):#on place notre perso à une position (i,j)==2
        if(random_map[i][j]==2):
            départ=(i,j)
            break

#AFFICHAGE DES REGLES DU JEU
stdscr.addstr(2, 15,"$   THE BUISNESS MAN   $")
stdscr.addstr(4,1,"Vous venez d'entrer dans le monde du travail !")
stdscr.addstr(5,1,"Votre objectif, gagner un maximum d'argent avant votre retraite.")
stdscr.addstr(6,1,"Les '$' vous aportent 1 euros, les '£'vous en aportent 3 et enfin les '€' vous en apportent 5!")
stdscr.addstr(7,1,"ATTENTION ! Les impôts peuvent vous tomber dessus à n'importe quel moment et vous faire ")
stdscr.addstr(8,1,"perdre jusqu'à 30 pourcent de vos gains")
stdscr.addstr(9,1,"Bon courage ! ")
stdscr.addstr(10,1,"(Vous pouvez vous déplacer avec {'z','q','s' et'd'appuyez sur 'd' pour commencer et 'p' pour quitter)")

#stdscr.addstr(len(random_map) + 3, 0,"%d,%d"%(départ[0],départ[1])) --> permettais de vérifier la position de notre personnage 
perso = create_perso(départ)

jeuencours=True
Variabletotalementinutiledansleresteducode=1

while jeuencours:
    c = stdscr.getkey()
    if Variabletotalementinutiledansleresteducode==1:
        start_time = datetime.datetime.now()#ne pas oublier de mettre import time en haut
        Variabletotalementinutiledansleresteducode=100 #Pour que le if ne soit plus jamais vrai
    # variable égale à 1. j'ai un if qui ne sera vrai qu'une seule fois tout au long de mon code 
    # sure que start a été initialisé qu'une seule fois. Alors il le prends en secondes donc plus besoin de conversion.
    if c=="p":
        break
    stdscr.erase() # on efface l'ecran
    update_p(c, perso, random_map)
    if random_map[perso["x"]][perso["y"]]==4:
        perso["Argent"]=int(perso["Argent"]*0.7)#Si on tombe sur le trou on multiplie l'argent total par 0.7 ce qui nous enlève donc 30%
        stdscr.addstr((len(random_map)+4),0,"OH NON ! Payez vos impôts! ")
    update_object(perso,objects,dico_valeur_objects)
    display_map_char_object(random_map, perso, dico,objects,dico_valeur_objects)# on affiche la carte et la joueur
    if random_map[perso["x"]][perso["y"]]==3 and len(objects)==0: #si notre perso se trouve sur 'X' et qu'il n'y a plus d'objets
        stdscr.addstr((len(random_map)+5),0,"Vous avez rejoins une nouvelle entreprise ! (Appuyez sur 'd' pour continuer)") #Ce texte s'affiche quand on arrive sur 'X' avant d echanger de map
        random_map,objects,dico_valeur_objects=create_new_level(perso,random_map,objects,size_map,proportion_wall,nb_objects,dico_valeur_objects)
    stdscr.refresh() 
    jeuencours=True
    if perso["Argent"]>=objectif:
        jeuencours=False  #ca nous fait sortir de la boucle
    stdscr.refresh()
end_time = datetime.datetime.now()
stdscr.erase() 
#fin du jeu

while True:

    perso["Argent"]>=objectif
    time_diff = (end_time - start_time)
    execution_time = str(round(time_diff.total_seconds())) #ce qui le met en seconde si je fais pas d'erreurs
    stdscr.addstr(0,0,f"Félicitations !Vous avez gagner , Argent: {perso['Argent']}")
    stdscr.addstr(1,0,f"Vous avez mis {execution_time} secondes")
    stdscr.refresh()
    c = stdscr.getkey()
    if c=="p":
        break