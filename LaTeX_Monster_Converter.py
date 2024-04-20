import progress_bar as progress_bar
import LaTeX as LX

import requests
import math
from deep_translator import GoogleTranslator

###########################################################################################################################################################################################
    # written by AMG, it makes API requests to open5e and converts the response into a text file, the content of this file can be direcly pasted into a LaTeX file
###########################################################################################################################################################################################
    # HOW TO USE: 
    # change monster name to an existing 5E monster (check open5e)
    # the api url should stay the same, if the API ever has a major update this will probably stop working (18.04.2024)
    # to get all the source/target language codes just make a faulty translator call, it will output all codes in form of an error message
    # the progress bar is fairly manual but also not really required, if the amount of 'progress()' calls is changed the init size needs to be changed as well
###########################################################################################################################################################################################
    # Setttings:
monster_name = "Shadow Elf Spellcaster Drider"
api_url = "https://api.open5e.com/monsters/?name="
source_language = 'en'
target_language = 'de'
progress_bar.init(29)
###########################################################################################################################################################################################
    # Setup:
#remove spaces and create full api url
monster_name = monster_name.replace(' ', '+')
api_url = api_url + monster_name

#get api response and parse the json
response = requests.get(api_url)
api_answer = response.json()

#set up translator, the error when using faulty codes will list all countries that are supported (including their 2 letter code)
translator = GoogleTranslator(source=source_language, target=target_language)

#the answer will include monsters from multile sources, the first one will usually be the official 5E version
first_entry = api_answer['results'][0]

# this does not really take the type into consideration but with 'None' it does not matter, and is the only one we really need to check
def has_content(text):
    if text == None or text == 'null' or text == '': 
        return False
    else:
        return True
###########################################################################################################################################################################################

# file generation
file = open(monster_name + "_LaTeX.txt", "w+")

#writing to file:
file.write(LX.thick_line + LX.lNew_line + LX.new_line + LX.new_line) #seperation to text before

content = first_entry['name']
if has_content(content):
    file.write(LX.bold_LARGE(content) + LX.new_line) # 'name'/name of the monster
progress_bar.progress()

#size, type, subtype, group and alignment go into one line
content = first_entry['size']
if has_content(content):
    file.write(translator.translate(content)) # 'size'/battlemap-size of the monster
progress_bar.progress()

content = first_entry['type']
if has_content(content):
    file.write(" " + translator.translate(content)) # 'type'/type of the monster (undead, etc.)
progress_bar.progress()

content = first_entry['subtype']
if has_content(content):
    file.write("," + translator.translate(content)) # 'subtype'/subtype of the monster (for some specific cases)
progress_bar.progress()

content = first_entry['group']
if has_content(content):
    file.write("," + translator.translate(content)) # 'group'/group or class of monster, like animal nomenclature
progress_bar.progress()

content = first_entry['alignment']
if has_content(content):
    file.write("," + translator.translate(content)) # 'alignment'/alignment from the 3x3 alignment grid
file.write(LX.lNew_line + LX.new_line) # end line of information with linebreak
progress_bar.progress()

file.write(LX.thin_line + LX.new_line) #seperation to "box in" name and basic description

#armor_class and armor_desc go into one line
content = first_entry['armor_class']
file.write(LX.bold("AC: "))
if has_content(content):
    file.write(str(content)) # 'armor_class'/armor value AC of the monster
progress_bar.progress()

content = first_entry['armor_desc']
if has_content(content):
    file.write(", " + translator.translate(content)) # 'armor_desc'/type of amor, as in natural armor etc.
progress_bar.progress()
file.write(LX.lNew_line + LX.new_line)

#I almost always use hit_points, life values can always be adjusted on the fly, no need for hitpoints
file.write(LX.bold("Leben: "))
content = first_entry['hit_points']
if has_content(content):
    file.write(str(content)) # 'hit_points'/HP of monster, these are the average values from the 'hit_dice' not used here
file.write(LX.lNew_line + LX.new_line)
progress_bar.progress()

#movement speed is automatically converted to m
file.write(LX.bold("Geschw.: "))
content = first_entry['speed']
if has_content(content):
    first = True
    for speed in content:
        if(first):
            first = False
        else:
            file.write(", ")
        file.write(translator.translate(speed) + ": " + str(math.floor(content[speed] / 3.281)) + "m")
