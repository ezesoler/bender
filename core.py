# -*- coding: utf-8 -*-
import sys
import os
import globals
import mod_walle
import mod_optimus
import mod_r2d2
import mod_t800
from colorama import init, Fore, Back, Style
init()

def main():
	banner()
	arguments()

def clear():
	os.system('cls' if os.name == 'nt' else 'clear')


def banner():
	clear()
	print(Fore.GREEN + '''
  ___ ___ _  _ ___  ___ ___  
 | _ ) __| \| |   \| __| _ \ 
 | _ \ _|| .` | |) | _||   / 
 |___/___|_|\_|___/|___|_|_\ 
  by EzeSoler          v %s  
		''' % globals.VERSION['num'])

def arguments():
	try:
		mod = sys.argv[1:][0]
		if mod == "t800":
			clear()
			mod_t800.run()
		elif mod == "walle":
			clear()
			mod_walle.run()
		elif mod == "optimus":
			clear()
			mod_optimus.run()
		elif mod == "r2d2":
			clear()
			mod_r2d2.run()
	except:
		print(Fore.YELLOW +"Besa mi brillante trasero metálico:")
		print(Fore.YELLOW +"Módulos disponibles:\n* t800\n* walle\n* optimus\n* r2d2")
	
main()