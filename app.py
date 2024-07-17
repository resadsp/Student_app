from tkinter import *
from datetime import date
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import Combobox
from PIL import Image, ImageTk
from odabir_grada import Gradovi
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from tksheet import Sheet
import globals as gl
import customtkinter
import tkinter.ttk as ttk
import os
import pathlib
import json
import mysql.connector as conn 
import pdfkit
from jinja2 import Template
import base64

@dataclass
class Author:
    student_id: int
    prezime: str
    ime: str
    datum_rodjenja: str
    JMBG: str
    broj_telefona: str
    grad_opstina: str
    postanski_broj: str
    region: str
    ulica: str
    broj_kuce: str
    ime_oca: str
    zanimanje_oca: str
    ime_majke: str
    zanimanje_majke: str
    devojacko_prezime: str
    naziv_skole: str
    smer: str
    godina_upisa: str
    trajanje: str
    grad_skole: str
    pol: str
    radno_stanje_oca: str
    radno_stanje_majke: str
    bracno_stanje: str
    Vrsta_s: str
    slika: str
    
    
def get_connection():
    return conn.connect(
        host="127.0.0.1",
        port=3306, 
        user="pyadmin",
        password="1234",
        database="student"
    )


gradovi = Gradovi.load_city()

def upis():
    a = gl.GlobalComponents.get("opstina_entry")
    for i in gradovi:
      if i.city == a.get():
         broj_poste_entry.insert(0, i.zip)
         Region_entry.insert(0, i.region)
   
def Exit():
    window.destroy()
    
def callbackFunc(event):
    country = event.widget.get()
    print(country)

    
def show_image():
    filename = filedialog.askopenfilename(initialdir=os.getcwd(),
                                          title="Select image file", filetype=(("JPG File", "*.jpg"),
                                                                             ("PNG File", "*.png"),
                                                                             ("All files", "*.txt")))
    img = (Image.open(filename))
    resized_image = img.resize((190,190))
    photo2 = ImageTk.PhotoImage(resized_image)
    lbl.config(image=photo2)
    lbl.image = photo2
    print(filename)
    c = str(filename)
    d = c.split("/")
    g = (d[::-1])
    e = f"{g[1]}/{g[0]}"
    gl.GlobalComponents.set("e", e)
    gl.GlobalComponents.set("filename", filename)
    
def selection():
    value = radio.get()
    if value == 1:
        gender = "Muski"
    elif value==2:
        gender = "Zenski"
    else:
        gender = None
    return gender

def selection2():
    value = pretraga.get()
    if value == 1:
        gender = "student_id"
    elif value==2:
        gender = "JMBG"
    else:
        gender = None
    return gender

def reg_number():
     connection = conn.connect(host="127.0.0.1", port=3306,
                                  user="pyadmin", password="1234", database="studenti")
     cursor = connection.cursor()
     cursor.execute("SELECT student_id FROM student ORDER BY student_id DESC LIMIT 1;")
     user_id = cursor.fetchone()
     c = list(user_id)
     a = (c[0])
     b = a + 1
     user_id = tuple((b,))
     return user_id


def Clear():
    Ime.set('')
    Prezime.set('')
    Datum_rodjenja.set('')
    JMBG.set('')
    Telefon.set('')
    Broj_poste.set('')
    Ulica.set('')
    Broj_ulice.set('')
    G_O.set('')
    Region.set('')
    Ime_oca.set('')
    Ime_majke.set('')
    Zanimanje.set('')
    Zanimanje_majke.set('')
    Devojacko.set('')
    Naziv_skole.set('')
    Smer.set('')
    Godina_upisa.set('')
    Trajanje.set('')
    Grad_skole.set('')
    Search.set('')
    radio.set('0')
    stanje_oca.set('Izaberi opciju')
    stanje_majke.set('Izaberi opciju')
    stanje.set('Izaberi opciju')
    Vrsta_skole.set('Izaberi opciju')
    img1=PhotoImage(file="img/upload_photo.png")
    lbl.config(image=img1)
    lbl.image=img1
    img=""
    