file.write(LX.lNew_line + LX.new_line)
progress_bar.progress()

file.write(LX.new_line) #seperation for better formating

file.write("\\begin{tabular}{|c|c|c|c|c|c|}" + LX.new_line)
file.write(LX.tab + "\\hline" + LX.new_line)
file.write(LX.tab + LX.bold("STR") + " & " + LX.bold("DEX") + " & " + LX.bold("CON") + " & " + LX.bold("INT") + " & " + LX.bold("WIS") + " & " + LX.bold("CHA") + "\\\\\\hline" + LX.new_line)
#stats are assumed to be present, if not we probably crash or get -5
file.write(LX.tab + str(first_entry['strength']) + "(+" + str(math.floor((first_entry['strength'] - 10) / 2)) + ") & ")
file.write(str(first_entry['dexterity']) + "(+" + str(math.floor((first_entry['dexterity'] - 10) / 2)) + ") & ")
file.write(str(first_entry['constitution']) + "(+" + str(math.floor((first_entry['constitution'] - 10) / 2)) + ") & ")
file.write(str(first_entry['intelligence']) + "(+" + str(math.floor((first_entry['intelligence'] - 10) / 2)) + ") & ")
file.write(str(first_entry['wisdom']) + "(+" + str(math.floor((first_entry['wisdom'] - 10) / 2)) + ") & ")
file.write(str(first_entry['charisma']) + "(+" + str(math.floor((first_entry['charisma'] - 10) / 2)) + ")\\\\\\hline" + LX.new_line)
file.write("\\end{tabular}" + LX.new_line)
file.write(LX.new_line)
progress_bar.progress()

#check if the text lines are required
exists = False # for formatting later on
if has_content(first_entry['strength_save']) or has_content(first_entry['dexterity_save']) or has_content(first_entry['constitution_save']) or has_content(first_entry['intelligence_save']) or has_content(first_entry['intelligence_save']) or has_content(first_entry['charisma_save']):
    file.write(LX.bold("Rettungswürfe:") + LX.lNew_line + LX.new_line)
    exists = True
content = first_entry['strength_save']
if has_content(content):
    file.write("STR:" + str(content) + "/")
content = first_entry['dexterity_save']
if has_content(content):
    file.write("DEX:" + str(content) + "/")
content = first_entry['constitution_save']
if has_content(content):
    file.write("CON:" + str(content) + "/")
content = first_entry['intelligence_save']
if has_content(content):
    file.write("INT:" + str(content) + "/")
content = first_entry['wisdom_save']
if has_content(content):
    file.write("WIS:" + str(content) + "/")
content = first_entry['charisma_save']
if has_content(content):
    file.write("CHA:" + str(content))
if exists:
    file.write(LX.lNew_line + LX.new_line) # this must be conditional as it can cause errors in LaTeX to have '\\' in the wrong place
progress_bar.progress()

content = first_entry['desc']
if has_content(content):
    file.write(LX.bold("Beschreibung: ") + translator.translate(content) + LX.lNew_line + LX.new_line) # 'desc'/lore or story of the monster
progress_bar.progress()
#seperator for "abilities", this is personal preferance
file.write("\\underline{" + LX.bold("Fähigkeiten:") + "}" + LX.lNew_line + LX.new_line)

content = first_entry['skills']
if has_content(content):
    first = True
    for skill in content:
        if first:
            first = False
        else:
            file.write(", ")
        file.write(translator.translate(skill) + " +" + str(content[skill]))
    file.write(LX.lNew_line + LX.new_line)
progress_bar.progress()

content = first_entry['damage_vulnerabilities']
if has_content(content):
    file.write(LX.bold("Schwächen:") + translator.translate(content) + LX.lNew_line + LX.new_line) # 'damage_vulnerabilities'/weakness of the monster 2x damage
progress_bar.progress()

content = first_entry['damage_resistances']
if has_content(content):
    file.write(LX.bold("Resistenzen:") + translator.translate(content) + LX.lNew_line + LX.new_line) # 'damage_resistances'/resistances of the monster 0.5x damage
progress_bar.progress()

content = first_entry['damage_immunities']
if has_content(content):
    file.write(LX.bold("Immunitäten:") + translator.translate(content) + LX.lNew_line + LX.new_line) # 'damage_immunities'/immunities of the monster 0x damage
progress_bar.progress()

