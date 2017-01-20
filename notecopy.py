#!/usr/bin/env python
import os, shutil, time, webbrowser, glob

# Made by Mark Schultz for automating
# uploading notes after class.

def find_ext(dr, ext):
    return glob.glob(os.path.join(dr, "*." + ext))
# Returns all files of a given extension in the folder.

def prepareNotes(course):
    # Copies the .pdf of notes from my LaTeX folder to the
    # NoteTaking folder, renames it to the proper format,
    # And opens Moodle to the right page to make it easy to
    # upload.

    ## Find highest number in a .pdf file, e.g. 23 in /year3/real/Real23.pdf
    beginning = "/home/mark/latex/year3/"
    src = os.path.join(beginning,course[1].lower())
    pdfs = find_ext(src,"pdf")  ## Finds all .pdfs in /year3/coursename/ folder
    lenCut = len(beginning)
    ## Removes /home/mark/latex/year3/ from filepath of each .pdf
    ##
    for val in pdfs:
        val = val[lenCut+1:]
    maximum = -1
    maximumindex = -1
    outputPdfs = pdfs[:]
    ## Iterates through all the RealXX.pdf names, finds the highest XX
    i = 0
    while i < len(pdfs):
        pdfs[i] = ''.join([c for c in pdfs[i] if c in '1234567890'])
        if int(pdfs[i])>maximum:
            maximum = int(pdfs[i])
            maximumindex = i
        i += 1
    fileToCopy = outputPdfs[maximumindex]
    ## Gets the absolute filepath of the file
    src = os.path.join(src,fileToCopy)
    dst = "/home/mark/Desktop/Notetaking/"
    ## Formats the date correctly for renaming
    date = time.strftime("%x").lstrip("0").replace("/","-")
    ## Renames the file in the format desired
    filename = course[0]+" Notes "+date+".pdf"
    shutil.copy(fileToCopy,dst+os.sep+filename)
    ## Open moodle page for uploading the notes
    webbrowser.open_new("https://moodle.reed.edu/"+course[2])
    ## Open the GUI file browser where the notes get copied to temporarily
    webbrowser.open('/home/mark/Desktop/Notetaking')
    ## Timer Section
    ## For copying the notes to the archive folder
    timeToExit = 20
    time.sleep(2)
    timeToExit -= 2
    print("Time remaining:")
    while timeToExit>0:
        if timeToExit % 2 == 0:
            print(timeToExit)
        time.sleep(1)
        timeToExit -= 1
    shutil.move(dst+os.sep+filename,dst+os.sep+course[1]+os.sep+filename)
    print("File moved")
    print("Safe to Close")
def chooseClass(classes):
    # Asks which course to apply prepareNotes to
    # if there are multiple courses.
    if len(classes) == 1:
        choice = 0
    else:
        i = 0
        print("Which class are the Notes For?")
        while i < len(classes):
            print(str(i+1)+" - "+classes[i][1])
            i += 1
        choice = int(input("Choose: "))
        choice = choice - 1
    return prepareNotes(classes[choice])

# Put lists for classes here
Real = ["MTH 321","Real","mod/data/view.php?id=40252"]

# Assemble the classes together and sort by title (e.g. "Real")
classes = []
classes.append(Real)
classes.sort(key = lambda x: x[1])

# Actually run things here
chooseClass(classes)