def Save():
    ime = Ime.get()
    prezime = Prezime.get()
    datum_rodjenja = Datum_rodjenja.get()
    jmbg =  JMBG.get()
    broj_telefona = Telefon.get()
    grad_opstina = G_O.get()
    br_poste = Broj_poste.get()
    regija = Region.get()
    ulica = Ulica.get()
    br_kuce = Broj_ulice.get()   
    ime_oca = Ime_oca.get()
    zanimanje_oca = Zanimanje.get()
    ime_majke = Ime_majke.get()
    zanimanje_majke = Zanimanje_majke.get()
    dev = Devojacko.get()
    naziv_skole = Naziv_skole.get()
    smer = Smer.get()
    godina_upisa = Godina_upisa.get()
    trajanje = Trajanje.get()
    grad_skole = Grad_skole.get()
    pol = selection()
    radno_stanje_oca= stanje_oca.get()
    radno_stanje_majke = stanje_majke.get()
    bracno_stanje = stanje.get()
    Vrsta_s = Vrsta_skole.get()
    slika = gl.GlobalComponents.get("e")



    if ime == "" or prezime == "" or datum_rodjenja=="" or jmbg=="" or broj_telefona=="" or regija=="" or ulica=="" or br_kuce=="" or ime_oca=="" or zanimanje_oca=="" or ime_majke=="" or zanimanje_majke=="" or dev=="" or naziv_skole=="" or smer=="" or godina_upisa=="" or trajanje=="" or grad_skole=="" or radio==None or s=="Izaberi opciju" or stanje_oca=="Izaberi opciju" or stanje_majke=="Izaberi opciju" or Vrsta_s=="Izaberi opciju" or slika==None:
            messagebox.showerror("Error", "Morate popuniti sva polja i izabrati jednu opciju od ponudjenih kao i ucitati sliku.")
    if len(jmbg) != 13:
        messagebox.showerror("Error", "JMBG mora imati 13 cifara.")
    else:
        connection = conn.connect(host="127.0.0.1", port=3306,
                                    user="pyadmin", password="1234", database="studenti")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM student WHERE JMBG = %s;",(jmbg, ))
        rez = cursor.fetchall()
        if rez == []:
            cursor.execute("INSERT INTO student VALUES(NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s);",
                        (ime, prezime, datum_rodjenja, jmbg, broj_telefona, grad_opstina, br_poste, regija, ulica, br_kuce, ime_oca, zanimanje_oca, ime_majke, zanimanje_majke, dev, naziv_skole, smer, godina_upisa, trajanje, grad_skole, pol, radno_stanje_oca, radno_stanje_majke, bracno_stanje, Vrsta_s, slika))
            user_id = cursor.lastrowid
            connection.commit()
            if user_id:
                messagebox.showinfo("Uspesno!", "Uspesno ste sacuvali podatke.")
            else:
                 messagebox.showerror("Neuspesno!", "Niste uspeli da sacuvate podatke!")
        else:
            messagebox.showwarning("Postoji", "Postoji student sa datim podacima. Unesite ponovo!")
            
        cursor.execute("SELECT student_id FROM student ORDER BY student_id DESC LIMIT 1;")
        user_id = cursor.fetchone()
        c = list(user_id)
        a = (c[0])
        b = a + 1
        gl.GlobalComponents.set("b",b)
        cursor.close()
        re = gl.GlobalComponents.get("b")
        Registration.set(re)
        Ime.set('')
        Prezime.set('')
        Datum_rodjenja.set('')
        JMBG.set('')
        Telefon.set('')
        Broj_poste.set('')
        Ulica.set('')
        Broj_ulice.set('')
        G_O.set('')
        Region.set('')
        Ime_oca.set('')
        Ime_majke.set('')
        Zanimanje.set('')
        Zanimanje_majke.set('')
        Devojacko.set('')
        Naziv_skole.set('')
        Smer.set('')
        Godina_upisa.set('')
        Trajanje.set('')
        Grad_skole.set('')
        stanje_oca.set('Izaberi opciju')
        stanje_majke.set('Izaberi opciju')
        stanje.set('Izaberi opciju')
        Vrsta_skole.set('Izaberi opciju')
        radio.set('0')
        img1=PhotoImage(file="img/upload_photo.png")
        lbl.config(image=img1)
        lbl.image=img1
        img=""
        return user_id
    

