from collections import deque
import random
import time


def readPDTFile(fileNumb):
    while(fileNumb<1 or fileNumb>12):
        fileNumb = int(input("This file does not exist, please enter another file number: "))
    f = open("Fichiers_txt/PDT-{fNumb}.txt".format(fNumb = fileNumb), "r")
    datalist = f.readlines()
    PDTRows = []
    for line in datalist:
        line = line.rstrip("\n")
        transport_fees = line.split(" ")
        PDTRows.append(transport_fees)
    return PDTRows


def changeToIntMatrice2D(Matrice2D):
    for i in range(len(Matrice2D)):
        for j in range(len(Matrice2D[i])):
            Matrice2D[i][j] = int(Matrice2D[i][j])
    return Matrice2D

def printCostMatrix(PDT):
    if(len(PDT[0]) == 2):
        for i in range(1, len(PDT)):
            for j in range(len(PDT[i])):
                if(PDT[i][j] < 10):
                    print("\033[0;97m|   ", end="")
                elif(PDT[i][j] >= 100 and PDT[i][j] < 1000):
                    print("\033[0;97m| ",end="")
                elif(PDT[i][j] >= 1000):
                    print("\033[0;97m|",end="")
                else:
                    print("\033[0;97m|  ", end="")
                if(j == len(PDT[i])-1 or i == len(PDT)-1):
                    print(f"\033[0;31m {PDT[i][j]}",end=" ")
                else:
                    print(f"\033[1;34m {PDT[i][j]}",end=" ")
            print("\033[0;97m|")
    else:
        for i in range(len(PDT)):
            for j in range(len(PDT[i])):
                if(PDT[i][j] < 10):
                    print("\033[0;97m|   ", end="")
                elif(PDT[i][j] >= 100 and PDT[i][j] < 1000):
                    print("\033[0;97m| ",end="")
                elif(PDT[i][j] >= 1000):
                    print("\033[0;97m|",end="")
                else:
                    print("\033[0;97m|  ", end="")
                if(j == len(PDT[i])-1 or i == len(PDT)-1):
                    print(f"\033[0;31m {PDT[i][j]}",end=" ")
                else:
                    print(f"\033[1;34m {PDT[i][j]}",end=" ")
            print("\033[0;97m|")


def getTotalOrders(PDT):
    totalOrders = []
    for i in range(len(PDT)):
        for j in range(len(PDT[i])):
            if(i == len(PDT)-1):
                totalOrders.append(PDT[i][j])
    return totalOrders

def getTotalProvisions(PDT):
    totalProvisions = []
    for i in range(len(PDT)):
        if(i == 0):
            continue
        if(i == len(PDT)-1):
            continue
        for j in range(len(PDT[i])):
            if(j == len(PDT[i])-1):
                totalProvisions.append(PDT[i][j])
    return totalProvisions

def fillMatriceWithRowsAndColums(matrice2D, rows, colums):
    newMatrice = [row[:] for row in matrice2D]  # Crée une copie de la matrice2D
    for i in range(len(newMatrice)+1):
        if (i == len(newMatrice)):
            newRow = []
            for k in range(len(rows)):
                newRow.append(rows[k])
            newMatrice.append(newRow)
            break
        for j in range(len(newMatrice[i])):
            if(j == len(newMatrice[i])-1):
                newMatrice[i].append(colums[i])
    return newMatrice


def FillByNordOuest(matrice2D):
    MatriceOfResult=[[0 for _ in range(matrice2D[0][1])] for _ in range(matrice2D[0][0])]
    order = getTotalOrders(matrice2D)
    provisions = getTotalProvisions(matrice2D)
    for i in range(matrice2D[0][0]):
        for j in range(matrice2D[0][1]):
            MatriceOfResult[i][j]=min(order[j],provisions[i])
            order[j]-=MatriceOfResult[i][j]
            provisions[i]-=MatriceOfResult[i][j]
    return MatriceOfResult


