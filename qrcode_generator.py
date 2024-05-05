import tkinter as tk 
import qrcode
from PIL import Image
from os import getcwd,remove


def generate(events=None):
    '''This function generates the qrcode when button is clicked'''
    
    show_qr.config(text="LOADING...")
    
    # changing name to save the image
    new_store_data = store_data.get()
    if "." or "?" or "/" or "//" or "https://" or "http://" in new_store_data:
        # replacing elements of link with nothing
        new_store_data = new_store_data.replace("https://","").replace("http://","")
        new_store_data = new_store_data.replace("/","").replace("-","").replace(":","")
        new_store_data = new_store_data.replace("?","").replace(".","").replace("=","")
        new_store_data = new_store_data.replace("+","").replace("&","")
    else:
        new_store_data = new_store_data
        
    # making qr code
    image_name = f"{new_store_data}.png"
    qr = qrcode.QRCode(version=10,box_size=40,border=1)
    qr.add_data(store_data.get())
    qr.make(fit=True)
    qr_image = qr.make_image(back_color="white",fill_color="black")
    qr_image.save(image_name)
    del qr,qr_image,new_store_data
    
    #resizing image
    qrcode_image = Image.open(image_name)
    new_image = qrcode_image.resize((250,250))
    new_image_name = f"new_{image_name}"
    new_image.save(f"{getcwd()}/qrcode/{new_image_name}")
    remove(image_name)
    del qrcode_image,new_image,image_name
    
    # opeing image
    image_tk = tk.PhotoImage(file=f"qrcode/{new_image_name}")
    show_qr.config(image=image_tk)
    show_qr.image = image_tk
        
        
def change_state(*a):
    '''This Function changes the state of Button'''
    
    if len(store_data.get())>0:
        button.config(state="normal")
        entry_widget.bind('<Return>',generate)
    else:
        button.config(state="disabled")
        
        
def erase_text(event):
    entry_widget.delete(0,len(store_data.get()))
    
    
if __name__=="__main__":
    root = tk.Tk()
    root.config(bg="#202020")
    root.maxsize(500,355)
    root.geometry("500x355")
    root.title("QR CODE GENERATOR")
    
    # Binding Key events
    root.bind("<Return>",generate)
    root.bind("<Control_L><a><BackSpace>",erase_text)
    root.bind("<Control_R><a><BackSpace>",erase_text)

    tk.Label(root,text="Enter data to generate it's qrcode:- ",font="Consolas 14 bold",bg="#202020",fg="#0000FF").place(x=1,y=1)

    show_qr = tk.Label(root,text="",bg="#202020")
    show_qr.place(x=100,y=97)

    store_data = tk.StringVar()
    entry_widget = tk.Entry(root,textvariable=store_data,width=60)
    entry_widget.place(x=1,y=30)


    button = tk.Button(root,text="Submit",font="helvetica 12 bold",bg="#ADD8E6",command=generate,state="disabled")
    tk.Button(root,text="Exit",font="helvetica 12 bold",bg="#ADD8E6",command=root.destroy).place(x=100,y=60)
    button.place(x=1,y=60)  

    store_data.trace_add("write",change_state)

    root.mainloop()