def update():
    unos_za_pretragu = Search.get()
    ime = Ime.get()
    prezime = Prezime.get()
    datum_rodjenja = Datum_rodjenja.get()
    jmbg =  JMBG.get()
    broj_telefona = Telefon.get()
    grad_opstina = G_O.get()
    br_poste = Broj_poste.get()
    regija = Region.get()
    ulica = Ulica.get()
    br_kuce = Broj_ulice.get()   
    ime_oca = Ime_oca.get()
    zanimanje_oca = Zanimanje.get()
    ime_majke = Ime_majke.get()
    zanimanje_majke = Zanimanje_majke.get()
    dev = Devojacko.get()
    naziv_skole = Naziv_skole.get()
    smer = Smer.get()
    godina_upisa = Godina_upisa.get()
    trajanje = Trajanje.get()
    grad_skole = Grad_skole.get()
    pol = selection()
    radno_stanje_oca= stanje_oca.get()
    radno_stanje_majke = stanje_majke.get()
    bracno_stanje = stanje.get()
    Vrsta_s = Vrsta_skole.get()
    slika = gl.GlobalComponents.get("e") 

    connection = conn.connect(host="127.0.0.1", port=3306,
                                    user="pyadmin", password="1234", database="studenti")
    cursor = connection.cursor()
    sql = "UPDATE student SET ime = %s, prezime = %s, datum_rodjenja = %s, jmbg = %s, broj_telefona = %s, grad_opstina = %s, postanski_broj = %s, region = %s, ulica = %s, broj_kuce = %s, ime_oca = %s, zanimanje_oca = %s, ime_majke = %s, zanimanje_majke = %s, devojacko_prezime = %s, naziv_skole = %s, smer = %s, godina_upisa = %s, trajanje = %s, grad_skole = %s, pol = %s, radno_stanje_oca = %s, radno_stanje_majke = %s, bracno_stanje = %s, Vrsta_s = %s, slika = %s WHERE student_id = %s"
    val = (ime, prezime, datum_rodjenja, jmbg, broj_telefona, grad_opstina, br_poste, regija, ulica, br_kuce, ime_oca, zanimanje_oca, ime_majke, zanimanje_majke, dev, naziv_skole, smer, godina_upisa, trajanje, grad_skole, pol, radno_stanje_oca, radno_stanje_majke, bracno_stanje, Vrsta_s, slika, unos_za_pretragu)
    cursor.execute(sql, val)
    connection.commit()
    user_id = cursor.fetchone
    if user_id:
            messagebox.showinfo("Uspesno!", "Uspesno ste sacuvali podatke.")
    else:
         messagebox.showerror("Neuspesno!", "Niste uspeli da sacuvate podatke!")

    cursor.close()
    Search.set('')
    Ime.set('')
    Prezime.set('')
    Datum_rodjenja.set('')
    JMBG.set('')
    Telefon.set('')
    Broj_poste.set('')
    Ulica.set('')
    Broj_ulice.set('')
    G_O.set('')
    Region.set('')
    Ime_oca.set('')
    Ime_majke.set('')
    Zanimanje.set('')
    Zanimanje_majke.set('')
    Devojacko.set('')
    Naziv_skole.set('')
    Smer.set('')
    Godina_upisa.set('')
    Trajanje.set('')
    Grad_skole.set('')
    stanje_oca.set('Izaberi opciju')
    stanje_majke.set('Izaberi opciju')
    stanje.set('Izaberi opciju')
    Vrsta_skole.set('Izaberi opciju')
    radio.set('0')
    img1=PhotoImage(file="img/upload_photo.png")
    lbl.config(image=img1)
    lbl.image=img1
    img=""
    return user_id