def GetCost(PDT): #Retourne les couts dans un tableau
    Cost = []
    for i in range(1,len(PDT)-1):
        

        for j in range(0,len(PDT[i])-1):
            
    
            Cost.append(PDT[i][j])
                
    return Cost

def GetMatriceCost(PDT):
    matriceCost = []
    for i in range(1,len(PDT)-1):
        Cost = []
        for j in range(0,len(PDT[i])-1):
            Cost.append(PDT[i][j])
        matriceCost.append(Cost)
    return matriceCost

def findMinInMatriceCost(PropIni, matriceCost, alreadyVisited):
    min = 1000000
    x = 0
    y = 0
    for i in range(len(matriceCost)):
        for j in range(len(matriceCost[i])):
            if(matriceCost[i][j] < min and is_in_list(matriceCost[i][j], alreadyVisited) == False and PropIni[i][j] == 0):
                min = matriceCost[i][j]
                x = i
                y = j
    return min, x, y


def CostTotal(matrice2D, Cost):  #Donne le cout totale de la proposition
    sum=0
    z=0
    #if len(matrice2D) * len(matrice2D[0]) != len(Cost):
    #    raise ValueError("Le nombre de coûts doit correspondre au nombre d'éléments dans la matrice.")
    
    for i in range(len(matrice2D)-1):
        for j in range(len(matrice2D[i])-1):
            sum = sum + Cost[z]*matrice2D[i][j]
            z=z+1
            
    return sum


def tranfo_matrice_into_adja(matrice, numberOfRows, numberOfColumns):
    #Initialisation de la matrice d'adjacence
    adja_matrice = []
    for i in range(numberOfRows + numberOfColumns):
        row_adja_matrice = []
        for j in range(numberOfRows + numberOfColumns):
            row_adja_matrice.append(0)
        adja_matrice.append(row_adja_matrice)

    #Remplissage de la matrice d'adjacence
    for i in range(len(adja_matrice)):
        for j in range(len(adja_matrice[i])):
            if(i >= numberOfRows):
                if(numberOfRows == numberOfColumns):
                    if (j < numberOfRows):
                        if(matrice[i - numberOfRows][j] != 0):
                            adja_matrice[j+numberOfColumns][i-numberOfRows] = matrice[i - numberOfRows][j]
                else:
                    if(j<numberOfRows):
                        if(matrice[j][i-numberOfRows] != 0):
                            adja_matrice[i][j] = matrice[j][i-numberOfRows]
            else:
                if(j >= numberOfRows):
                    if(matrice[i][j-numberOfRows] != 0):
                        adja_matrice[i][j] = matrice[i][j-numberOfRows]

    return adja_matrice

def transfo_adja_into_matrice(adja_matrice, matrice, numberOrRows):
    for i in range(0, numberOrRows):
        for j in range(numberOrRows, len(adja_matrice)):
            matrice[i][j-numberOrRows] = adja_matrice[i][j]
    return matrice


