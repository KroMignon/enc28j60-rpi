#! /usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 13 janv. 2013

@author: FMousset
'''

import os

pcsp_cmd = '"c:\Program Files (x86)\PuTTY\pscp.exe" -pw engele %s pi@192.168.2.102:/home/pi/enc28j60'
nfo_file = ".update_nfo"

# Set these to your own details.
#myssh = Connection('192.168.2.102', username='pi', password='engele')
#myssh.chdir('ec28j60')

files = []
excludes = ['pysftp.py', 'spidev.py']

# recherche du dossier du script
dossier = os.path.dirname(os.path.abspath(__file__))
os.chdir(dossier)

# Ajout du nom du script dans la liste des fichiers ignor�s
excludes.append(os.path.basename(__file__))

# Lecture de la dernière mise à jour du Raspberry PI
timestmp = None
if os.path.exists(nfo_file):
    timestmp = os.path.getmtime(nfo_file)

# recherche des fichiers Python
for filename in os.listdir(dossier):
    if filename[-3:] == '.py' and not(filename in excludes):
        if (timestmp==None or timestmp < os.path.getmtime(filename)):
            files.append(filename)

# Transfert vers le Raspberry PI
if len(files) > 0:
    ma_command = pcsp_cmd %  " ".join(files)
    os.system(ma_command)

    # MAJ du fichier d'info de MAJ
    fichier = open(nfo_file, "w")
    fichier.close()
