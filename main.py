import tkinter as tk
from tkinter import colorchooser
from tkinter import simpledialog
import time
import subprocess
import webbrowser


# updates current color for future use 
def update_color():
    r = entry_r.get()
    g = entry_g.get()
    b = entry_b.get()

    try:
        r = int(r)
        g = int(g)
        b = int(b)

        if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
            colorLabel.config(bg=f'#{r:02X}{g:02X}{b:02X}')
            resultLabel.config(text=f'R: {r}, G: {g}, B: {b}')
            rgbReturn = r, g, b
            return rgbReturn
        else:
            resultLabel.config(text="Invalid value(s) (over 255)")
    except ValueError:
        resultLabel.config(text="Please enter integers (numbers) less than 255.")

    return None



# opens and stores values for custom color picker
def openColorPicker():
    color = colorchooser.askcolor(title="Custom Color")
    
    if color[1]:
        if color[1]:
            r, g, b = [int(x) for x in color[0]]
            entry_r.delete(0, tk.END)
            entry_g.delete(0, tk.END)
            entry_b.delete(0, tk.END)
            entry_r.insert(0, str(r))
            entry_g.insert(0, str(g))
            entry_b.insert(0, str(b))
            update_color()
        
        pickR, pickG, pickB = [int(x) for x in color[0]]
        print(f"Selected Color: R={pickR}, G={pickG}, B={pickB}")
        return pickR, pickG, pickB
    else:
        print("Color selection canceled.")
        return None



#Popup after creation is done. this one is only shown when you choose to create AND open 
def successMessageOPEN(filename):
    popup = tk.Tk()
    popup.geometry("300x100")
    popup.title("File Creation Status")

    label = tk.Label(popup, text="Created " + filename + " successfully!", padx=20, pady=20)
    label.pack()
    label2 = tk.Label(popup, text="Opening " + filename, padx=30, pady=30)
    label2.pack()

    ok_button = tk.Button(popup, text="OK", command=popup.destroy)
    ok_button.pack()
    
    time.sleep(1)
    subprocess.run(["start", filename], shell=True)

    popup.mainloop()



#inserts defualt windows values 
def defaultValues():
    entry_r.insert(0, str(0))
    entry_g.insert(0, str(120))
    entry_b.insert(0, str(215))
    update_color()



#Popup after creation is done. only shows when only chose to create and not open 
def successMessage(filename):
    popup = tk.Tk()
    popup.geometry("300x100")
    popup.title("File Creation Status")

    label = tk.Label(popup, text="Created " + filename + " successfully!", padx=20, pady=20)
    label.pack()

    ok_button = tk.Button(popup, text="OK", command=popup.destroy)
    ok_button.pack()

    popup.mainloop()




#Creates file AND automaticly opens 3 seconds later, tied to createButton1
def createAndOpen():
    fileName = simpledialog.askstring("File Name", "Enter the file name:")
    rgbValues = update_color()
    if rgbValues is not None:
        r, g, b = rgbValues
        rgbString = f"{r} {g} {b}"
        regContent = fr"""Windows Registry Editor Version 5.00

[HKEY_CURRENT_USER\Control Panel\Colors]
"Hilight"="{rgbString}"
"HotTrackingColor"="{rgbString}"
"""

    filePath = fileName + ".reg"

    with open(filePath, "w") as regFile:
        regFile.write(regContent)

    successMessageOPEN(filePath)

    

    
#Creates file but doesnt automaticly open, tied to createButton2
def createNotOpen():
    fileName = simpledialog.askstring("File Name", "Enter the file name:")
    rgbValues = update_color()
    if rgbValues is not None:
        r, g, b = rgbValues
        rgbString = f"{r} {g} {b}"
        print(rgbString)
        regContent = fr"""Windows Registry Editor Version 5.00

[HKEY_CURRENT_USER\Control Panel\Colors]
"Hilight"=sz:"{rgbString}"
"HotTrackingColor"=sz:"{rgbString}"
"""

    filePath = fileName + ".reg"

    with open(filePath, "w") as regFile:
        regFile.write(regContent)

    successMessage(filePath)

    print(f"File '{filePath}' created successfully.")
     
     
     
     
     
#GUI 

window = tk.Tk()
window.title("TransBoxEnhanced")

entry_r = tk.Entry(window, width=20)
entry_g = tk.Entry(window, width=20)
entry_b = tk.Entry(window, width=20)

entry_r.grid(row=0, column=0, padx=5, pady=5)
entry_g.grid(row=0, column=1, padx=5, pady=5)
entry_b.grid(row=0, column=2, padx=5, pady=5)

label_r = tk.Label(window, text="R:")
label_g = tk.Label(window, text="G:")
label_b = tk.Label(window, text="B:")

label_r.grid(row=1, column=0)
label_g.grid(row=1, column=1)
label_b.grid(row=1, column=2)

label_info1 = tk.Label(window, text="  Welcome to TransBoxEnhanced")
label_info2 = tk.Label(window, text=" translucent box customizer for windows")
label_info1.bind("<Button-1>", lambda e: webbrowser.open_new("https://www.deprived.lol"))
label_info3 = tk.Label(window, text=" Choose color then select option for .reg")
label_info1.grid(row=1, column=0, rowspan=3, padx=25, pady=30)
label_info2.grid(row=2, column=0, rowspan=3, padx=25, pady=30)
label_info3.grid(row=3, column=0, rowspan=3, pady=30)

updateButton = tk.Button(window, text="View Color  (If Manually Typed)", command=update_color)
updateButton.grid(row=2, column=2, pady=20)

createButton1 = tk.Button(window, text="Create AND Run .reg (Admin)", command=createAndOpen)
createButton1.grid(row=3, column=2, pady=20)

createButton2 = tk.Button(window, text="Create .reg file", command=createNotOpen)
createButton2.grid(row=3, column=3, pady=20)

updateButton = tk.Button(window, text="Open Color Picker", command=openColorPicker)
updateButton.grid(row=6, column=3, pady=20)

defaultButton = tk.Button(window, text="Default Values", command=defaultValues)
defaultButton.grid(row=6, column=2, pady=20)

resultLabel = tk.Label(window, text="")
resultLabel.grid(row=4, column=1, columnspan=4, pady=20)


colorLabel = tk.Label(window, text="", width=20, height=2)
colorLabel.grid(row=6, column=0, columnspan=3, pady=10)


window.mainloop()