def vrati():
    Ime.set('')
    Prezime.set('')
    Datum_rodjenja.set('')
    JMBG.set('')
    Telefon.set('')
    Broj_poste.set('')
    Ulica.set('')
    Broj_ulice.set('')
    G_O.set('')
    Region.set('')
    Ime_oca.set('')
    Ime_majke.set('')
    Zanimanje.set('')
    Zanimanje_majke.set('')
    Devojacko.set('')
    Naziv_skole.set('')
    Smer.set('')
    Godina_upisa.set('')
    Trajanje.set('')
    Grad_skole.set('')
    Search.set('')
    radio.set('0')
    stanje_oca.set('Izaberi opciju')
    stanje_majke.set('Izaberi opciju')
    stanje.set('Izaberi opciju')
    Vrsta_skole.set('Izaberi opciju')
    img1=PhotoImage(file="img/upload_photo.png")
    lbl.config(image=img1)
    lbl.image=img1
    img=""
    Button(window, text="Upload Sliku", width=19, height=2, font="arial 13 bold", bg="lightblue", fg="black", command=show_image).place(x=1690, y=410)
    Button(window, text="Sacuvaj", width=19, height=2, font="arial 13 bold", bg="lightgreen", fg="black",  command=Save).place(x=1690, y=500)
    Button(window, text="Resetuj", width=19, height=2, font="arial 13 bold", bg="lightpink",fg="black", command=Clear).place(x=1690, y=580)
    Button(window, text="Izadji", width=19, height=2, font="arial 13 bold", bg="grey", fg="black", command=Exit).place(x=1690, y=660)



def Search_student():
    unos_za_pretragu = Search.get()
    opcija = selection2()
    connection = conn.connect(host="127.0.0.1", port=3306,
                                  user="pyadmin", password="1234", database="studenti")
    cursor = connection.cursor(dictionary=True, buffered=True)
    if opcija == "student_id":
        cursor.execute("""SELECT * FROM student
                        WHERE student_id = %s;""", (unos_za_pretragu, ))
        result_set = cursor.fetchall()
        cursor.close()
    if opcija == "JMBG": 
        cursor.execute("""SELECT * FROM student
                        WHERE JMBG = %s;""", (unos_za_pretragu, ))
        result_set = cursor.fetchall()
        cursor.close()
    niz=[]
    if result_set:
        for i in result_set:
            niz.append(Author(**i))
        Button(window, text="Upload novu sliku", width=19, height=2, font="arial 13 bold", bg="lightblue", fg="black", command=show_image).place(x=1690, y=410)
        Button(window, text="Update podatke", width=19, height=2, font="arial 13 bold", bg="blue", fg="white",command=update).place(x=1690, y=500)
        Button(window, text="Sacuvaj u PDF", width=19, height=2, font="arial 13 bold", bg="green", fg="white", command=save_to_pdf).place(x=1690, y=580)
        Button(window, text="Obrisi", width=19, height=2, font="arial 13 bold", bg="red", fg="white", command=delete_student).place(x=1690, y=660)
        

    else:
        messagebox.showwarning("Ne postoji", "Ne postoji student sa datim podacima!")
    for niz in niz:
        img1=PhotoImage(file="img/upload_photo.png")
        lbl.config(image=img1)
        lbl.image=img1
        img=""
        Ime.set(niz.ime)
        Prezime.set(niz.prezime)
        Datum_rodjenja.set(niz.datum_rodjenja)
        JMBG.set(niz.JMBG)
        Telefon.set(niz.broj_telefona)
        G_O.set(niz.grad_opstina)
        Broj_poste.set(niz.postanski_broj)
        Region.set(niz.region)
        Ulica.set(niz.ulica)
        Broj_ulice.set(niz.broj_kuce)
        Ime_oca.set(niz.ime_oca)
        Ime_majke.set(niz.ime_majke)
        Zanimanje.set(niz.zanimanje_oca)
        Zanimanje_majke.set(niz.zanimanje_majke)
        Devojacko.set(niz.devojacko_prezime)
        Naziv_skole.set(niz.naziv_skole)
        Smer.set(niz.smer)
        Godina_upisa.set(niz.godina_upisa)
        Trajanje.set(niz.trajanje)
        Grad_skole.set(niz.grad_skole)
        stanje_oca.set(niz.radno_stanje_oca)
        stanje_majke.set(niz.radno_stanje_majke)
        stanje.set(niz.bracno_stanje)
        Vrsta_skole.set(niz.Vrsta_s)
        if niz.pol == "Muski":
            radio.set('1')
        else:
            radio.set('2')
        if niz.slika != None:
            img = (Image.open(f"{niz.slika}"))
            resized_image = img.resize((190,190))
            photo2 = ImageTk.PhotoImage(resized_image)
            lbl.config(image=photo2)
            lbl.image = photo2

        
