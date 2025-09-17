from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import pymysql
import os
import cv2
import numpy as np
from time import strftime  # for getting time
from datetime import datetime

class Face_Recognition:
    def __init__(self, root):
        self.root = root
        self.train_classifier()
        self.face_recog()

    def face_recog(self):
        def draw_boundray(img, classifier, scaleFactor, minNeighbors, color, text, clf):
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)

            for (x, y, w, h) in features:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
                id, predict = clf.predict(gray_image[y:y + h, x:x + w])
                confidence = int((100 * (1 - predict / 300)))

                conn = pymysql.connect(host="127.0.0.1",user="root",password="Mohibali123@",database="face_recognizer",port=3305)
                my_cursor = conn.cursor()

                my_cursor.execute("SELECT Name FROM student WHERE StudentID=" + str(id))
                n = my_cursor.fetchone()
                n = "+".join(n) if n else "Unknown"

                my_cursor.execute("SELECT Roll FROM student WHERE StudentID=" + str(id))
                r = my_cursor.fetchone()
                r = "+".join(r) if r else "Unknown"

                my_cursor.execute("SELECT DEP FROM student WHERE StudentID=" + str(id))
                d = my_cursor.fetchone()
                d = "+".join(d) if d else "Unknown"

                my_cursor.execute("SELECT StudentID FROM student WHERE StudentID=" + str(id))
                i = my_cursor.fetchone()
                i =  str(i[0]) if i else "Unknown"

                if confidence > 80:
                    cv2.putText(img, f"Student ID: {i}", (x, y - 75), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    cv2.putText(img, f"Roll: {r}", (x, y - 55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    cv2.putText(img, f"Name: {n}", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)   
                    cv2.putText(img, f"Department: {d}", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    self.mark_attendence(i,r,n,d)
                else:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    cv2.putText(img, "Unknown Face", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)

            return img

        def recognize(img, clf, faceCascade):
            return draw_boundray(img, faceCascade, 1.3, 5, (255, 255, 255), "Face", clf)

        faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("classifier.xml")
#EE
        video_cap = cv2.VideoCapture(0)
        cv2.namedWindow("WELCOME TO FACE RECOGNITION", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("WELCOME TO FACE RECOGNITION", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        while True:
            ret, img = video_cap.read()
            if not ret:
                print("Failed to capture image")
                break

            img = recognize(img, clf, faceCascade)
            cv2.imshow("WELCOME TO FACE RECOGNITION", img)

            if cv2.waitKey(1) == 13:
                break

        
        video_cap.release()
        cv2.destroyWindow("WELCOME TO FACE RECOGNITION")  # Destroy the specific window
        cv2.destroyAllWindows()  # Ensure no lingering windows exist
        self.root.destroy()


#_________________ATTENDENCE MARKING____________________
    def mark_attendence(Self,i,r,n,d):
        with open("excelSheet.csv","r+",newline='\n') as f:
            myDataList=f.readlines()
            name_list=[]
            for line in myDataList:
                entry=line.split((",")) #umer,005,cs
                name_list.append(entry[0])

            if((i not in name_list) and (r not in name_list) and (n not in name_list)and (d not in name_list) ):
                now=datetime.now()
                d1=now.strftime("%d/%m/%y")
                dtString=now.strftime("%H:%M:%S")
                f.writelines(f"\n{i},{r},{n},{d},{dtString},{d1},Present")


    def train_classifier(self):
        data_dir = "data"  # all data move to data dir
        path = [os.path.join(data_dir, file) for file in os.listdir(data_dir)]  # all data move to path
        faces = []
        ids = []
        for image in path:
            img = Image.open(image).convert("L")  # gray scale image conversion
            imageNp = np.array(img, 'uint8')  # datatype
            id = int(os.path.split(image)[1].split('.')[1])

            faces.append(imageNp)
            ids.append(id)
           

        ids = np.array(ids)  # id converting to numpy #88% fast performance
        # _____________train the classifier--------------
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces, ids)
        clf.write("classifier.xml")
        cv2.destroyAllWindows()





if __name__ == "__main__":
    root = Tk()
    root.withdraw()
    obj = Face_Recognition(root)
    root.mainloop()