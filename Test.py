#avec le temps mais sans le trou 
import curses
stdscr = curses.initscr()
curses.noecho()
import random
import datetime


def display_map_char_object (m,p,d,objects,argent):
    d1 = fusion(d,p)
    for i in range(len(m)):
        for j in range(len(m[i])):
            if j==p['x'] and i==p['y']:
                stdscr.addstr(i,j,p['char'])
            elif (i,j)in objects:
                stdscr.addstr(i,j,argent)
            elif(m[i][j]==3):
                stdscr.addstr(i,j,'X')
            elif(m[i][j]==2):
                stdscr.addstr(i,j,' ')
            else:
                stdscr.addstr(i,j,d[m[i][j]])

    stdscr.addstr(len(m) + 1, 0,f"Score: {p['score']}")
    


def update_object(p,objects,argent):
    if (p['y'], p['x']) in objects:
        if argent=="$":
            p["score"]+=1
        elif argent=="£":
            p["score"]+=2
        elif argent=="€":
            p["score"]+=3
        objects.discard((p['y'], p['x']))

    return objects
def generate_random_map(size_map,proportion_wall):
    mapran=[]
    mapran=[[0 for i in range(size_map[0])] for j in range(size_map[1])]

    nbrelementtot=0
    for i in range(len(mapran)):
        for j in range(len(mapran[0])):
            nbrelementtot+=1   #est ce que tu penses qu'on devrait utiliser la fct count a la place d'une boucle? 
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
        k,l=random.randint(0,len(mapran)-1),random.randint(0,len(mapran[0])-1) #coordonées de la sorite #coordonées de l'entrée
        if mapran[k][l]!=1:
            mapran[k][l]=3
            sortiepasmise=False
    
    return mapran
#111111111
def create_new_level(perso,newmap,objects,size_map,proportion_wall,nb_objects):
    argent=choisir_symbole()
    newmap=generate_random_map(size_map,proportion_wall)
    objects=creates_object(nb_objects,newmap) #on crée des objets a des nouvelles positions
    #de base je voulais mettre en argument k t l mais je me dis vu l'ennoncé qu'on a peut etre pas le droit ducoup on recher dans map la position de l'entrée 
    for i in range(len(newmap)):
        for j in range(len(newmap[0])):
            if newmap[i][j]==2:
                perso["x"],perso["y"]=i,j
                break #pour qu'il arrete dès qu'il a fini vu que pas besoin de plus, apres on l'a mis nnul part ailleurs onc j'ai peut qu'elle pense que c'est pas nous mdrrr
    return newmap
    
                
                

    


proportion_wall=0.15
  
size_map=(9,9)    
nb_objects=4 
 
 
objects = creates_object(nb_objects,map)
random_map=generate_random_map(size_map,proportion_wall)
for i in range(len(random_map)):
    for j in range(len(random_map[i])):
        if(random_map[i][j]==2):
            départ=(i,j)
            break
stdscr.addstr(len(random_map) + 3, 0,"%d,%d"%(départ[0],départ[1]))
perso = create_perso(départ)
argent=choisir_symbole()
jeuencours=True



while jeuencours:
    start_time = datetime.datetime.now() #ne pas oublier de mettre import time en haut
    c = stdscr.getkey()
    stdscr.erase() # on efface l'ecran
    update_p(c, perso, random_map)
    update_object(perso,objects,argent)
    display_map_char_object(random_map, perso, dico,objects,argent)# on affiche la carte et la joueur    
    if random_map[perso["y"]][perso["x"]]==3:
        stdscr.addstr(0,0,"Nouveau monde!")# ca il faudra l'enlever mais c'est juste pour voir où ca marche pas 
        random_map=create_new_level(perso,random_map,objects,size_map,proportion_wall,nb_objects)
    #stdscr.refresh() #le refresh avant ou apres le if?
    jeuencours=True
    if perso["score"]>=5:
        end_time = datetime.datetime.now()
        jeuencours=False  #ca nous fait sortir de la boucle
    stdscr.refresh()

        
#le jeu est fini: l'affichage 
if perso["score"]>=5:
    time_diff = (end_time - start_time)
    execution_time = str(time_diff.total_seconds() *1000) #ce qui le met en seconde si je fais pas d'erreurs
    #apres là je calibrerai quand on aura fini pour avoir un truc un peu cohérant mais en gros faire une conversion pour avoir un nombre d'année entre 20 ans et 80 ans 
    stdscr.addstr(0,0,execution_time)#"FELICITATION! Vous avez gagné assez d'argent pour prendre votre retraite à %f ans"
    #je chercherai dans mon cours de L1 demain comment marche les %f je m'en souviens plus     
else:#donc le cas où on a perdu 
    stdscr.addstr(0,0,"DOMMAGE! Vous avez perdu, votre score est de")

#stdscr.addstr(2, 15,"$   THE BUISNESS MAN   $")
#stdscr.addstr(4,1,"Vous venez d'entrer dans le monde du travail !")
#stdscr.addstr(5,1,"Votre objectif, gagner un maximum d'argent avant votre retraite.")
#stdscr.addstr(6,1,"Les '$' vous aportent 2 euros, les '£'vous en aportent 3 et enfin les '€' vous en apportent 5!")
#stdscr.addstr(7,1,"ATTENTION ! Les impôts peuvent vous tomber dessus à n'importe quel moment et vous faire ")
#stdscr.addstr(8,1,"perdre jusqu'à 30 pourcent de vos gains")
#stdscr.addstr(9,1,"Bon courage ! (appuyez sur 'd' pour commencer)")