def delete_student():
    unos_za_pretragu = Search.get()
    a = messagebox.askyesno("Da-Ne!","Da li zelite da obrisete studenta?")
    if a == True:
        connection = conn.connect(host="127.0.0.1", port=3306,
                                    user="pyadmin", password="1234", database="studenti")
        cursor = connection.cursor(dictionary=True, buffered=True)
        cursor.execute("""DELETE FROM student
                        WHERE student_id = %s;""", (unos_za_pretragu, ))
        rows_affected = cursor.rowcount
        connection.commit()
        cursor.close()
        if rows_affected>0:
                Ime.set('')
                Prezime.set('')
                Datum_rodjenja.set('')
                JMBG.set('')
                Telefon.set('')
                Broj_poste.set('')
                Ulica.set('')
                Broj_ulice.set('')
                G_O.set('')
                Region.set('')
                Ime_oca.set('')
                Ime_majke.set('')
                Zanimanje.set('')
                Zanimanje_majke.set('')
                Devojacko.set('')
                Naziv_skole.set('')
                Smer.set('')
                Godina_upisa.set('')
                Trajanje.set('')
                Grad_skole.set('')
                Search.set('')
                radio.set('0')
                stanje_oca.set('Izaberi opciju')
                stanje_majke.set('Izaberi opciju')
                stanje.set('Izaberi opciju')
                Vrsta_skole.set('Izaberi opciju')
                img1=PhotoImage(file="img/upload_photo.png")
                lbl.config(image=img1)
                lbl.image=img1
                img=""
                messagebox.showinfo("Info", "Uspesno ste obrisali studenta.")
    else:
        messagebox.showinfo("Info", "Niste obrisali studenta.")

def save_to_pdf():
    connection = conn.connect(host="127.0.0.1", port=3306,
                                  user="pyadmin", password="1234", database="studenti")
    ime = Ime.get()
    prezime = Prezime.get()
    datum_rodjenja = Datum_rodjenja.get()
    jmbg =  JMBG.get()
    broj_telefona = Telefon.get()
    grad_opstina = G_O.get()
    br_poste = Broj_poste.get()
    regija = Region.get()
    ulica = Ulica.get()
    br_kuce = Broj_ulice.get()   
    ime_oca = Ime_oca.get()
    zanimanje_oca = Zanimanje.get()
    ime_majke = Ime_majke.get()
    zanimanje_majke = Zanimanje_majke.get()
    dev = Devojacko.get()
    naziv_skole = Naziv_skole.get()
    smer = Smer.get()
    godina_upisa = Godina_upisa.get()
    trajanje = Trajanje.get()
    grad_skole = Grad_skole.get()
    pol = selection()
    radno_stanje_oca= stanje_oca.get()
    radno_stanje_majke = stanje_majke.get()
    bracno_stanje = stanje.get()
    Vrsta_s = Vrsta_skole.get()
    cursor = connection.cursor()
    cursor.execute("SELECT slika FROM student WHERE JMBG=%s;",(jmbg,))
    slika = cursor.fetchone()
    cursor.close()
    with open("./templates/primer1.jinja", "r", encoding="utf-8") as f:
        with open(f"./{slika[0]}", "rb") as img:
             imgb64 = base64.b64encode(img.read()).decode("utf-8")
        t = Template(f.read())
        pdf_name = "./izlaz/" + f"{ime} {prezime} {jmbg}.pdf"
        pdfkit.from_string(t.render(
            report_timestamp=str(datetime.strftime(datetime.now(),'%d.%m.%Y-%H:%M:%S')),
            ime = ime, prezime = prezime, datum_rodjenja = datum_rodjenja, jmbg = jmbg,
            broj_telefona = broj_telefona, grad_opstina = grad_opstina, br_poste = br_poste,
            regija = regija, ulica = ulica, br_kuce = br_kuce, ime_oca = ime_oca, zanimanje_oca = zanimanje_oca,
            ime_majke = ime_majke, zanimanje_majke = zanimanje_majke, dev = dev, naziv_skole = naziv_skole, 
            smer = smer, godina_upisa = godina_upisa, trajanje = trajanje, grad_skole = grad_skole, 
            pol = pol, radno_stanje_oca = radno_stanje_oca, radno_stanje_majke = radno_stanje_majke, bracno_stanje = bracno_stanje,
            Vrsta_s = Vrsta_s,
            company_logo=imgb64), pdf_name) 
    messagebox.showinfo("Uspesno", "Uspesno ste sacuvali PDF dokumenat.")