def calc_couts_potentiel(Matrice2D, newMatrice):
    print()
    a = 0
    j = 0
    listecouts_val = []
    listecouts = []
    for ligne in newMatrice[:-1]:
        i = 0
        for element in ligne[:-1]:
            if element != 0:
                listecouts.append("E" + "(" + str(j + 1) + ")" + " - " + "E" + "(" + chr(
                    97 + i) + ")" + " = ")  # permet d'obtenir nos équations de coûts potentiels dont le résultat est connu
                listecouts_val.append(Matrice2D[j + 1][i])  # permet d'obtenir les valeurs de nos équations de potentiel


            elif element == 0:
                listecouts.append("E" + "(" + str(j + 1) + ")" + " - " + "E" + "(" + chr(
                    97 + i) + ")" + " = ")  # permet d'obtenir nos équations de coûts potentiels dont le résultat est inconnu
                listecouts_val.append(None)  # ainsi nous initialisons leurs résultats a None
            i = i + 1
        j = j + 1

    potentiel_des_S_val = []  # Matrice contenant la valeur des potentiels des Sources
    potentiel_des_C_val = []  # Matrice contenant la valeur des potentiels des Cibles

    for ligne in newMatrice[:-1]:
        potentiel_des_S_val.append(
            None)  # On rempli la Matrice contenant les valeurs des potentiels des Sources en leur attribuant la valeur None
    for element in ligne[:-1]:
        potentiel_des_C_val.append(
            None)  # On rempli la Matrice contenant les valeurs des potentiels des Cibles en leur attribuant la valeur None
    potentiel_des_C_val[0] = 0  # On fixe le potentiel E2=0
    print("On fixe le potentiel E2=0 et nous connaissons les équations suivantes :")
    a = 0
    for element in listecouts:
        if listecouts_val[a] != None:
            print(element, "=", listecouts_val[a])
        a = a + 1

    a = 0
    i = 0
    j = 0
    N = len(potentiel_des_S_val) * len(
        potentiel_des_C_val)  # Permet de créer une condition d'arrêt grâce à l'initialisation de cpt en parallèle
    cpt = 0
    while (cpt != N):  # si cpt==N alors cela veut dire que tous nos coûts potentiels ont été calculés
        for elementa in potentiel_des_S_val:
            for elementb in potentiel_des_C_val:
                if elementa != None and elementb == None and listecouts_val[
                    a] != None:  # Si nous ne connaissons pas la valeur d'un potentiel cible
                    potentiel_des_C_val[i] = -(listecouts_val[
                                                   a] - elementa)  # alors nous essayons de le trouver en résolvant les équations
                    # dont nous connaissons le résultat et où la valeur d'un potentiel sortie est connue

                if elementa != None and elementb != None and listecouts_val[
                    a] == None:  # Permet de remplir les équations dont nous ne connaissions pas la solution
                    listecouts_val[a] = elementa - elementb

                elif elementa == None and elementb != None and listecouts_val[
                    a] != None:  # Si nous ne connaissons pas la valeur d'un potentiel sortie
                    potentiel_des_S_val[j] = listecouts_val[
                                                 a] + elementb  # alors nous essayons de le trouver en résolvant les équations
                a = a + 1  # dont nous connaissons le résultat et où la valeur d'un potentiel cible est connue
                i = i + 1
            i = 0
            j = j + 1
        j = 0
        for elementa in potentiel_des_S_val:  # permet de savoir si tous les coûts potentiels ont été calculés
            for elementb in potentiel_des_C_val:
                if elementa != None and elementb != None:
                    cpt = cpt + 1  # Si oui, alors cpt s'incrémentera jusqu'à la valeur N et notre boucle while s'arrêtera
        if cpt != N:
            cpt = 0  # Si non, alors cpt repart à 0 et notre boucle while tournera jusqu'à ce que tous les coûts potentiels soient calculés
            a = 0
    print()
    print("Après calcul les potentiels sont : ")
    i = 1
    for element in potentiel_des_S_val:  # permet d'afficher les potentiels une fois calculés
        print("E (", i, ") =", element)
        i = i + 1
    i = 1
    for element in potentiel_des_C_val:
        print("E (", chr(97 + i), ") =", element)
        i = i + 1

    Matricedescoutspotentiels = []
    Matricedescoutspotentielsligne = []
    for elementa in potentiel_des_S_val:  # permet de remplir la matrice des coûts potentiels
        for elementb in potentiel_des_C_val:
            Matricedescoutspotentielsligne.append(elementa - elementb)
        Matricedescoutspotentiels.append(Matricedescoutspotentielsligne)
        Matricedescoutspotentielsligne = []

    print()
    print("Ainsi la matrice des coûts potentiels est la suivante :")
    for element in Matricedescoutspotentiels:  # permet d'afficher la matrice des coûts potentiels
        print("| ", end="")
        for i in element:
            if i < 0 or i > 9:  # pour ne pas créer de décalage dans l'affichage de la matrice si un coût potentiel est négatif ou contient une dizaine
                print(i, end="")
                print("| ", end="")
            else:
                print(i, "| ", end="")
        print()
    return Matricedescoutspotentiels
        
