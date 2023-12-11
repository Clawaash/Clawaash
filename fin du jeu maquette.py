import time
import curses
stdscr = curses.initscr()
curses.noecho()
#la fin: gagner ou perdre
start_time = datetime.datetime.now() #ne pas oublier de mettre import time en haut 
jeuencours=True
while jeuencours:
    if score==30 or (perso['x'],perso['y'])==(trou['x'],trou['y']):
        jeuencours=False
    elif (perso['x'],perso['y'])==(trou['x'],trou['y']): #trou pas encore écrit mais ca compare si le personnage est sur la meme postition que le trou cad dans le trou 
           
        
    c = stdscr.getkey()  # pour recuperer les d´eplacements
    stdscr.erase() # on efface l'ecran
    update_p(c, p, m)      #on update le déplacement d'après 
    display_map_and_char(m, p, d) # on affiche la carte et la joueur
    stdscr.refresh()      #on met a jour l'écran? 

#une fois qu'on est sortis de la boucle, on va afficher si il a gagné et le temps mis, ou si il a perdu et le score    
   
if score==30:
    end_time = datetime.datetime.now()
    time_diff = (end_time - start_time)
    execution_time = time_diff.total_seconds() *1000 #ce qui le met en seconde si je fais pas d'erreurs
    #apres là je calibrerai quand on aura fini pour avoir un truc un peu cohérant mais en gros faire une conversion pour avoir un nombre d'année entre 20 ans et 80 ans 
    stdscr.addstr(0,0,"FELICITATION! Vous avez gagné assez d'argent pour prendre votre retraite à %f ans")
    #je chercherai dans mon cours de L1 demain comment marche les %f je m'en souviens plus     
else:#donc le cas où on a perdu 
    (perso['x'],perso['y'])==(trou['x'],trou['y']):
    stdscr.addstr(0,0,"DOMMAGE! Vous avez perdu, votre score est de %f"%f)