background = "#06283D"
framebg="#EDEDED"
framefg="#06283D"
default="arial 13"

window = customtkinter.CTk()
window.title("Student Registration System")
window.geometry("1710x750+210+100")
window.iconbitmap("iconica.ico")
window.config(bg=background)

Label(window, text="Email: resadspahovic94@gmail.com", width=10, height=3, bg="#f0687c", anchor="e").pack(side=TOP, fill=X)
Label(window, text="PRETRAGA STUDENATA PO:", width=10, height=2, bg="#c36464", fg="#fff", font="arial 20 bold").pack(side=TOP, fill=X)
pretraga = IntVar(value=1)
R11 = Radiobutton(window, text="INDEX", variable=pretraga, value=1, bg=framebg, fg=framefg, command=selection2, font="roboto 14")
R11.place(x=1170, y=68)
R22 = Radiobutton(window, text="JMBG", variable=pretraga, value=2, bg=framebg, fg=framefg, command=selection2, font="roboto 14")
R22.place(x=1260, y=68)

Search = StringVar()
Entry(window, textvariable=Search, width=15, bd=2, font="arial, 20").place(x=1350, y=65)
imageicon3 =  PhotoImage(file="img/search.png")
Srch = Button(window, image=imageicon3, width=50, height=39, bg="#68ddfa", command=Search_student)
Srch.place(x=1600, y=60)

imageicon4 = PhotoImage(file="img/back.png")
Update_button = Button(window, image=imageicon4, bg="#68ddfa",  width=50, height=39, command=vrati)
Update_button.place(x=410, y=60)

Label(window, text="Broj indexa:", font=default, fg=framebg, bg=background).place(x=30, y=150)
Label(window, text="Datum:", font=default, bg=background, fg=framebg).place(x=500, y=150)

Registration = StringVar()
Date = StringVar()

red_entry = Entry(window, textvariable=Registration, width=15, font=default)
red_entry.place(x=160, y=150)
Registration.set(reg_number())


today = date.today()
d1 = today.strftime("%d/%m/%Y")
date_entry = Entry(window, textvariable=Date, width=15, font=default)
date_entry.place(x=550, y=150)
Date.set(d1)

obj = LabelFrame(window, text="Podaci o studentu", font=20, bd=2, width=1630, bg=framebg, fg=framefg, height=350, relief=GROOVE)
obj.place(x=30, y=200)

Label(obj, text="Ime:", font=default, bg=framebg, fg=framefg).place(x=30, y=50)
Label(obj, text="Prezime:", font=default, bg=framebg, fg=framefg).place(x=30, y=100)
Label(obj, text="Pol:", font=default, bg=framebg, fg=framefg).place(x=30, y=150)
Label(obj, text="Datum rodjenja:", font=default, bg=framebg, fg=framefg).place(x=30, y=200)

Label(obj, text="JMBG:", font=default, bg=framebg, fg=framefg).place(x=500, y=50)
Label(obj, text="Broj telefona:", font=default, bg=framebg, fg=framefg).place(x=500, y=100)
Label(obj, text="Status:", font=default, bg=framebg, fg=framefg).place(x=500, y=150)
Label(obj, text="Grad/Opstina:", font=default, bg=framebg, fg=framefg).place(x=500, y=200)

Label(obj, text="Postanski broj:", font=default, bg=framebg, fg=framefg).place(x=970, y=50)
Label(obj, text="Region:", font=default, bg=framebg, fg=framefg).place(x=970, y=100)
Label(obj, text="Ulica:", font=default, bg=framebg, fg=framefg).place(x=970, y=150)
Label(obj, text="Broj kuce:", font=default, bg=framebg, fg=framefg).place(x=970, y=200)

Ime = StringVar()
ime_entry = Entry(obj, textvariable=Ime, width=20, font=default)
ime_entry.place(x=160, y=50)

Prezime = StringVar()
prezime_entry = Entry(obj, textvariable=Prezime, width=20, font=default)
prezime_entry.place(x=160, y=100)