def calc_couts_marginaux(Matricedescoutspotentiels, Matricedescouts):
    Matricedescoutsmarginaux = []
    Matricedescoutsmarginauxligne = []
    a=0
    b=0
    for element in Matricedescoutspotentiels: #permet de remplir la matrice des coûts marginaux
        for i in element:
            Matricedescoutsmarginauxligne.append(Matricedescouts[a]-element[b]) #permet de calculer les coûts marginaux et de les insérer dans un tableau temporaire
            a=a+1
            b=b+1
        b=0
        Matricedescoutsmarginaux.append(Matricedescoutsmarginauxligne) #permet d'insérer le tableau temporaire dans la matrice des coûts marginaux
        Matricedescoutsmarginauxligne = []                             #ainsi cela créer les lignes de cette matrice
    
    print()
    print("La matrice des coûts marginaux est la suivante :")
    for element in Matricedescoutsmarginaux: #permet d'afficher la matrice des coûts marginaux
        print("| ", end="")
        for i in element:
            if i <0 or i>9: #pour ne pas créer de décalage dans l'affichage de la matrice si un coût potentiel est négatif ou contient une dizaine
                print(i,end="")
                print("| ", end="")
            else :
                print(i,"| ", end="")
        print()    
    return Matricedescoutsmarginaux
    
def extract_provisions_order(matrice):
    if not matrice:
        return [], []

    n = len(matrice)  # Nombre de lignes pour les provisions
    m = len(matrice[0])  # Nombre de colonnes pour les commandes

    provisions = [ligne for ligne in matrice]
    orders = [[ligne[i] for ligne in matrice] for i in range(len(matrice[0]))]
    return provisions, orders



def printMatriceOfResult(matriceOfResult):
    for i in range(len(matriceOfResult)):
        for j in range(len(matriceOfResult[i])):
            cell_value = matriceOfResult[i][j]
            padding = max(4 - len(str(cell_value)), 0)
            print(f"\033[0;97m|{' ' * padding}{cell_value} ", end="")
        print("\033[0;97m|")

def CheckIfNumberInMatrice(matrice, nombre):
    for ligne in matrice:
        if nombre in ligne:
            return True
    return False

def GetRealSizeInList(liste):
    count = 0
    for element in liste:
        if element != 999:
            count += 1
    return count

    
# def GenerateMatrice2D(size, seed=None) :
#     if seed is not None:
#         random.seed(seed)

#     constraint_table=[[[0,0] for _ in range(size)] for _ in range(size)]
#     initial_prop=[]

#     for i in range(size):
#         for j in range(size):
#             constraint_table[i][j][0] = random.randint(1, 100)
    
#     temp = [[random.randint(1, 100) for _ in range(size)] for _ in range(size)]
#     p=[sum(row) for row in temp]
#     c=[sum(column) for column in zip(*temp)]

#     for i in range(size):
#         constraint_table[i].append(p[i])
#         constraint_table.append(c)
#     return constraint_table


import copy

def GenerateMatrice2D(size, seed=None):
    Matrice2D = []

    if seed is not None:
        random.seed(seed)
    
    constraint_table = [[0 for _ in range(size + 1)] for _ in range(size + 1)]
    
    for i in range(size):
        for j in range(size):
            constraint_table[i][j] = random.randint(1, 100)
    Matrice2D=constraint_table
    Matrice2D.insert(0,[size, size])

    temp = [[random.randint(1, 100) for _ in range(size)] for _ in range(size)]
    p = [sum(row) for row in temp]
    c = [sum(column) for column in zip(*temp)]
    for i in range(size):
        Matrice2D[i + 1][-1] = p[i]

    for i in range(size):
        Matrice2D[-1][i] = c[i]
        
    Matrice2D[-1].pop(-1)
    return Matrice2D




