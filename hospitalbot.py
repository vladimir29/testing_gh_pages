#!/usr/bin/python
# -*- coding: utf-8 -*-

from TreeModule.Tree import *
from boto3 import  client
import boto3
import StringIO
from contextlib import closing
import serial
import os.path
import sys
import json
import StringIO
from difflib import SequenceMatcher

input_string = ""

buff = ""

root = Node(None, [], "La ce secție vreți să mergeți?")
# cantunderstand = Node(root, [], "Unde mai exact aveți probleme?")
dontknow = Node(root, [], "Ce problemă aveți?")
oftalmologie = Node(root, [], "Secția de oftalmologie se află la parter, corp A, hol 3, a treia ușă pe stânga")
cardiologie = Node(root, [], "Secția de cardiologie se află la parter, corp A, hol 3, a doua ușă pe stânga")
dermatologie = Node(root, [], "Secția de dermatologie se află la parter, corp A, hol 1, prima ușă pe dreapta")
gastroenterologie = Node(root, [], "Secția de gastroenterologie se află la parter, corp A, hol 1, prima ușa pe dreapta")
ortopedie = Node(root, [], "Secția de ortopedie se află la parter, corp A, hol 2, prima ușă pe stânga")
repeat = Node(root, [], "Unde mai exact aveți probleme?")
repeat_son = Node(repeat, [], "")
dontknow_son = Node(dontknow, [], "")

oftalmologie2 = Node(repeat, [], "Secția de oftalmologie se află la parter, corp A, hol 3, a treia ușă pe stânga. Să adaug %s ca afecțiune?" % buff)
cardiologie2 = Node(repeat, [], "Secția de cardiologie se află la parter, corp A, hol 3, a doua usă pe stânga. Să adaug %s ca afecțiune?" % buff)
dermatologie2 = Node(repeat, [], "Secția de dermatologie se află la parter, corp A, hol 1, prima ușă pe dreapta. Să adaug %s ca afecțiune?" % buff)
gastroenterologie2 = Node(repeat, [], "Secția de gastroenterologie se află la parter, corp A, hol 1, prima ușa pe dreapta. Să adaug %s ca afecțiune?" % buff)
ortopedie2 = Node(repeat, [], "Secția de ortopedie se află la parter, corp A, hol 2, prima ușă pe stânga. Să adaug %s ca afecțiune?" % buff)

eye_problems = ["oftalmo", "oftalmologie", "ma dor ochii", "la ochi", "ochi"]
heart_problems = ["cardio", "cardiologie", "inima", "la inima", "ma doare inima"]
skin_problems = ["dermato", "dermatologie", "am mancarimi", "am o eruptie", "la piele", "piele", "cosuri", "varicela", "bube", "alunite"]
digestive_problems = ["gastro", "gastroentero", "gastroenterologie", "ma doare stomacul", "la stomac", "ma doare burta", "stomacul", "stomac",
                      "burta"]
limbs_problems = ["ma doare in cot", "ortopedie", "la brat", "la cot", "la umar", "la mana", "la picior",
                  "am o luxatie", "am o fractura", "mi-am luxat mana", "mi-am luxat un deget",
                  "mi-am luxat degetul", "mi-am rupt mana", "mi-am rupt un deget", "fractura", "luxatie",
                  "mana", "picior", "piciorul", "umar", "umarul", "cot", "cotul"]

polly = client("polly", 'us-east-1')
ser = serial.Serial('/dev/ttyUSB0', 9600)
#input_string = ser.readline().strip('\r\n').strip()
#input_string = ser.readline().strip('\r\n').strip()

def found(string, list):
        for element in list:
                if len(element) > len(string):
                        if string in element:
                                return True
                else:
                        if element in string:
                                return True

        return False

def get_input():
        #ser = serial.Serial('/dev/ttyUSB0', 9600)
        mesaj = ser.readline().strip('\r\n').strip()

        return mesaj

def play_response(node):
        to_polly = node.value
	response = polly.synthesize_speech(
                Text= to_polly,
                OutputFormat="mp3",
                VoiceId="Carmen")

	if "AudioStream" in response:
                with closing(response["AudioStream"]) as stream:
                    data = stream.read()
                    nume = "pollytest.mp3"
                    fo = open(nume, "w+")
                    fo.write( data )
                    fo.close()
        
	import webbrowser
        webbrowser.open("pollytest.mp3")

def tree_recursion(node):
	#print node.value
	play_response(node)
        
	if node.isLeaf() == 0:
		#input_string = raw_input("").lower()
                input_string = ser.readline().strip('\r\n').strip()
		input_string = input_string.replace('ă', 'a')
		input_string = input_string.replace('â', 'a')
		input_string = input_string.replace('ț', 't')
		input_string = input_string.replace('ș', 's')
		input_string = input_string.replace('î', 'i')
                print input_string
                
		if found(input_string, eye_problems):
			tree_recursion(oftalmologie)
		elif found(input_string, heart_problems):
			tree_recursion(cardiologie)
		elif found(input_string, skin_problems):
			tree_recursion(dermatologie)
		elif found(input_string, digestive_problems):
			tree_recursion(gastroenterologie)
		elif found(input_string, limbs_problems):
			tree_recursion(ortopedie)
		elif input_string == "nu stiu":
			tree_recursion(dontknow)
		else:
			tree_recursion(repeat)

tree_recursion(root)
