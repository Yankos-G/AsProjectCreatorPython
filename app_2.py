import tkinter
import customtkinter  # <- import the CustomTkinter module
from PIL import Image
import os
import main
import bot_test

#    os.system("bot_test.py")
root = tkinter.Tk()  # create the Tk window like you normally do
root.title("Quick project")

root.configure(bg='white')

IMAGE_PATH = 'C:/Users/Szkolenie/Desktop/br_logo.jpg'

def button_AS():
    var = input_AS_path.get()
    label_input_AS.configure(text=var)
    print(var)

def button_project():
    var = input_project_path.get()
    label_input_project.configure(text=var)
    print(var)

def button_bot_start():
    var = input_project_path.get()
    label_input_project.configure(text=var)
    os.system("bot_test.py")
    print(var)

def add_module():
    var = input_project_path.get()
    label_input_project.configure(text=var)
    os.system("main.py")
    print(var)

customtkinter.set_appearance_mode("Light") # Other: "Light", "System" (only macOS)

r0=0
r1=1
r2=2
r3=3
r4=4
r5=5
c0=0
c1=1
c2=2
c3=3
c4=4
c5=5

button_add_module = customtkinter.CTkButton(master=root, fg_color=("orange"), border_width=2,border_color="black",
                                             text_color=("gray10", "#DCE4EE"),command=add_module, text="Add module")
button_add_module.grid(row=r5, column=c2, padx=(20, 20), pady=(20, 20), sticky="nsew")

button_bot = customtkinter.CTkButton(master=root, fg_color=("orange"), border_width=2,border_color="black",
                                             text_color=("gray10", "#DCE4EE"),command=button_bot_start, text="New project bot")
button_bot.grid(row=r5, column=c1, padx=(20, 20), pady=(20, 20), sticky="nsew")
# INPUT PROJECTS
input_AS_path = customtkinter.CTkEntry(root, placeholder_text=r"np. 'C:\'")
input_AS_path.grid(row=r2, column=c1, columnspan=2, padx=(20, 0), pady=(15, 20), sticky="nsew")
button_AS_path = customtkinter.CTkButton(master=root, fg_color=("orange"), border_width=2,border_color="black",
                                             text_color=("gray10", "#DCE4EE"),command=button_AS, text="Potwierdź")
button_AS_path.grid(row=r2, column=c3, padx=(20, 20), pady=(20, 20), sticky="nsew")
# INPUT AS
input_project_path = customtkinter.CTkEntry(root, placeholder_text=r"np. 'C:\projects'")
input_project_path.grid(row=r4, column=c1, columnspan=2, padx=(20, 0), pady=(15, 20), sticky="nsew")
button_project_path = customtkinter.CTkButton(master=root, fg_color=("orange"), border_width=2,border_color="black",
                                             text_color=("gray10", "#DCE4EE"),command=button_project, text="Potwierdź")
button_project_path.grid(row=r4, column=c3, padx=(20, 20), pady=(20, 20), sticky="nsew")

label_input_AS = customtkinter.CTkLabel(master=root,
                               text='None',
                               width=120,
                               height=25,
                               corner_radius=8)
label_input_AS.grid(row=r2,column=c4,padx=(20, 20), pady=(20, 20))

label_AS_TEXT = customtkinter.CTkLabel(master=root,
                               text='Wprowadź ścieżkę do pliku AS',
                               width=120,
                               height=25,
                               corner_radius=8)
label_AS_TEXT.grid(row=r1,column=c1,padx=(20, 0), pady=(20, 0))

label_project_TEXT = customtkinter.CTkLabel(master=root,
                               text='Wprowadź ścieżkę do projektów',
                               width=120,
                               height=25,
                               corner_radius=8)

label_input_project = customtkinter.CTkLabel(master=root,
                               text='None',
                               width=120,
                               height=25,
                               corner_radius=8)
label_input_project.grid(row=r4,column=c4,padx=(20, 20), pady=(20, 20))
#---------------------TEXT-----------------------------
label_project_TEXT.grid(row=r3,column=c1,padx=(20, 0), pady=(20, 0))

IMG = customtkinter.CTkImage(light_image=Image.open(os.path.join(IMAGE_PATH)), size=(192 , 102))
label = customtkinter.CTkLabel(master=root, image=IMG, text='')

label.place(relx=0.37, rely=0.37, anchor=tkinter.S)

s = customtkinter.CTkLabel(master=root, text='')
s.grid(column=c0, row=r0,padx=(10,10),ipady=70)


if __name__ == "__main__":
    root.mainloop()