def FillByBallasHammer(matrice2D):

    Matriceclone = matrice2D.copy()
    MatriceOfResult = [[-999 for _ in range(matrice2D[0][1])] for _ in range(matrice2D[0][0])]
    order = getTotalOrders(Matriceclone)
    provisions = getTotalProvisions(Matriceclone)
    
    # Calcul des pénalités pour chaque ligne et chaque colonne
    penalitiesLine = [0 for _ in range(matrice2D[0][0])]
    penalitiesColumn = [0 for _ in range(matrice2D[0][1])]
    while(CheckIfNumberInMatrice(MatriceOfResult, -999)):
        # Calcul des pénalités pour chaque ligne
        for i in range(Matriceclone[0][0]):
            sorted_line = sorted(Matriceclone[i + 1][:-1])
            #print("sorted_line :", sorted_line)
            if(GetRealSizeInList(sorted_line) > 1):
                penalitiesLine[i] = sorted_line[1] - sorted_line[0]
            else:
                if(sorted_line[0] == 999):
                    penalitiesLine[i] = 0
                else:
                    penalitiesLine[i] = sorted_line[0]

        # Calcul des pénalités pour chaque colonne
        for j in range(Matriceclone[0][1]):
            column = [Matriceclone[i + 1][j] for i in range(matrice2D[0][0])]
            sorted_column = sorted(column)
            #print("sorted_column :", sorted_column)
            if(GetRealSizeInList(sorted_column) > 1): 
                penalitiesColumn[j] = sorted_column[1] - sorted_column[0]
            else:
                if(sorted_column[0] == 999):
                    penalitiesColumn[j] = 0
                else:
                    penalitiesColumn[j] = sorted_column[0]

        maxPenalitiesLine = max(penalitiesLine)
        maxPenalitiesColumn = max(penalitiesColumn)
        #FindAllIndexOfmaxPenalitiesLine
        indexsOfMaxPenalitiesLine=[]
        #indexsOfMaxPenalitiesLine.append(penalitiesLine.index(maxPenalitiesLine))
        for i in range(Matriceclone[0][0]):
            if(penalitiesLine[i] == maxPenalitiesLine):
                indexsOfMaxPenalitiesLine.append(i)
        #print("indexsOfMaxPenalitiesLine :", indexsOfMaxPenalitiesLine)
        #FindAllIndexOfmaxPenalitiesColumn
        indexsOfMaxPenalitiesColumn=[]
        indexsOfMaxPenalitiesColumn.append(penalitiesColumn.index(maxPenalitiesColumn))
        for i in range(matrice2D[0][1]):
            if(penalitiesColumn[i] == maxPenalitiesColumn and i not in indexsOfMaxPenalitiesColumn):
                indexsOfMaxPenalitiesColumn.append(i)
        #print("indexsOfMaxPenalitiesColumn :", indexsOfMaxPenalitiesColumn)
        #pour chaque index de maxPenalitiesLine on va chercher la plus petite valeur dans la ligne et on va regarder le min de son order et provision
        CaseToChange=None
        if (maxPenalitiesLine>maxPenalitiesColumn):
            for e in indexsOfMaxPenalitiesLine:
                #print("here : ",Matriceclone[e + 1][:-1])
                minValue = min(Matriceclone[e + 1][:-1])
                indexMinValue = Matriceclone[e + 1][:-1].index(minValue)
                if (CaseToChange==None):
                    CaseToChange=(e,indexMinValue)
                else :
                    if(min(order[indexMinValue],provisions[e])>min(order[CaseToChange[1]],provisions[CaseToChange[0]])):
                        CaseToChange=(e,indexMinValue)
            MatriceOfResult[CaseToChange[0]][CaseToChange[1]]=min(order[CaseToChange[1]],provisions[CaseToChange[0]])
            valueToChange=min(order[CaseToChange[1]],provisions[CaseToChange[0]])
            order[CaseToChange[1]]-=valueToChange
            provisions[CaseToChange[0]]-=valueToChange
            if(order[CaseToChange[1]]>provisions[CaseToChange[0]]):
               
               for i in range(matrice2D[0][1]):
                    Matriceclone[CaseToChange[0]+1][i]=999
                    if(i!=CaseToChange[1] and MatriceOfResult[CaseToChange[0]][i]==-999):
                        MatriceOfResult[CaseToChange[0]][i]=0
            else:

               for i in range(matrice2D[0][0]):
                    Matriceclone[i+1][CaseToChange[1]]=999
                    if(i!=CaseToChange[0] and MatriceOfResult[i][CaseToChange[1]]==-999):
                        MatriceOfResult[i][CaseToChange[1]]=0  
            #deleteLaLigne qui a était traité dans clone
            # for i in range(len(Matriceclone[CaseToChange[0]+1])):
                
            #     print("changed :",Matriceclone[CaseToChange[0]+1])
            #Matriceclone[0][0]-=1
        
        if (maxPenalitiesLine<maxPenalitiesColumn):
            for e in indexsOfMaxPenalitiesColumn:
                column_values = [row[e] for row in Matriceclone[1:-1]]
                minValue = min(column_values)
                indexMinValue = column_values.index(minValue)
                if (CaseToChange==None):
                    CaseToChange=(indexMinValue,e)
                else :
                    if(min(provisions[indexMinValue],order[e])>min(order[CaseToChange[1]],provisions[CaseToChange[0]])):
                        CaseToChange=(indexMinValue,e)
            MatriceOfResult[CaseToChange[0]][CaseToChange[1]]=min(order[CaseToChange[1]],provisions[CaseToChange[0]])
            valueToChange=min(order[CaseToChange[1]],provisions[CaseToChange[0]])
            order[CaseToChange[1]]-=valueToChange
            provisions[CaseToChange[0]]-=valueToChange
            if(order[CaseToChange[1]]>provisions[CaseToChange[0]]):
               
               for i in range(matrice2D[0][1]):
                    Matriceclone[CaseToChange[0]+1][i]=999
                    if(i!=CaseToChange[1] and MatriceOfResult[CaseToChange[0]][i]==-999):
                        MatriceOfResult[CaseToChange[0]][i]=0
            else:
            #    valueToChange=min(order[CaseToChange[1]],provisions[CaseToChange[0]])
            #    provisions[CaseToChange[0]]-=valueToChange
            #    order[CaseToChange[1]]-=valueToChange
               for i in range(matrice2D[0][0]):
                    Matriceclone[i+1][CaseToChange[1]]=999
                    if(i!=CaseToChange[0] and MatriceOfResult[i][CaseToChange[1]]==-999):
                        MatriceOfResult[i][CaseToChange[1]]=0        
            #deleteLaColonne qui a était traité dans clone
            # for i in range(len(Matriceclone[1:])):
                
            #     print("changed :",Matriceclone[i])
            #Matriceclone[0][1]-=1
        
        if(maxPenalitiesLine==maxPenalitiesColumn):
            BetterValueForLine=None
            BetterValueForColumn=None
            for e in indexsOfMaxPenalitiesLine:
                minValueLine = min(Matriceclone[e + 1][:-1])
                indexminValueLine = Matriceclone[e + 1][:-1].index(minValueLine)
                if (BetterValueForLine==None):
                    BetterValueForLine=(e,indexminValueLine)
                else :
                        if(min(order[indexminValueLine],provisions[e])>min(order[BetterValueForLine[1]],provisions[BetterValueForLine[0]])):
                            BetterValueForLine=(e,indexminValueLine)
            for e in indexsOfMaxPenalitiesColumn:
                column_values = [row[e] for row in Matriceclone[1:-1]]
                minValueColumn = min(column_values)
                indexminValueColumn = column_values.index(minValueColumn)
                if (BetterValueForColumn==None):
                    BetterValueForColumn=(indexminValueColumn,e)
                else :
                        if(min(order[e],provisions[indexminValueColumn])>min(order[BetterValueForColumn[1]],provisions[BetterValueForColumn[0]])):
                            BetterValueForColumn=(indexminValueColumn,e)
            if(min(order[BetterValueForLine[1]],provisions[BetterValueForLine[0]])>min(order[BetterValueForColumn[1]],provisions[BetterValueForColumn[0]])):
                CaseToChange=BetterValueForLine
            else:
                CaseToChange=BetterValueForColumn
            MatriceOfResult[CaseToChange[0]][CaseToChange[1]]=min(order[CaseToChange[1]],provisions[CaseToChange[0]])
            if(order[CaseToChange[1]]>provisions[CaseToChange[0]]):
                valueToChange=min(order[CaseToChange[1]],provisions[CaseToChange[0]])
                provisions[CaseToChange[0]]-=valueToChange
                order[CaseToChange[1]]-=valueToChange
                for i in range(matrice2D[0][1]):
                    Matriceclone[CaseToChange[0]+1][i]=999
                    if(i!=CaseToChange[1] and MatriceOfResult[CaseToChange[0]][i]==-999):
                        MatriceOfResult[CaseToChange[0]][i]=0
            else:
                valueToChange=min(order[CaseToChange[1]],provisions[CaseToChange[0]])
                order[CaseToChange[1]]-=valueToChange
                provisions[CaseToChange[0]]-=valueToChange
                for i in range(matrice2D[0][0]):
                    Matriceclone[i+1][CaseToChange[1]]=999
                    if(i!=CaseToChange[0] and MatriceOfResult[i][CaseToChange[1]]==-999):
                        MatriceOfResult[i][CaseToChange[1]]=0
                
                



        #else:
        #print("Matriceclone",Matriceclone)
        #time.sleep(5)
    return MatriceOfResult
    #You have to checkWithTheindexOfLineAndColumnAndfindTheValueYouCanMakeTheCaseToChange

