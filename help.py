from tkinter import*
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox




class Help:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1400x790+0+0")
        self.root.title("STUDENT MANAGEMENTSYSTEM")

        # Get the screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        self.root.geometry(f"{screen_width}x{screen_height}+0+0")

        img1 = Image.open(r"college_images\WhatsApp Image 2024-11-26 at 21.23.24_3805640f.jpg")
        img1 = img1.resize((screen_width, screen_height), Image.Resampling.LANCZOS)  # Resize dynamically
        self.photoimg1 = ImageTk.PhotoImage(img1)

        # Create a Label to display the background image
        bg_img = Label(self.root, image=self.photoimg1)
        bg_img.place(x=0, y=0, width=screen_width, height=screen_height)

        title_lbl1=Label(bg_img,text="HELP DESK",font=("Helvetica", 20, "bold"), fg="#001F54",bg="white")
        title_lbl1.place(x=-100,y=-5,width=1530,height=40) 

        title_lbl2=Label(bg_img,text="CONTACT",font=("Helvetica", 20, "bold"), fg="#001F54",bg="white")
        title_lbl2.place(x=550,y=450) 

        title_lbl2=Label(bg_img,text="SU92-BSCSM-S23-003@superior.edu.pk",font=("Helvetica",15,"bold"), fg="#001F54",bg="white")
        title_lbl2.place(x=450,y=500) 

        title_lbl2=Label(bg_img,text="SU92-BSCSM-S23-005@superior.edu.pk",font=("Helvetica",15,"bold"), fg="#001F54",bg="white")
        title_lbl2.place(x=450,y=550) 

        title_lbl2=Label(bg_img,text="SU92-BSCSM-S23-030@superior.edu.pk",font=("Helvetica",15,"bold"), fg="#001F54",bg="white")
        title_lbl2.place(x=450,y=600)  





if __name__== "__main__":
    root=Tk() #calling root with tool kit
    obj=Help(root)
    root.mainloop()
