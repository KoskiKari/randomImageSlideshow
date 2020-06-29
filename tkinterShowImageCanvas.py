import tkinter as tk
from PIL import Image, ImageTk
import random,glob

#1280×720

class App(tk.Frame):
    def __init__(self,root):
        super().__init__()
        self.createCanvas()
        self.nameLabel()
        self.buttonWidget()
        self.loadImage()

    def createCanvas(self):
        #create canvas to host the image
        self.canvas = tk.Canvas(width=1280,height=720)
        self.canvas.pack()

    def randomImg(self):
        global images
        global currentImage

        #make sure the image is different from the current
        while True:
            tmpImage = random.choice(images)
            if tmpImage != currentImage:
                currentImage = tmpImage
                break
        return currentImage

    def nameLabel(self):
        global currentImage
        self.lbl = tk.Label(text=currentImage)
        self.lbl.pack(side = 'top')

    def buttonWidget(self):
        self.btn = tk.Button(text='Update', command=self.refresh)
        self.btn.pack(side = 'bottom')

    def refresh(self):
        #destroy and re-initialize image and name of file
        self.canvas.delete('all')
        self.loadImage()
        self.lbl.destroy()
        self.nameLabel()

    def loadImage(self):
        global running
        global afterJob

        #load image and resize to fit canvas
        self.loadImg = Image.open(self.randomImg())
        self.resizedImg = self.loadImg.resize((1280,720),Image.ANTIALIAS)
        self.renderTk = ImageTk.PhotoImage(self.resizedImg)

        #add image to canvas
        self.canvas.create_image(0,0,image=self.renderTk,anchor='nw')

        #if first time around run after() plainly
        if not running:
            afterJob = self.canvas.after(3000,self.refresh)
            running = True

        #in case user press update, cancel after() and make new one
        else:
            self.canvas.after_cancel(afterJob)
            afterJob = self.canvas.after(3000,self.refresh)

#main
global running
global afterJob
global images
global currentImage

#get all jpg from the folder and set current image
images = [i for i in glob.glob('*.jpg')]
currentImage = random.choice(images)

#set flag for after() not running
running = False

root = tk.Tk()
root.title('Random Slideshow')
root.resizable(False,False)
app = App(root)
root.mainloop()