def find_start(matrix, NodeVisited=None):
    n = len(matrix)

    for i in range(n):
        for j in range(n):
            if NodeVisited == None:
                if matrix[i][j] != 0:
                    return i
            else:
                isInNodeVisited=False
                for e in NodeVisited:
                    if(i in e):
                        isInNodeVisited=True
                if matrix[i][j] != 0 and isInNodeVisited==False :
                    return i
                
    return -1  # Si aucun sommet n'est trouvé, retourne -1


def isConnexe(matrix):
    NodeVisited=[]
    NodeVisited.append(BFS(matrix))
    print("NodeVisited",NodeVisited)
    if(len(NodeVisited[0])==len(matrix)):
        return True
    AllPartOfGraph=NodeVisited
    RealSizeOfGraph=len(NodeVisited[0])
    while(RealSizeOfGraph<len(matrix)):
        AllPartOfGraph.append(BFS(matrix,NodeVisited))
        RealSizeOfGraph=0
        for i in range(len(AllPartOfGraph)):
            RealSizeOfGraph+=len(AllPartOfGraph[i])
    print("AllPartOfGraph",AllPartOfGraph)
    return AllPartOfGraph    

def popParent(queue):
    if len(queue) == 0:
        return None
    return queue.popleft()

        #matrix = matrix adj



