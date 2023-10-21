"""
Programme de conjugaison des verbes du 1er et 2e groupe, 
à l'imparfait, au futur et au présent

Pris en compte:
 - verbes pronominaux
 - Verbe dont les pronoms prennent des apostrophes

Exceptions prises en compte:

-cer -ger
-eter -eler -e<consonne>er
-uyer -oyer
"""

def verif_verbe(verbe: str, groupe: int) -> bool:
    """ 
    Vérifie si le verbe est correct en fonction du groupe rentré
    """
    ## Verfication de terminaisons en fonction du groupe
    ok_verbe = (groupe == 1 and verbe.strip().endswith('er') or groupe == 2 and verbe.strip().endswith('ir'))
    return len(verbe) >= 4 and ok_verbe

def isvoyelle(lettre: str) -> bool:
    """
    Retourne si la valeur est dans les lettres où il jaut mettre j'
    """
    return lettre.lower() in 'aeiouyeèêéiïaäaâôûùh'


def get_terms(num_temps, groupe=1, prono=None, is_appostrophe=False) -> list:
    """
    Retourne les terminaisons et les pronoms en fonction du temps, du groupe et de si un verbe est pronominal
    """
    ## Pronoms lorsqu'on a un verbe pronominal
    list_pronos = ['m', 't', 's', 'nous', 'vous', 's']

    all_terms = [[
        ## Present
        # 1er Groupe
        [['je', 'e'], ['tu', 'es'], ['il', 'e'], ['nous', 'ons'], ['vous', 'ez'], ['ils', 'ent']],
        # 2e Groupe
        [['je', 'is'], ['tu', 'is'], ['il', 'it'], ['nous', 'issons'], ['vous', 'issez'], ['ils', 'issent']]],
        
        ## Imparfait
        # 1er Groupe
        [[['je', 'ais'], ['tu', 'ais'], ['il', 'ait'], ['nous', 'ions'], ['vous', 'iez'], ['ils', 'aient']],
        # 2e Groupe
        [['je', 'issais'], ['tu', 'issais'], ['il', 'issait'], ['nous', 'issions'], ['vous', 'issiez'], ['ils', 'issaient']]], 
        
        ## Futur
        # 1er Groupe
        [[['je', 'erai'], ['tu', 'eras'], ['il', 'era'], ['nous', 'erons'], ['vous', 'erez'], ['ils', 'eront']],
        # 2e Groupe
        [['je', 'irai'], ['tu', 'iras'], ['il', 'ira'], ['nous', 'irons'], ['vous', 'irez'], ['ils', 'iront']]]   
    ]
    
    ## Choisir le bon groupe de terminaisons
    list_terms = all_terms[num_temps][groupe - 1]
    
    ## Rajouter un pronom si c'est un verbe pronominal
    if prono is not None:
        for index in range(len(list_terms)):
            if len(list_pronos[index]) > 1:
                list_terms[index][0] = list_terms[index][0] + ' ' + list_pronos[index]
            else:
                list_terms[index][0] = list_terms[index][0] + ' ' + list_pronos[index] + prono[1:]
    
    ## Rajouter l'appostrophe si besoin    
    elif is_appostrophe:
        list_terms[0][0] = list_terms[0][0][:-1] + "'"
    
    return list_terms
    

