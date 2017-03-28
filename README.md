# moodle-notetaking-uploader
Small python script made to assist with taking notes at Reed College.

The script will:

1. Find the most recent .pdf file (assuming it's named ClassName(#number), i.e. Real36).

2. Preform a regex search over the corresponding .tex file to find the date (I store it as \lec{M/DD})

2. Copy it to a "staging directory", open that directory in a graphical file explorer.

3. Open the correct webpage for the class that you're taking notes for (to allow you to "drag and drop" from the graphical file explorer to the webpage).

4. Upon entering any input on the terminal, it will move the "staged" file to an archive subfolder of the staging directory.

A lot of the things here (where the recent .pdf's are stored, where the staging directory is, the correct webpage is) is hard-coded.  Nevertheless, it allows uploading my notes to be a ~10 second process.