def getConnexeSimple(adjmatrix,numberOfRow,PDT, PropIni, alreadyVisited):
    AllPartOfGraph=isConnexe(adjmatrix)
    matrice_couts = GetMatriceCost(PDT)
    min, x, y = findMinInMatriceCost(PropIni,matrice_couts, alreadyVisited)
    if(len(AllPartOfGraph)==1):
        print("déjà connexe !!")
        return adjmatrix
    find = False
    while(find == False):
        for i in range(numberOfRow):
            for j in range(numberOfRow,len(adjmatrix)):
                if(adjmatrix[i][j] == 0 and i == x and j-numberOfRow == y):
                    alreadyVisited.append(min)
                    adjmatrix[i][j] = 1
                    is_cyclic, point = returnDetectCycle(adjmatrix)
                    if(is_cyclic == True):
                        adjmatrix[i][j] = 0
                        min, x, y = findMinInMatriceCost(PropIni ,matrice_couts, alreadyVisited)
                    else:
                        adjmatrix[j][i] = 1
                        return adjmatrix
    return adjmatrix

def getConnexeComp(adjmatrix,numberOfRow,PDT, PropInit):
    AllPartOfGraph = isConnexe(adjmatrix)
    alreadyVisited = []
    if(len(AllPartOfGraph) >= 2):
        for i in range(len(AllPartOfGraph)):
            if(isConnexe(adjmatrix) == True):
                return adjmatrix
            adjmatrix = getConnexeSimple(adjmatrix, numberOfRow, PDT, PropInit, alreadyVisited)
    else:
        adjmatrix = getConnexeSimple(adjmatrix, numberOfRow, PDT, PropInit, alreadyVisited)
    return adjmatrix
            