def conjuger(verbe, temps, num_temps, grp):
    """
    Affiche les conjuguaisons d'un verbe en fonction du temps et du groupe
    """
    # Exceptions avec les verbes en -eler et -eter
    exceptions_eler = ['acheter','racheter','bégueter','corseter', 'crocheter','fileter','fureter','haleter','agneler','celer','déceler','receler','ciseler','démanteler','écarteler','encasteler','geler','dégeler','congeler','surgeler','marteler','modeler','peler']
    
    # Obtenir les terminaisons
    radical = verbe[:-2]
    if verbe.startswith('se '):
        # Verbe pronominal sans apostrophe
        terms = get_terms(num_temps, groupe=grp, prono='se', is_appostrophe=isvoyelle(verbe[0]))
        radical = radical[3:]
    elif verbe.startswith('s\''):
        # Verbe pronominal avec apostrophe
        terms = get_terms(num_temps, groupe=grp, prono='s\'', is_appostrophe=isvoyelle(verbe[0]))
        radical = radical[2:]
    else:
        # Verbe non pronominal
        terms = get_terms(num_temps, groupe=grp, prono=None, is_appostrophe=isvoyelle(verbe[0]))
    
    ## Exceptions en cer/ger    
    # ajouts = (lettre a rajouter au radical à certaines personnes, sinon)
    ajouts = ('', '')
    if verbe.endswith('cer'):
        # On change le c du radical en ç 
        radical = radical[:-1]
        ajouts = ('ç', 'c')

    elif verbe.endswith('ger'):
        # On ajoute un e au radical 
        ajouts = ('e', '')
             
    ## On applique les changement de radical 
    for index, (p, t) in enumerate(terms):
        # Seulement à nous au présent et à toutes les personnes sauf nous et vous à l'imparfait
        if ((index == 3 and temps == 'present') or (temps == 'imparfait' and index not in [3, 4])):
            # Si les condtitions de temps et de personnes sont respectées, on change le radical<
            terms[index][1] = ajouts[0] + t
        else:
            terms[index][1] = ajouts[1] + t

    # Cas normal pour les verbes en et eter et eler en e<consonne>er
    # On Change le radical en fonction de l'exception
    # ajouts = (lettre a rajouter au radical à certaines personnes, sinon)
    ajouts = ('', '')
    if verbe[-4] in ['e', 'è', 'é']:
        radical = radical[:-2]
        if verbe[-3] in ['l', 't']:
            # Si le verbe est en eter ou en eler
            if verbe in exceptions_eler:
                # Si le verbe n'est pas dans les exceptions
                # on remplace le e par è
                ajouts = ('è' + verbe[-3], 'e' + verbe[-3])
            else:
                # on double la consonne
                ajouts = ('e' + 2 * verbe[-3], 'e' + verbe[-3])
        else:
            # on remplace le e par è
            ajouts = ('è' + verbe[-3], 'e' + verbe[-3])
            
    ## On applique les changement de radical 
    for index, (p, t) in enumerate(terms):
        # Seulement à toutes les personnes sauf nous et vous au présent et à toutes les personnes du futur
        if (temps == 'present' and index not in [3, 4]) or temps == 'futur':
            # Si les condtitions de temps et de personnes sont respectées, on change le radical
            terms[index][1] = ajouts[0] + t
        else:
            terms[index][1] = ajouts[1] + t
   
    
    # exceptions en oyer/uyer
    if (verbe.endswith('oyer') or verbe.endswith('uyer')) and temps in ['present', 'futur']:
        radical = radical[:-1] + 'i'

    # Rendu Final
    print('###################################')
    for (pronom, terminaison) in terms:
        resulist_terms = pronom + ' ' + radical + terminaison
        print(resulist_terms.replace("' ", "'"))


def main():
    """
    Menu de choix
    ##### Pour rendre l'affichage plus clair dans la console.
    """
    print('############################################################################################################################################')
    print('############################################################################################################################################')
    groupe = int(input('Quel est le groupe de votre verbe ? (1 ou 2)\n'))
    num_temps = int(input("A quel temps voulez vous conjuguer votre verbe ?\n 1: Présent \n 2: Imparfait \n 3: Futur \n"))
    temps = ['present', 'imparfait', 'futur'][num_temps - 1]
    verbe = input("Quel est votre verbe ? \n")
    print('')
    if verif_verbe(verbe, groupe):
        try:
            conjuger(verbe, temps, num_temps - 1, groupe)
        except Exception as erreur:
            print('Oups, une erreur est survenue : \n', erreur)
    else:
        print("Le verbe n'est pas conforme !")

if __name__ == '__main__':
    print('############################################################################################################################################')
    print('Ctrl + C pour quitter')
    while True:
        ## Pour boucler sur l'affichage du menu de choix
        main()
