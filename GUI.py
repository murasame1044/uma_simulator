import tkinter as tk
from tkinter import ttk
import tkinter

from sqlalchemy import literal

root  = tk.Tk()
root.geometry("300x800")
root.title("ステータス記入")

lbl_top = tk.Label(root, text="ウマ娘の各ステータスを入力してください")
lbl_top.place(x=20, y=30)

def make_label(x, y, txt):
    label = tk.Label(text=txt)
    label.place(x=x, y=y)
    entry = tk.Entry(width=15)
    entry.place(x=x+60, y=y)

    def getvalue():
        status = entry.get()
        return status
    
    button = tkinter.Button(text="OK", command=getvalue)


def make_combobox(x, y, text, values):
    label = tk.Label(text=text)
    label.place(x=x, y=y)
    comboBox = ttk.Combobox(master=root, width=15, values=values, justify="left", state="readonly")
    comboBox.place(x=x+60, y=y)
    
    def getvalue():
        comboBox.get()
    
    button = tkinter.Button(text="OK", command=getvalue)
    button.place(x=x+100, y=y)
    button.pack()
      

item_rst = ["大逃げ", "逃げ", "先行", "差し", "追込"]
item_rankgrd = ["S", "A", "B", "C", "D", "E", "F", "G"]
item_rankdst = ["S", "A", "B", "C", "D", "E", "F", "G"]
item_rankrst = ["S", "A", "B", "C", "D", "E", "F", "G"]

name = make_label(30, 80, "名前:")
spd = make_label(30, 130, "スピード:")
stm = make_label(30, 180, "スタミナ:")
pwr = make_label(30, 230, "パワー:")
gut = make_label(30, 280, "根性:")
itl = make_label(30, 330, "賢さ:")
rst = make_combobox(30, 380, "脚質:", item_rst)
rankgrd = make_combobox(30, 430, "バ場適正:", item_rankgrd)
rankdst = make_combobox(30, 480, "距離適正:", item_rankdst)
rankrst = make_combobox(30, 530, "脚質適正:", item_rankrst)

# rst = cmbBox_rst.get()

root.mainloop()