content = first_entry['condition_immunities']
if has_content(content):
    file.write(LX.bold("Zustands-Immunitäten:") + translator.translate(content) + LX.lNew_line + LX.new_line) # 'condition_immunities'/can't be effected by those conditions
progress_bar.progress()

content = first_entry['senses']
if has_content(content):
    file.write(LX.bold("Sinne:") + translator.translate(content) + LX.lNew_line + LX.new_line) # 'senses'/senses of the monster (e.g.: darkvision etc.)
progress_bar.progress()

content = first_entry['languages']
if has_content(content):
    file.write(LX.bold("Sprachen:") + translator.translate(content) + LX.lNew_line + LX.new_line) # 'languages'/languages the monster can speak/understand
progress_bar.progress()

content = first_entry['challenge_rating']
if has_content(content):
    file.write(LX.bold("DC: ") + str(content) + LX.lNew_line + LX.new_line) # 'challange_rating'/CR,DC of the monster
progress_bar.progress()

file.write(LX.thin_line + LX.new_line) # seperator for section 'what the monster is' to 'what the monster can do'

content = first_entry['actions']
if has_content(content):
    file.write(LX.bold_large("Aktionen:") + LX.new_line)
    for action in content:
        file.write(LX.bold(translator.translate(action['name'])) + ": " + translator.translate(action['desc']) + LX.lNew_line + LX.new_line)
    file.write(LX.thin_line + LX.new_line)

content = first_entry['bonus_actions']
if has_content(content):
    file.write(LX.bold_large("Bonusaktionen:") + LX.new_line)
    for bonus_action in content:
        file.write(LX.bold(translator.translate(bonus_action['name'])) + ": " + translator.translate(bonus_action['desc']) + LX.lNew_line + LX.new_line)
    file.write(LX.thin_line + LX.new_line)
progress_bar.progress()

content = first_entry['reactions']
if has_content(content):
    file.write(LX.bold_large("Reaktionen:") + LX.new_line)
    for reaction in content:
        file.write(LX.bold(translator.translate(reaction['name'])) + ": " + translator.translate(reaction['desc']) + LX.lNew_line + LX.new_line)
    file.write(LX.thin_line + LX.new_line)
progress_bar.progress()

content = first_entry['legendary_desc']
if has_content(content):
    file.write(LX.bold_large("Legendär:") + LX.new_line)
    file.write(translator.translate(content) + LX.lNew_line + LX.new_line)
    file.write(LX.thin_line + LX.new_line)
progress_bar.progress()

content = first_entry['legendary_actions']
if has_content(content):
    file.write(LX.bold_large("Legendäre Aktionen:") + LX.new_line)
    for legendary_action in content:
        file.write(LX.bold(translator.translate(legendary_action['name'])) + ": " + translator.translate(legendary_action['desc']) + LX.lNew_line + LX.new_line)
    file.write(LX.thin_line + LX.new_line)
progress_bar.progress()

content = first_entry['special_abilities']
if has_content(content):
    file.write(LX.bold_large("Spezielle Eigenschaften:") + LX.new_line)
    for special_ability in content:
        file.write(LX.bold(translator.translate(special_ability['name'])) + ": " + translator.translate(special_ability['desc']) + LX.lNew_line + LX.new_line)
    file.write(LX.thin_line + LX.new_line)
progress_bar.progress()

content = first_entry['spell_list']
if has_content(content) and len(content) > 0:
    file.write(LX.bold_large("Zauberliste:") + LX.new_line)
    for spell in content:
        file.write(LX.bold(spell) + LX.lNew_line + LX.new_line)
    file.write(LX.thin_line + LX.new_line)
progress_bar.progress()

content = first_entry['environments']
if has_content(content):
    file.write(LX.bold("Umgebungen: "))
    first = True
    for environment in content:
        if first:
            first = False
        else:
            file.write(", ")
        file.write(translator.translate(environment))
    file.write(LX.lNew_line + LX.new_line)
progress_bar.progress()

content = first_entry['page_no']
if has_content(content):
    file.write(LX.bold("Seitennummer: ") + str(content) + LX.lNew_line + LX.new_line) # 'page_no'/page number of "D&D 5E Monster Manual (english ver.)"
progress_bar.progress()

#seperation line to other content
file.write(LX.thick_line + LX.new_line + LX.new_line)

file.close()