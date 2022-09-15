# Moodle Photo Flashcards

This library is designed to provide photo flashcards and an interactive name quiz to help you learn student names. The tools here are written in Python, and have the following dependencies:

- numpy
- tkinter
- matplotlib
- pandas
- mediapipe

Once these are installed (which can be done using pip), you simply do the following:

- Navigate to your course Moodle Page, and from the hamburger menu in the top left, select "Photo Roster"
- Use the Role filter to select "Student AC", and change Display mode to "Printable"
- Save this page to your local computer, into the directory containing this repo (ctrl+S, should be a .html file and an associated folder that contains the student photos)
- From within the folder that contains the html file, run the "ApplyMasks_and_ParseMoodle.py" script, using `python3 ApplyMasks_and_ParseMoodle.py [datadir_name]`. The final argument should be the name of the folder that contains the student images. If the folder has a space in its name, it behooves you to rename the folder to something simple (like "photos").
- Now you should be ready to run either `python3 MakeFlashcards.py` or `python3 MakeQuiz.py` to help you learn the student names!

![](https://github.com/Moodle_StudentPhoto_Flashcards/Example_NameQuiz.gif)