radio = IntVar()
R1 = Radiobutton(obj, text="Muski", variable=radio, value=1, bg=framebg, fg=framefg, command=selection, font="roboto 11")
R1.place(x=150, y=150)
R2 = Radiobutton(obj, text="Zenski", variable=radio, value=2, bg=framebg, fg=framefg, command=selection, font="roboto 11")
R2.place(x=220, y=150)

Datum_rodjenja = StringVar()
datum_rodjenja_entry = Entry(obj, textvariable=Datum_rodjenja, width=20, font=default)
datum_rodjenja_entry.place(x=160, y=200)

JMBG = StringVar()
jmbg_entry = Entry(obj, textvariable=JMBG, width=20, font=default)
jmbg_entry.place(x=630, y=50)

Telefon = StringVar()
telefon_entry = Entry(obj, textvariable=Telefon, width=20, font=default)
telefon_entry.place(x=630, y=100)

s = (' Ozenjen/Udata',  
                          'Neozenjen/Neudata', 
                          ' Udovci/Udovice', 
                          ' Razveden/a', 
                          ' Ostalo') 
Status = StringVar()
stanje = ttk.Combobox(obj, width = 20, textvariable = Status, values=s, font="roboto 11") 
stanje.place(x=630, y=150)
stanje.set("Izaberi opciju")

G_O = StringVar()
opstina_entry = Entry(obj, textvariable=G_O, width=20, font=default)
opstina_entry.place(x=630, y=200)
gl.GlobalComponents.set("opstina_entry", opstina_entry)
imageicon5 = PhotoImage(file="img/true.png")
button = Button(obj, image=imageicon5, bg="#68ddfa",  width=30, height=25, command=upis)
button.place(x=835, y=197)

Broj_poste = StringVar()
broj_poste_entry = Entry(obj, textvariable=Broj_poste, width=20, font=default)
broj_poste_entry.configure(state='normal')
broj_poste_entry.place(x=1150, y=50)

Region = StringVar()
Region_entry = Entry(obj, textvariable=Region, width=20, font=default)
Region_entry.place(x=1150, y=100)

Ulica = StringVar()
ulica_entry = Entry(obj, textvariable=Ulica, width=20, font=default)
ulica_entry.place(x=1150, y=150)

Broj_ulice = StringVar()
broj_ulice_entry = Entry(obj, textvariable=Broj_ulice, width=20, font=default)
broj_ulice_entry.place(x=1150, y=200)


obj2 = LabelFrame(window, text="Podaci o roditeljima", font=20, bd=2, width=1630, bg=framebg, fg=framefg, height=280, relief=GROOVE)
obj2.place(x=30, y=500)

Label(obj2, text="Ime oca:", font=default, bg=framebg, fg=framefg).place(x=30, y=50)
Label(obj2, text="Zanimanje:", font=default, bg=framebg, fg=framefg).place(x=30, y=100)
Label(obj2, text="Radni odnos:", font=default, bg=framebg, fg=framefg).place(x=30, y=150)

Label(obj2, text="Ime majke:", font=default, bg=framebg, fg=framefg).place(x=500, y=50)
Label(obj2, text="Zanimanje:", font=default, bg=framebg, fg=framefg).place(x=500, y=100)
Label(obj2, text="Radni odnos:", font=default, bg=framebg, fg=framefg).place(x=500, y=150)

Label(obj2, text="Dev. prezime majke:", font=default, bg=framebg, fg=framefg).place(x=970, y=50)

Ime_oca = StringVar()
ime_oca_entry = Entry(obj2, textvariable=Ime_oca, width=20, font=default)
ime_oca_entry.place(x=160, y=50)

Zanimanje = StringVar()
zanimanje_entry = Entry(obj2, textvariable=Zanimanje, width=20, font=default)
zanimanje_entry.place(x=160, y=100)

stanje_o = (' Zaposlen',  
                          'Nezaposlen', 
                          ' Rad na odredjeno', 
                          ' Privatnik/Preduzetnik', 
                          ' Ostalo') 
R_O_Oca = StringVar()
stanje_oca = ttk.Combobox(obj2, width = 20, textvariable = R_O_Oca, values=stanje_o, font="roboto 11") 
stanje_oca.place(x=160, y=150)
stanje_oca.set("Izaberi opciju")