def BFS(adjacenceMatrix, AlreadyVisited=None):
    NodeVisited=[]
    if AlreadyVisited is None:
        startpoint=find_start(adjacenceMatrix)
    else:
        startpoint=find_start(adjacenceMatrix,AlreadyVisited)
    currentNode=startpoint
    queueToDo=[]
    queueToDo.append(currentNode)
    NodeVisited.append(currentNode)
    while(queueToDo):
        currentNode=queueToDo.pop(0)
        for i in range(len(adjacenceMatrix[currentNode])):
            if(adjacenceMatrix[currentNode][i]!=0 and i not in NodeVisited):
                queueToDo.append(i)
                NodeVisited.append(i)  
    return NodeVisited

def returnBFSCyclic(adja_matrice, start):
    visited = []
    for i in range(len(adja_matrice)):
        visited.append(False)
    queue = deque()
    parents = deque()

    queue.append(start)
    visited[start] = True

    while queue:
        current_node = queue.popleft()
        node_parent = popParent(parents)
        for i in range(len(adja_matrice[current_node])):
            if(adja_matrice[current_node][i] != 0 and visited[i] == True and i != node_parent):
                return True, i, node_parent
            if(adja_matrice[current_node][i] != 0 and visited[i] == False and i != node_parent):
                queue.append(i)
                parents.append(current_node)
                visited[i] = True

    return False, None, None

def returnDetectCycle(adja_matrice):
    point = set()
    for i in range(len(adja_matrice)):
        iscyclic, final, parent = returnBFSCyclic(adja_matrice, i)
        point.add(final)
        point.add(parent)
    return iscyclic, point

def is_in_list(value, table):
    find = False
    for i in range(len(table)):
        if(table[i] == value):
            find = True
    return find

def findTuples(points, adja_matrice, NumberOfRows):
    listOfTuples = []
    for i in range(len(points)):
        if(points[i] < NumberOfRows):
            for j in range(len(adja_matrice[0])):
                if(adja_matrice[points[i]][j] != 0 and is_in_list(j, points)):
                    row = [points[i], j]
                    listOfTuples.append(row)
    return listOfTuples

def isOpti(matriceMarg):
    min = 10000000
    x = 0
    y = 0
    Opti = True
    for i in range(len(matriceMarg)):
        for j in range(len(matriceMarg[i])):
            if(matriceMarg[i][j] < 0 and matriceMarg[i][j] < min):
                min = matriceMarg[i][j]
                x = i
                y = j
                Opti = False
    return Opti, x, y


