import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import font
from PIL import ImageTk
from PIL import Image
from diffusers import DiffusionPipeline, StableDiffusionPipeline
from tkinter import filedialog

access_tokens = "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"

class DrawFrame(tk.Frame):
    def __init__(self,master,ldm:StableDiffusionPipeline):
        super().__init__(master)
        ### GUI 関連 の初期化 #########################
        self.master.geometry("1200x600")
        self.master.title("DrawEditor with Text")
        
        self.pack()
        self.master.update_idletasks()
        
        self.width = self.master.winfo_width()
        self.height = self.master.winfo_height()
        
        self.frame1 = tk.Frame(
            self,
            width=int(self.width/5)*3,
            height=self.height
        )

        self.frame2 = tk.Frame(
            self,
            width=int(self.width/5)*2,
            height=self.height
        )
        self.frame1.grid(column=0,row=0)
        self.frame2.grid(column=1,row=0)
        self.frame1.update_idletasks()
        self.frame2.update_idletasks()

        self.create_widgets()
        
        ### Diffuser の初期化 #########################
        
        # load model and scheduler
        self.ldm = ldm
        self.prompt = None
        
        
        
    # Create Widgets function
    def create_widgets(self):
        
        # frame1上にウィジェットを作成
        self.canvas = tk.Canvas(
            self.frame1,
            bg="white"
        )
        self.canvas.place(x=0,y=0,width=self.frame1.winfo_width(),
            height=int((self.frame1.winfo_height()/5)*4))
        
        self.button1 = tk.Button(
            self.frame1,
            text="Save Img",
            command=self.save_img
        )
        self.button1.place(x=0,y=int((self.frame1.winfo_height()/5)*4),width=self.frame1.winfo_width(),height=int((self.frame1.winfo_height()/5)*1))
        
        # frame2上にウィジェットを作成
        #text_pallete
        # Text
        f = font.Font(family='Helvetica')
        v1 = tk.StringVar()
        self.txt = tk.Text(self.frame2)
        self.txt.configure(
            font=f
        )
        self.txt.place(x=0,y=0,width=self.frame2.winfo_width(),height=int((self.frame2.winfo_height()/5)*4))

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            self,
            orient=VERTICAL,
            command=self.txt.yview)
        self.txt['yscrollcommand'] = scrollbar.set

        # Button
        self.button2 = tk.Button(
            self.frame2,
            text="Make Image",
            command=self.make_image_from_Diffusion
        )
        self.button2.place(x=0,y=int((self.frame2.winfo_height()/5)*4),width=self.frame2.winfo_width()/2,height=int((self.frame2.winfo_height()/5)*1))
        
        self.button3 = tk.Button(
            self.frame2,
            text="Remake Image",
            command=self.remake_image_from_Diffusion
            
        )
        self.button3.place(x=self.frame2.winfo_width()/2,y=int((self.frame2.winfo_height()/5)*4),width=self.frame2.winfo_width()/2,height=int((self.frame2.winfo_height()/5)*1))
        
    # Event Callback Function
    def make_image_from_Diffusion(self):
        self._get_string()
        self._create_img()
        self._view_image()
    
    
    def _get_string(self):
        self.update()
        self.prompt = self.txt.get("1.0","end")
        
    def _get_remake_text(self):
        self.update()
        self.remake_prompt = self.txt.get("1.0","end")
        self.prompt = self.prompt+self.remake_prompt
    
    def _create_img(self):
        images = self.ldm([self.prompt], num_inference_steps=50, eta=0.3, guidance_scale=6)["images"]
        images[0].save("text_image.png")
    
    def _view_image(self):
        self.update()
        # Canvasのサイズを取得するため更新しておく
        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()
        self.photo = Image.open("text_image.png")
        self.photo = self.photo.resize((self.canvas_width, self.canvas_height))
        self.photo_image = ImageTk.PhotoImage(self.photo)
        
        self.canvas.create_image(
                self.canvas_width / 2,       # 画像表示位置(Canvasの中心)
                self.canvas_height / 2,                   
                image=self.photo_image  # 表示画像データ
                )
        
    def remake_image_from_Diffusion(self):
        self._get_remake_text()
        self._create_img()
        self._view_image()
        
    def save_img(self):
        filename =  filedialog.asksaveasfilename(
            title = "名前を付けて保存",
            filetypes = [ ("PNG", ".png")], # ファイルフィルタ
            initialdir = "./", # 自分自身のディレクトリ
            defaultextension = "bmp"
        )
        self.photo.save(filename)


def main():
    model_id = "CompVis/stable-diffusion-v1-4"
    # ldm = DiffusionPipeline.from_pretrained(model_id)
    model=StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", use_auth_token=access_tokens)
    root = tk.Tk()
    app = DrawFrame(master=root,ldm=model)#Inheritクラスの継承！
    app.mainloop()

if __name__ == "__main__":
    main()