Ime_majke = StringVar()
ime_majke_entry = Entry(obj2, textvariable=Ime_majke, width=20, font=default)
ime_majke_entry.place(x=630, y=50)

Zanimanje_majke = StringVar()
zanimanje_majke_entry = Entry(obj2, textvariable=Zanimanje_majke, width=20, font=default)
zanimanje_majke_entry.place(x=630, y=100)


stanje_m = (' Zaposlena',  
                          'Nezaposlena', 
                          ' Rad na odredjeno', 
                          ' Privatkin/Preduzetnik', 
                          ' Ostalo') 
R_O_Majke = StringVar()
stanje_majke = ttk.Combobox(obj2, width = 20, textvariable = R_O_Majke, values=stanje_m, font="roboto 11") 
stanje_majke.place(x=630, y=150)
stanje_majke.set("Izaberi opciju")

Devojacko = StringVar()
devojacko_entry = Entry(obj2, textvariable=Devojacko, width=20, font=default)
devojacko_entry.place(x=1150, y=50)

obj3 = LabelFrame(window, text="Podaci o srednjem obrazovanju", font=20, bd=2, width=1630, bg=framebg, fg=framefg, height=235, relief=GROOVE)
obj3.place(x=30, y=745)

Label(obj3, text="Tacan naziv sk.:", font=default, bg=framebg, fg=framefg).place(x=30, y=50)
Label(obj3, text="Vrsta skole:", font=default, bg=framebg, fg=framefg).place(x=30, y=100)

Label(obj3, text="Smer:", font=default, bg=framebg, fg=framefg).place(x=500, y=50)
Label(obj3, text="Godina upisa:", font=default, bg=framebg, fg=framefg).place(x=500, y=100)

Label(obj3, text="Trajanje skole:", font=default, bg=framebg, fg=framefg).place(x=970, y=50)
Label(obj3, text="Grad/Opstina:", font=default, bg=framebg, fg=framefg).place(x=970, y=100)


Naziv_skole = StringVar()
naziv_entry = Entry(obj3, textvariable=Naziv_skole, width=20, font=default)
naziv_entry.place(x=160, y=50)

vrsta = ('Gimnazija', ' Masinska', ' Ekonomska', ' Tehnicka','Tekstilna','Ugostiteljska','Medicinska','Drugo') 
Vrsta_skole = StringVar()
Vrsta_skole = ttk.Combobox(obj3, width = 20, textvariable = Vrsta_skole, values=vrsta, font="roboto 11") 
Vrsta_skole.place(x=160, y=100)
Vrsta_skole.set("Izaberi opciju")

Smer = StringVar()
smer_entry = Entry(obj3, textvariable=Smer, width=20, font=default)
smer_entry.place(x=630, y=50)

Godina_upisa = StringVar()
godina_upisa_entry = Entry(obj3, textvariable=Godina_upisa, width=20, font=default)
godina_upisa_entry.place(x=630, y=100)

Trajanje = StringVar()
trajanje_entry = Entry(obj3, textvariable=Trajanje, width=8, font=default)
trajanje_entry.place(x=1150, y=50)

Grad_skole = StringVar()
grad_skole_entry = Entry(obj3, textvariable=Grad_skole, width=20, font=default)
grad_skole_entry.place(x=1150, y=100)


f = Frame(window, bd=3, bg="white",  width=200, height=200, relief=GROOVE)
f.place(x=1690, y=200)
img = PhotoImage(file="img/upload_photo.png")
lbl = Label(f, bg="lightblue", image=img)
lbl.place(x=0, y=0)

Button(window, text="Upload Sliku", width=19, height=2, font="arial 13 bold", bg="lightblue", fg="black", command=show_image).place(x=1690, y=410)
Button(window, text="Sacuvaj", width=19, height=2, font="arial 13 bold", bg="lightgreen", fg="black",  command=Save).place(x=1690, y=500)
Button(window, text="Resetuj", width=19, height=2, font="arial 13 bold", bg="lightpink",fg="black", command=Clear).place(x=1690, y=580)
Button(window, text="Izadji", width=19, height=2, font="arial 13 bold", bg="grey", fg="black", command=Exit).place(x=1690, y=660)


if __name__=="__main__":
    window.mainloop()
