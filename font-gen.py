# Copyright (c) 2022 Oxi. All rights reserved.
from PIL import Image, ImageDraw, ImageFont
import math
import tkinter as tk
from tkinter import filedialog
import os
import glob
from time import sleep

root = tk.Tk()
root.withdraw()

print("Loading Config...")
f = open('config.txt', encoding="utf-8")
configText = f.read()
f.close()
configData = {}
for line in configText.split("\n"):
    line = ''.join(line.split(" "))
    configData[line.split("=")[0]] = '='.join(line.split("=")[1:])

requiredConfigEntries = ['charSize', 'charSet']
for entry in requiredConfigEntries:
    if not entry in configData:
        raise ExceptionError(f'Error > "{entry}" is missing in the config.')
        
charSize = (int(configData['charSize'].split(",")[0]), int(configData['charSize'].split(",")[1]))
characters = configData['charSet']

print("Done.")
print("")

images = []
fontFile = filedialog.askopenfilename(title="Select font", initialdir="/fonts", filetypes=[('Font File', '.ttf'),('Font File', '.otf')])
fontName = fontFile.split("/")[len(fontFile.split("/"))-1].split(".")[0]

fontSize = 1
font = ImageFont.truetype(fontFile, fontSize)

print("Loaded Font.")

sleep(0.5)
#charSize = (int(input("Character Image Size X: ")), int(input("Character Image Size Y: ")))
print(f"Using Character Sprite Size of {charSize[0]}px x {charSize[1]}px.")
sleep(1)

# fraction of height that font should fit
fontFrac = 0.9

# determine font size
breakSize = fontFrac * charSize[1]
jumpSize = 75
while True:
    if font.getbbox("A")[3] < breakSize:
        fontSize += jumpSize
    else:
        jumpSize = jumpSize // 2
        fontSize -= jumpSize
    font = ImageFont.truetype(fontFile, fontSize)
    if jumpSize <= 1:
        break
    
print("Calculated Font Size.")

sleep(0.5)
print("")

# CHARACTER IMAGE GENERATION
print(f"Generating {len(characters)} Character Frames...")
for char in characters:
    W, H = charSize
    image = Image.new('RGBA', charSize)
    draw = ImageDraw.Draw(image)
    _, _, w, h = draw.textbbox((0, 0), char, font=font)
    draw.text(((W-w)/2, (H-h)/2), char, font=font, fill='white')
    images.append([image, char])
print("Done.")

sleep(1)
print("")

# SPRITESHEET GENERATION
print("Generating Spritesheet...")

if os.path.isdir(f'output/{fontName}'):
    for f in glob.glob(f'output/{fontName}/*'):
        os.remove(f)
else:
    os.mkdir(f'output/{fontName}')

def isPerfect(N):
    if (math.sqrt(N) - math.floor(math.sqrt(N)) != 0):
        return False
    return True

def ceilPerfect(N):
    current = N
    while not isPerfect(current):
        current += 1
    return current

def merge_images(image1, image2, dr):
    (width1, height1) = image1.size
    (width2, height2) = image2.size

    if dr == "x":
        result_width = width1 + width2
        result_height = max(height1, height2)

        result = Image.new('RGBA', (result_width, result_height))
        result.paste(im=image1, box=(0, 0))
        result.paste(im=image2, box=(width1, 0))
        return result
    elif dr == "y":
        result_width = max(width1, width2)
        result_height = height1 + height2

        result = Image.new('RGBA', (result_width, result_height))
        result.paste(im=image1, box=(0, 0))
        result.paste(im=image2, box=(0, height1))
        return result

sqrCount = 0
sideLength = 0
extras = 0

itemMap = {}

outName = f'output/{fontName}/{fontName}-fontsheet.png'

sqrCount = ceilPerfect(len(images))
sideLength = int(math.sqrt(sqrCount))
extras = sqrCount - len(images)

rows = []
rowIndex = 0
# do all rows except last
while rowIndex < math.sqrt(sqrCount)-1:
    row = images[rowIndex*sideLength][0]
    itemMap[rowIndex*sideLength]=(rowIndex, 0)
    imgIndex = (rowIndex*sideLength) + 1
    column = 1
    while imgIndex < (rowIndex+1)*sideLength:
        p = (imgIndex/len(images))*100
        print(f'Creating Rows {int(p)}%')

        itemMap[imgIndex]=(rowIndex, column)
        row = merge_images(row, images[imgIndex][0], 'x')
        imgIndex += 1
        column += 1
    rows.append(row)
    rowIndex+=1

# do last row (may not fill fully)
index = int(sqrCount-math.sqrt(sqrCount))
lastRow = images[index][0]
itemMap[index]=(rowIndex, 0)
imgIndex = (index)+1
column = 1
while imgIndex < len(images):
    p = (imgIndex/len(images))*100
    print(f'Creating Rows {int(p)}%')
    itemMap[imgIndex]=(rowIndex, column)
    lastRow = merge_images(lastRow, images[imgIndex][0], 'x')
    imgIndex += 1
    column += 1
rows.append(lastRow)

print("Merging Rows...")

finalIndex = 1
final = rows[0]
while finalIndex < len(rows):
    final = merge_images(final, rows[finalIndex], 'y')
    finalIndex += 1

print("Saving...")
final.save(outName)
final.close()
print("Done.")
sleep(1)
print("")
print("Generating Lua...")

charMap = "{\n"
for index in itemMap:
    # couple overrides to fix issues
    if images[index][1] == "'":
        images[index][1] = "\\'"
    elif images[index][1] == "\\":
        images[index][1] = "\\\\"
    # add char entry
    charMap += f"['{images[index][1]}']={{x={itemMap[index][0]}, y={itemMap[index][1]}}},\n"
charMap = charMap[:-2] + "}"

code = f"""
-- !!! PUT INTO game.ReplicatedStorage.RBXFonts AS A ModuleScript TITLED '{fontName}', AND REPLACE 'FONTSHEET_ID' WITH THE RBXASSETID !!!

-------------------------------------------------------------

-- GENERATED BY RBXFONT (https://github.com/oxi-dev0/RBXFont)
local font = {{}}

font.sheet = "FONTSHEET_ID" -- Roblox Fontsheet Image ID            <-------- PLEASE REPLACE
font.charSize = {{x={charSize[0]},y={charSize[1]}}} -- Size of each character in pixels
font.columns = {sideLength} -- Number of columns
font.rows = {sideLength} -- Number of rows

font.charMap = {charMap}

return font
"""

print(f"Saving Lua to 'output/{fontName}/fontCode.txt'...")
f = open(f'output/{fontName}/fontCode.txt', 'w+')
f.write(code)
f.close()
print(f"Done.")
print("")
sleep(0.5)
print(f"Please copy the code in 'output/{fontName}/fontCode.txt' to game.ReplicatedStorage.RBXFonts as a ModuleScript titled '{fontName}'")
print(f"Then, upload the fontsheet image in 'output/{fontName}' to roblox, and replace 'FONTSHEET_ID' in the module script with the RBXASSETID string.")
