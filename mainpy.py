from Functions import *

decided = False

while(decided == False):
    #choix entre fichier ou generer matrice
    choice = int(input("Choisir entre générer une matrice aléatoire ou charger un fichier (1 pour fichier ou 0 pour générer une matrice aléatoire) : "))
    while(choice != 1 and choice != 0):
        choice = int(input("Choisir entre générer une matrice aléatoire ou charger un fichier (1 pour fichier ou 0 pour générer une matrice aléatoire) : "))
    
    if(choice == 1):
        FileNumber = int(input("Enter the number of the file you want to test : "))
        PDT = changeToIntMatrice2D(readPDTFile(FileNumber))
    if (choice ==0):
        size=int(input("Entrez la taille de la matrice : "))
        while(size<1 or size>10000):
            size = int(input("La taille de la matrice doit être comprise entre 1 et 10000 : "))
        PDT = GenerateMatrice2D(size)
    #extractions des données
   
    numberOfRows = PDT[0][0]
    numberOfColumns = PDT[0][1]
    total_orders = getTotalOrders(PDT)
    total_provisions = getTotalProvisions(PDT)
    cost = GetCost(PDT)

    #affichage de la matrice des coûts
    print("Voici la matrice des coûts : ")
    printCostMatrix(PDT)
    print()
    ##Sum = CostTotal(PDT, cost)
    ##print("Le cout totale de la proposition initiale est", Sum)

    #choix transport initial
    choice = int(input("Choisir le transport initial (1 pour Nord-Ouest ou 0 pour Ballas-Hammer) : "))
    while(choice != 1 and choice != 0):
        choice = int(input("(1 pour Nord-Ouest ou 0 pour Ballas-Hammer) : "))
    if(choice == 1):
        #Nord-Ouest
        NO=FillByNordOuest(PDT)
        NO_Full = fillMatriceWithRowsAndColums(NO, total_orders, total_provisions)
        print("Proposition initiale (Après NO) : ")
        # while() # a definir
        printCostMatrix(NO_Full)
        Sum = CostTotal(NO_Full, cost)
        print("Le coût total de cette proposition de transport est : ", Sum)
        print("test de la matrice d'adjacence :")
        printCostMatrix(tranfo_matrice_into_adja(NO, numberOfRows, numberOfColumns))
        
        print("Le graphe est-il non dégénéré?")
        matriceadj=tranfo_matrice_into_adja(NO, numberOfRows, numberOfColumns)
        is_cyclic,point=returnDetectCycle(matriceadj)
        if(isConnexe(matriceadj)==True and is_cyclic== False):
            print("Oui")
        if(isConnexe(matriceadj)==True and is_cyclic== True):
            print("cyclique")
            list_point=list(point)
            print("Les sommets qui forment le cycle sont: ",list_point)
            list_arretes=findTuples(list_point,matriceadj,numberOfRows)
            print("Les arretes qui forment le cycle sont: ",list_arretes)
        if(isConnexe(matriceadj)!=True and is_cyclic== False):
            print("Non connexe")
            matriceadj=getConnexeComp(matriceadj,numberOfRows,PDT, NO)
        if(isConnexe(matriceadj)!=True and is_cyclic== True):
            print("Non connexe et cyclique")
            matriceadj=getConnexeComp(matriceadj,numberOfRows,PDT, NO)
            list_point=list(point)
            print("Les sommets qui forment le cycle sont: ",list_point)
            list_arretes=findTuples(list_point,matriceadj,numberOfRows)
            print("Les arretes qui forment le cycle sont: ",list_arretes)

        NO = transfo_adja_into_matrice(matriceadj, NO, numberOfRows)
        NO_Full = fillMatriceWithRowsAndColums(NO, total_orders, total_provisions)
        printCostMatrix(NO_Full)

        #On rentre dans le marche pied
        couts_potentiel = calc_couts_potentiel(PDT, NO_Full)
        couts_marginaux = calc_couts_marginaux(couts_potentiel, cost)
        Opti, x, y = isOpti(couts_marginaux)
        while(Opti == False):
            print("La proposition n'est pas optimale.")
            print("L'arête à ajouter est la suivante : ", (x,y))
            NO[x][y] = 1
            matriceadj = tranfo_matrice_into_adja(NO, numberOfRows, numberOfColumns)
            is_cyclic, point = returnDetectCycle(matriceadj)
            list_point = list(point)
            print("Les sommets qui forment le cycle sont: ", list_point)
            list_arretes = findTuples(list_point, matriceadj, numberOfRows)


    elif(choice == 0):
        #Ballas-Hammer
        PDT_temp = [[val for val in ligne] for ligne in PDT]
        BA=FillByBallasHammer(PDT_temp)
        BA_Full = fillMatriceWithRowsAndColums(BA, total_orders, total_provisions)
        print("Proposition initiale (Après BA) : ")
        printCostMatrix(BA_Full)
        Sum = CostTotal(BA_Full, cost)
        print("Le coût total de cette proposition de transport est : ", Sum)
        print("test de la matrice d'adjacence :")
        printCostMatrix(tranfo_matrice_into_adja(BA, numberOfRows, numberOfColumns))
        print("Le graphe est-il non dégénéré?")
        matriceadj=tranfo_matrice_into_adja(BA, numberOfRows, numberOfColumns)
        is_cyclic,point=returnDetectCycle(matriceadj)

        if(isConnexe(matriceadj)==True and is_cyclic== False):
            print("Oui")

        if(isConnexe(matriceadj)==True and is_cyclic== True):
            print("cyclique")
            list_point=list(point)
            print("Les sommets qui forment le cycle sont: ",list_point)
            list_arretes=findTuples(list_point,matriceadj,numberOfRows)
            print("Les arretes qui forment le cycle sont: ",list_arretes)
        if(isConnexe(matriceadj)!=True and is_cyclic== False):
            print("Non connexe")
            matriceadj=getConnexeComp(matriceadj,numberOfRows,PDT, BA)
        if(isConnexe(matriceadj)!=True and is_cyclic== True):
            print("Non connexe et cyclique")
            matriceadj=getConnexeComp(matriceadj,numberOfRows,PDT, BA)
            list_point=list(point)
            print("Les sommets qui forment le cycle sont: ",list_point)
            list_arretes=findTuples(list_point,matriceadj,numberOfRows)
            print("Les arretes qui forment le cycle sont: ",list_arretes)

        BA = transfo_adja_into_matrice(matriceadj, BA, numberOfRows)
        BA_Full = fillMatriceWithRowsAndColums(BA, total_orders, total_provisions)
        printCostMatrix(BA_Full)

        #On rentre dans le marche pied
        couts_potentiel = calc_couts_potentiel(PDT, BA_Full)
        couts_marginaux = calc_couts_marginaux(couts_potentiel, cost)



    #Permet à l'utilisateur de tester plusieurs fichiers
    choice = int(input("Continue ? (1 for Yes and 0 for No) : "))
    while(choice != 0 and choice != 1):
        choice = int(input("This is the wrong choice (1 for Yes and 0 for No) : "))
    if(choice == 0):
        decided = True
    