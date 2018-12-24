# coding:utf-8
########################################################################################################################
####################################################GUI for FRA#########################################################
########################################################################################################################
# Developed by Cihan Ruan 2016.12.15
# Improved by 2017.9.14

# Modified by Zhaopeng Zhang 2018.04.17
# merge """GUI.py, lib_win_gui, icon.ico, limit.GIF, Welcome.gif""" into FRA program.
# this script is needed only when you want to get GUI.exe using pyinstaller in windows platform.

import Tkinter as tk
from tkFileDialog import askopenfilename
from tkFileDialog import asksaveasfilename
import tkFileDialog as fd
from Tkinter import IntVar
import ttk
import tkMessageBox
from Tkinter import Menu
import fra
import sys
import os
from lib_win_gui.startfile import start as startfile
import webbrowser
from lib_win_gui import PMOnlineQuery
from tkMessageBox import showerror

if __name__ == '__main__':
    PATH2 = os.path.dirname(os.path.realpath(__file__))

    # New Edition
    window = tk.Tk()
    window.title('Welcome to FRA algorithm')
    # window.iconbitmap('icon.ico')
    window.wm_resizable(width=False, height=False)
    window.minsize(1040, 760)
    window.maxsize(1040, 760)

    # Welcome image
    canvas = tk.Canvas(window, height=200, width=1100)
    image_file = tk.PhotoImage(file=os.path.join(PATH2, 'Welcome.gif'))
    image = canvas.create_image(0, 0, anchor='nw', image=image_file)
    canvas.pack(side='top')

    # Menubar
    menubar = Menu(window)

    def limit_dl():
        startfile('limit.GIF')

    fmenu = Menu(menubar, tearoff=0)
    # fmenu.add_command(label="Requirements", command=window.quit)
    # fmenu.add_command(
    #     label="How to use",
    #     command=startfile(os.path.join(PATH2, "README.txt")))
    fmenu.add_command(label="PubMed Download Limitation", command=limit_dl)
    fmenu.add_separator()
    fmenu.add_command(label="Exit", command=window.quit)
    menubar.add_cascade(label="Help", menu=fmenu)

    def versionInfo():
        tkMessageBox.showinfo(
            "Version Info", "Fast Review Algorithm GUI Version 1.3 \n\n"
            "Developed by Cihan Ruan, Zhaopeng Zhang, Wei Zheng, Qiqige Wuyun, Jishou Ruan\n"
            "Department of Mathmatics, Nankai University\n"
            "All right reserved")

    def contactInfo():
        tkMessageBox.showinfo(
            "Contact us",
            "Please contact us by visiting https://mathbio.nankai.edu.cn/fra/ \nOr mail to xxx@mail.com \nThank you!"
        )

    def declaimer():
        tkMessageBox.showinfo(
            "Declaimer", 'FRA Software is for research purposes only.\n \n'
            'We reserve the right to make changes in the software without notification. \n \n'
            'We also make no representation or warranty that such application will be suitable for the specified use without further testing or modification.\n \n'
            'When using the brief search function, please read the limitation document and consciously comply with the relevant regulations'
        )

    vmenu = Menu(menubar, tearoff=0)
    vmenu.add_command(label="Declaimer", command=declaimer)
    vmenu.add_command(label="Verision Info", command=versionInfo)
    vmenu.add_command(label="Contact Us", command=contactInfo)
    menubar.add_cascade(label='About', menu=vmenu)
    window['menu'] = menubar

    ###########################################Part1: DOWNLOAD#############################################
    tk.Label(
        window,
        text=
        'To continue this data analysis process,\nyou need the query result of keywords you want from \nPubMed Database in .txt format and MEDLINE format.',
        font=("Verdana 12"),
        fg='#067a64',
        justify='left').place(
            x=20, y=220)

    def openEg():
        examplefile = os.path.join(PATH2, 'test/pubmed_result.txt')
        startfile(examplefile)

    eg_btn = tk.Button(
        window,
        width=15,
        bg='#526370',
        fg='white',
        text="View Example",
        font=("Verdana 10 bold"),
        command=openEg)
    eg_btn.pack()
    eg_btn.place(x=335, y=285)
    tk.Label(
        window,
        text='You could get the target data file in two ways',
        font=("Verdana 11 italic"),
        fg='black',
        justify='center').place(
            x=20, y=320)

    # -----------------------------------------Method 1: Query here----------------------------------------#
    tk.Label(
        window, text='Brief Search', font=("Verdana 12 bold"),
        fg='black').place(
            x=20, y=350)

    resultNo = IntVar()
    keyWord = vars()
    email = vars()

    #   PMOnlineQuery.queryOnline(max_count, TERM, mailAd)
    #   max_count = resultNo
    #   TERM= keyWord
    #   mailAd = email

    tk.Label(
        window, text='Email Address:', font=("Verdana 11"), fg='black').place(
            x=20, y=380)
    emailAdEn = tk.Entry(window, width=30, bg='#F5FFFA')
    emailAdEn.pack()
    emailAdEn.place(x=140, y=380)

    tk.Label(
        window, text='Keyword:', font=("Verdana 11"), fg='black').place(
            x=20, y=420)
    query_keyword = tk.Entry(window, width=30, bg='#F5FFFA')
    query_keyword.pack()
    query_keyword.place(x=140, y=420)

    query_result = tk.Label(
        window,
        height=4,
        width=56,
        text="No searching result.",
        font=("Verdana 10 italic"),
        bg='#F5FFFA',
        fg='#067a64')
    query_result.pack()
    query_result.place(x=20, y=490)

    limitNo = 1000
    tk.Label(
        window, text='Choose the first', font=("Verdana 11"),
        fg='black').place(
            x=20, y=455)
    tk.Label(
        window, text='publications', font=("Verdana 11"), fg='black').place(
            x=225, y=455)
    downloadNo = tk.Entry(window, width=8, bg='#F5FFFA')
    downloadNo.pack()
    downloadNo.place(x=160, y=457)

    def goQuery():

        if not emailAdEn.get():
            tkMessageBox.showerror(
                title="Need email address",
                message="Please enter a valid email address for further search."
            )
        elif not query_keyword.get():
            tkMessageBox.showerror(
                title="Need keyword",
                message="Please enter keywords to search.")
        else:
            keyWord = query_keyword.get()
            PMOnlineQuery.TERM = keyWord
            email = emailAdEn.get()
            PMOnlineQuery.mailAd = email
            print(keyWord)
            print(email)
            resultNo = downloadNo.get()

            if not downloadNo.get():
                tkMessageBox.showerror(
                    title="Incomplete Information",
                    message="Please input how many query result you want.")
            elif resultNo.isdigit():
                resultNo = int(resultNo)
                print(resultNo)
                if resultNo < 0 or resultNo > limitNo:
                    tkMessageBox.showerror(
                        title="Error",
                        message=
                        "Please enter a positive value no more than limitation\n(Please check the requirement)"
                    )
                elif resultNo > 0 and resultNo < limitNo:
                    print "It works!"
                    query_result["text"] = "Start searching!\n"\
                    "Please wait...\n" \
                    "Do not close this process until you see next command."
                    window.update_idletasks()
                    PMOnlineQuery.max_count = resultNo
                    PMOnlineQuery.queryOnline2(
                        PMOnlineQuery.max_count, PMOnlineQuery.TERM,
                        PMOnlineQuery.mailAd, window, query_result)

            else:
                print "Input is not an integer"
                tkMessageBox.showerror(
                    title="Input must be integer",
                    message="Please enter a valid integer.")

    query_btn = tk.Button(
        window,
        bg='#03caa8',
        height=5,
        width=8,
        fg='white',
        font=("Verdana 10 bold"),
        text='Search',
        command=goQuery)
    query_btn.pack()
    query_btn.place(x=400, y=375)

    def goDownload():
        options = {}
        options['filetypes'] = [('text files', '.txt')]
        saveFilePath = fd.asksaveasfilename(**options) + ".txt"
        print("saveFilename=" + saveFilePath)
        saveFile = open(saveFilePath, mode='w')  #defaultextension='.txt'
        #                    if saveFilename is None:
        #                        tkMessageBox.showwarning("Sorry", "Your query result has been downloaded to")#asksaveasfile return 'None' if dialog closed with "cancel".
        #                        print ("saveFile is None")
        #                        return
        #                    else:
        write_content = PMOnlineQuery.resultContent
        try:
            if not write_content.strip():
                tkMessageBox.showerror(
                    "Oops!",
                    "It seems that there is no research result could be downloaded, please redo the search."
                )
            else:
                saveFile.write(write_content)  #Input content
                #saveFile.write(content.rstrip())
                tkMessageBox.showinfo(
                    "Successful",
                    "Your query result has been downloaded as " + saveFilePath)
                saveFile.close()
        except:
            tkMessageBox.showerror(
                title="Oops!",
                message="Unable to save file,please try search again.")

    download_btn = tk.Button(
        window,
        width=20,
        height=2,
        bg='#03caa8',
        fg='white',
        text='DOWNLOAD!',
        font=("Verdana 10 bold"),
        command=goDownload)
    download_btn.pack()
    download_btn.place(x=160, y=570)

    #-----------------------------------------Method 2: Query Online--------------------------------------#
    tk.Label(
        window,
        text='Complete Search',
        font=("Verdana 12 bold"),
        fg='black',
        justify='left').place(
            x=20, y=625)

    def openIntroImg():
        startfile('download.jpg')

    intro_pic = tk.Button(
        window,
        width=20,
        height=2,
        bg='#03caa8',
        fg='white',
        font=("Verdana 10 bold"),
        text="Check Introduction",
        command=openIntroImg)
    intro_pic.pack()
    intro_pic.place(x=290, y=665)

    url = 'https://www.ncbi.nlm.nih.gov/pubmed/'

    def openPM():
        webbrowser.open_new(url)

    open_PM = tk.Button(
        window,
        width=20,
        height=2,
        bg='#03caa8',
        fg='white',
        font=("Verdana 10 bold"),
        text='Go to PubMed',
        command=openPM)
    open_PM.pack()
    open_PM.place(x=25, y=665)

    #######################################Dividing Line###################################################
    line = tk.Canvas(window, width=8, height=800)
    bg_Image = tk.PhotoImage(file=os.path.join(PATH2, 'line.gif'))
    image2 = line.create_image(0, 150, anchor='center', image=bg_Image)
    line.pack(side='top')
    ######################################################################################################

    # SHOW Status
    #   tk.Label(window, text='FRA Data Analysis Process', font=('Verdana 11 italic')).place(x=560, y=285)
    data_pcs = tk.Label(
        window,
        text="When you are ready,\nclick the ACTION! button for processing.",
        font=('Verdana', 10, 'italic'),
        fg='#346392',
        width=56,
        height=9,
        bg='#F0FFFF')
    data_pcs.place(x=560, y=455)

    #filename = tk.StringVar()
    filetext = 'Your target file is here'
    foldertext = 'Your target folder is here'
    #PathStart="C:\\Users\\hp\\Desktop\\asthma\\"

    ##################Select file source file##########################
    #Select target folder
    tk.Label(
        window,
        text=
        'After you get the target .txt file,\nyou could select it and get the relevant data analysis.\n',
        font=("Verdana 12"),
        fg='#346392',
        justify='left').place(
            x=560, y=220)

    tk.Label(
        window,
        text='Select the data source file(txt format):',
        font=('Verdana 12')).place(
            x=560, y=315)

    ################################Original Function openFolder#######################################
    #   def openFolder():
    #       global folderName
    #       folderName = fd.askdirectory( ) ## filename not filehandle
    #       selected_folder["text"]= str(folderName) if  folderName else foldertext
    #       #PathStart = folderName + "/"
    #       #print PathStart
    #      # file_btn["text"]= str(filename) if filename else filetext

    #   selected_folder = tk.Label(window, text=filetext, font ="Verdana 10 italic", fg='#346392', width = 35, bg='#F0FFFF', height=1)
    #   selected_folder.place(x=560, y=349)

    #   folder_btn=tk.Button(window,width=8,text="Select...",bg='#59ace3',fg = 'white',font=("Verdana 10 bold"), command= openFolder)
    #   folder_btn.pack()
    #   folder_btn.place(x=850, y=346)

    #    def copyPath():
    #        global PathStart
    #        PathStart=folderName + "/"
    #        print PathStart


    def openFile():
        global fileName
        global folderName
        global PathStart

        fileName = askopenfilename(
            parent=window,
            initialdir=PATH2,
            filetypes=[("Text files", "*.txt")])
        selected_file["text"] = str(fileName)
        folderName = os.path.split(fileName)[0]
        PathStart = folderName + "/"

    ######################################################################################################
    database_ch = ""
    selected_file = tk.Label(
        window,
        text=filetext,
        font="Verdana 10 italic",
        fg='#346392',
        width=45,
        bg='#F0FFFF',
        height=1)
    selected_file.place(x=560, y=349)

    file_btn = tk.Button(
        window,
        width=8,
        text="Select...",
        bg='#59ace3',
        fg='white',
        font=("Verdana 10 bold"),
        command=openFile)
    file_btn.pack()
    file_btn.place(x=935, y=346)
    
    
    def go(*args):
        global database_ch
        database_ch = database_choice.get()

    comvalue=tk.StringVar()
    database_choice = ttk.Combobox(
        window,
        textvariable=comvalue
        )
    database_choice.pack()
    database_choice.place(x=650, y=400)
    database_choice["values"]=("proteins", "diseases")
    database_choice.current(0)  #选择第一个
    database_choice.bind("<<ComboboxSelected>>", go)
    

    def mainloop():
        #  global saveFolder
        #  saveFolder = fd.askdirectory( ) ## filename not filehandle
        #  savePathStart = saveFolder + "/"
        #  print savePathStart

        ######## STEP 1 pubmed.py############
        texts = "run FRA, please wait ... "
        data_pcs["text"] = str(texts)
        window.update_idletasks()
        inputfile = fileName
        outdir = os.path.join(os.path.dirname(inputfile), "FRA")
        print "inputfile: {}".format(inputfile)
        print "PATH: {}".format(PATH2)
        print "outdir: {}".format(outdir)
        fra.run(PATH2, inputfile, outdir, database=database_ch+".txt")
        ########  END   ########
        texts = "end!\nClick the Check Result button to show the result."
        data_pcs["text"] = str(texts)
        window.update_idletasks()

    #Finished
    folder_btn1 = tk.Button(
        window,
        width=20,
        height=2,
        text="ACTION!",
        bg='#59ace3',
        fg='white',
        font=("Verdana 10 bold"),
        command=mainloop)
    folder_btn1.pack()
    folder_btn1.place(x=690, y=622)

    def openResultFolder():
        if not folderName:
            tkMessageBox.showerror(
                title="No results!",
                message=
                "No results exit!\nPlease try it over from the very beginning."
            )
        else:
            webbrowser.open_new(folderName)

    folder_btn4 = tk.Button(
        window,
        width=20,
        height=2,
        text="Check Results",
        bg='#59ace3',
        fg='white',
        font=("Verdana 10 bold"),
        command=openResultFolder)
    folder_btn4.pack()
    folder_btn4.place(x=690, y=665)

    window.mainloop()
