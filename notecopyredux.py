import time
import os
import glob
import shutil
import webbrowser
import atexit
import subprocess
import sys
import re

FILE_PATHS = ["/home/mark/classes/Sp17/", "-Spring-2017/notes/"]
DEST_PATH = "/home/mark/Desktop/Notetaking/"
EXTRACT_DIGITS_RE = re.compile(r"\d+")
DATE_FROM_TEX_RE = re.compile("\\lec\{(\d+)/(\d+)\}")


def find_ext(dr, ext):
    """
    Return a list of all files with a given file extension in a folder.
    """
    return glob.glob(os.path.join(dr, "*." + ext))


def move_renamed_file(old_file_path, new_file_path):
    """
    Should move the staged .pdf to an "archive" folder on exit.
    """
    shutil.move(old_file_path, new_file_path)


def get_number_in_string(string, default=-1):
    """
    Given a string that contains a number, returns that number.

    String expected to be of the form <word>XY.pdf, where <word> contains no numbers.

    """
    find = EXTRACT_DIGITS_RE.search(string)
    if find is None:
        return default
    else:
        return int(find.group())


class Course:

    def __init__(self, class_name, class_schedule, subject, course_number, moodle_id):
        self.directory = "".join([FILE_PATHS[0], class_name, FILE_PATHS[1]])
        self.class_schedule = class_schedule
        self.subject = subject
        self.course_number = str(course_number)
        self.moodle_id = str(moodle_id)

    def make_new_name(self, date=None):
        """
        Makes a new name of form SUBJ NUM MM-DD-YYYY.pdf, where SUBJ is the department the class is in (i.e. MATH), NUM is the three-digit class number, and MM-DD-YYYY is the most recent date.
        """
        if date is None:
            date = time.strftime("%x")
        formatted_date = date.lstrip("0").replace("/", "-")
        return "".join([self.subject, " ", self.course_number, " ", formatted_date, ".pdf"])

    def find_highest_pdf(self):
        """
        Finds the .pdf with file name containing the highest number in the directory.
        """
        pdfs = find_ext(self.directory, "pdf")
        last_backslash = pdfs[0].rfind("/")
        for num in range(len(pdfs)):
            pdfs[num] = pdfs[num][last_backslash + 1:]
        pdfs.sort(key=get_number_in_string)
        self.target_pdf = pdfs[-1]
        return "".join([self.directory, self.target_pdf])

    def find_tex_from_pdf(self, pdf_directory):
        """
        Given a file-path to a .pdf file, returns the .tex file corresponding to it.
        """
        return pdf_directory.split('.')[0] + '.tex'

    def get_date_from_tex(self, tex):
        """
        Given a file-path to a .tex file, opens it and looks for \lec{A/BC}, which is the date it was written.

        Returns MM/DD/YYYY
        """
        with open(tex, 'r') as f:
            string = f.read()
        date = DATE_FROM_TEX_RE.search(string).groups()
        return "/".join([date[0].zfill(2), date[1], time.strftime("%Y")])

    def move_file(self, file_name, date):
        """
        Takes a file, renames it, and moves it to the "staging" folder.
        """
        new_file_name = self.make_new_name(date)
        dest = os.path.join(DEST_PATH, new_file_name)
        shutil.copy(file_name, dest)

    def open_browser(self):
        """
        Opens the webpage and "staging" folder to allow drag and drop of the .pdf to the website.
        """
        webbrowser.open_new(
            "".join(["https://moodle.reed.edu/mod/data/view.php?id=", self.moodle_id]))
        subprocess.Popen(["xdg-open", DEST_PATH])

    def upload_notes(self):
        """
        Runs all the prior functions in the right order.
        """
        pdf = self.find_highest_pdf()
        tex = self.find_tex_from_pdf(pdf)
        date = self.get_date_from_tex(tex)
        new_file_name = self.make_new_name(date)
        self.move_file(pdf, date)
        self.open_browser()
        atexit.register(move_renamed_file, "".join([DEST_PATH, new_file_name]), "".join(
            [DEST_PATH, self.course_number, " archive/", new_file_name]))
        input("Press any key to exit")
        sys.exit()


if __name__ == "__main__":
    crypto = Course("cryptography", "MWF", "MATH", 388, 51406)
    crypto.upload_notes()
