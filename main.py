# SQLite is used for database
import sqlite3
from sqlite3 import Error
# Sys is used for accessing files (.txt and .png files)
import sys
# PIL is used to view PNG images
from PIL import Image
# fpdf is used to export papers into PDFs
from fpdf import FPDF
# Used to convert pdf files to docx files
from pdf2docx import Converter
# Used to remove unwanted files
import os

class menu:
    def __init__(self):
        self.option = 1
        # Loops until the user decides to exit
        while self.option != 0:
            try:
                self.option = int(input('''MENU
            
Create:
1. Create a new paper
2. Edit a paper
3. Remove a paper

Analyse:
4. Add/Edit Marks
5. Analyse
6. Add/remove a class/student

0. Exit

Please select an option: '''))
            except:
                print()
                print('That is not a valid option 2')
                print()
            else:
                # Creating a new paper
                if self.option == 1:
                    name = None
                    while name == None:
                        name = input('What would you like to name this paper? ')
                        # Checks if the name already exists
                        if name in data.getNames():
                            print('A paper with that name already exists')
                            print()
                            name = None
                    # If the name does not already exist, the paper is created, added to the database and edit mode is loaded
                    current_paper = paper(name, data.generateID())
                    current_paper.addPaper()
                    current_paper.editPaper()
                    print()
                # Editting an existing paper
                elif self.option == 2:
                    papers = data.getPapers()
                    option = None
                    # Choosing which paper to edit
                    while option is None:
                        try:
                            print()
                            print('Please choose a paper:')
                            print()
                            for x in papers:
                                print(str(x[0]) + '. ' + x[1])
                            print()
                            option = int(input(''))
                            current_paper = paper(papers[option][1], option)
                            current_paper.initialiseQuestions()
                            current_paper.editPaper()
                        except ValueError:
                            print()
                            print('That is not a valid option 3')
                            option = None
                    print()
                elif self.option == 3:
                    # Remove a paper
                    papers = data.getPapers()
                    option = None
                    # Choosing which paper to remove
                    while option is None:
                        try:
                            print()
                            print('Please choose a paper to remove:')
                            print()
                            num = 0
                            for x in papers:
                                print(str(x[0]+1) + '. ' + x[1])
                                num += 1
                            print('0. Go back')
                            print()
                            option = int(input(''))
                            if option > 0 and option <= num:
                                # REMOVE THE PAPER
                                print()
                                print('Are you sure you would like to remove this paper?')
                                confirmation = input('Type "YES" to confirm: ')
                                if confirmation == 'YES':
                                    ID = papers[option-1][0]
                                    data.removePaper(ID)
                                    data.save()
                                    papers.remove(papers[option-1])
                                    print('Removed')
                                print()
                            elif option != 0:
                                print('That is not a valid option')
                                option == None
                        except ValueError:
                            print()
                            print('That is not a valid option ')
                            option = None
                    print()
                elif self.option == 4:
                    ##########################
                    # Add/Edit marks
                    classes = data.getClasses()
                    for x in classes:
                        print(str(x[0]) + '. ' + x[1])
                    print('0. Go back')
                    print()
                    
                    ##########################
                    print()
                elif self.option == 5:
                    ##########################

                    # Analyse

                    ##########################
                    print()
                elif self.option == 6:
                    ##########################

                    #Add/remove a class/student

                    ###########################
                    print()
                elif self.option != 0:
                    print('That is not a valid option 4')
                    print()

# Class to manage the database
# For program to work database must be stored in the same folder as the program and must be named "database.db"
class database:
    # Initiates the SQLite database by attempting to establish a connection
    def __init__(self, path):
        self.path = path
        self.connection = None
        try:
            self.connection = sqlite3.connect(path)
        except Error as e:
            print(f"The error '{e}' occured")
    
    # This method allows us to run SQL querys on the databse
    def execute_read_query(self, query):
        # The cursor allows us to input the SQL querys
        cursor = self.connection.cursor()
        result = None
        # Attempts to execute the query and return the result
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"The error '{e}' occurred")

    # Saves the database by commiting all changes
    def save(self):
        self.connection.commit()
        #Connection to the databse is re-establised after commiting changes
        self.__init__(self.path)

    # Returns all papers sorted by ID
    def getPapers(self):
        return self.execute_read_query('SELECT * FROM Papers ORDER BY PaperID')

    # Adds a new paper into the database
    def addPaper(self, name, ID):
        self.execute_read_query("INSERT INTO Papers VALUES (" + str(ID) + ", '" + name + "');")

    def removePaper(self,ID):
        self.execute_read_query("DELETE FROM Papers WHERE PaperID=" + str(ID))

    # Returns the lowest unused PaperID
    def generateID(self):
        currentID = 0
        while currentID in [i[0] for i in self.execute_read_query('SELECT PaperID FROM Papers')]:
            currentID += 1
        return currentID

    # Returns names of all papers
    def getNames(self):
        return [i[0] for i in self.execute_read_query('SELECT PaperName FROM Papers')]

    # Returns all questions using filters
    def getQuestions(self, unit, topic, board, qualification, year, paper, orderby):
        return self.execute_read_query("SELECT * FROM Questions WHERE QuestionUnit LIKE '" + unit + "' AND QuestionTopic LIKE '" + topic + "' AND ExamBoard LIKE '" + board + "' AND Qualification LIKE '" + qualification + "' AND Year LIKE '" + str(year) + "' AND QuestionPaper LIKE '" + paper + "' ORDER BY " + orderby)

    # Returns all question units
    def getUnits(self):
        return [i[0] for i in self.execute_read_query('SELECT DISTINCT QuestionUnit FROM Questions')]

    # Returns all topics in a specified question unit
    def getTopics(self, unit):
        return [i[0] for i in self.execute_read_query("SELECT DISTINCT QuestionTopic FROM Questions WHERE QuestionUnit LIKE '" + unit + "'")]

    # Returns all exam boards for which there is a question from the specific topic and/or unit
    def getBoards(self, unit, topic):
        return [i[0] for i in self.execute_read_query("SELECT DISTINCT ExamBoard FROM Questions WHERE QuestionUnit LIKE '" + unit + "' AND QuestionTopic LIKE '" + topic + "'")]

    # Returns all qualifications for which there is a question from the specific topic and/or unit and/or exam board
    def getQualifications(self, unit, topic, board):
        return [i[0] for i in self.execute_read_query("SELECT DISTINCT Qualification FROM Questions WHERE QuestionUnit LIKE '" + unit + "' AND QuestionTopic LIKE '" + topic + "' AND ExamBoard LIKE '" + board + "'")]

    # Returns all years for which there is a question from the specific topic and/or unit and/or exam board and/or qualification
    def getYears(self, unit, topic, board, qualification):
        return [i[0] for i in self.execute_read_query("SELECT DISTINCT Year FROM Questions WHERE QuestionUnit LIKE '" + unit + "' AND QuestionTopic LIKE '" + topic + "' AND ExamBoard LIKE '" + board + "' AND Qualification LIKE '" + qualification + "'")]

    # Returns all exam papers for which there is a question from the specific topic and/or unit and/or exam board and/or qualification and/or year
    def getQuestionPapers(self, unit, topic, board, qualification, year):
        return [i[0] for i in self.execute_read_query("SELECT DISTINCT QuestionPaper FROM Questions WHERE QuestionUnit LIKE '" + unit + "' AND QuestionTopic LIKE '" + topic + "' AND ExamBoard LIKE '" + board + "' AND Qualification LIKE '" + qualification + "' AND Year LIKE '" + str(year) + "'")]

    def getClasses(self):
        return [i[0] for i in self.execute_read_query("SELECT * FROM Classes")]

# This represents the paper that the user creates/edits (not the exam paper from where the questions are sourced)
class paper:
    def __init__ (self, name, ID):
        self._name = name
        self._ID = ID
        # List stores all questions in the paper
        self._questions = []

    def getID(self):
        return self._ID
    
    # Querys the database for all the questions that are within the specific paper
    def initialiseQuestions(self):
            list = data.execute_read_query("SELECT Questions.QuestionID, QuestionUnit, QuestionTopic, QuestionMarks, QuestionMins, ExamBoard, Qualification, Year, QuestionPaper, Question, MarkScheme, ExaminersReport FROM Questions, Links WHERE Links.QuestionID = Questions.QuestionID AND Links.PaperID=" + str(self._ID) + " ORDER BY Links.QuestionOrder")
            print(list)
            for x in list:
                # Adds the question into the list as either a text question if the question is stored as a txt file (check if last letter is t) or an image question if it is not
                if x[9][len(x[9])-1] == 't':
                    self._questions.append(textQuestion(x[0],x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9], x[10], x[11]))
                else:
                    self._questions.append(imageQuestion(x[0],x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9], x[10], x[11]))

    # Adds new paper to databse and saves
    def addPaper(self):
        data.addPaper(self._name, self._ID)
        data.save()

    # This allows the user to edit a filter
    def filters(self, list, filtertype):
        while True:
            print()
            print('Filter by ' + filtertype + ':')
            count = 1
            # Displays all available options for the filer
            for x in list:
                print(str(count) + '. ' + str(x))
                count += 1
            # Option to not filter that specific metric
            print('0. Do not filter by ' + filtertype)
            try:
                option = int(input('Please choose an option: '))
                # Wildcard is used if option to not filter is chosen
                if option == 0:
                    return '%'
                # Returns relevant syntax for the filter to work in the SQL query
                else:
                    return list[option-1]
            except:
                print()
                print('That is not a valid option 5')

    def editPaper(self):
        option = None
        unit, topic, board, qualification, year, paper, orderby = '%', '%', '%', '%', '%', '%', 'QuestionMarks'
        changes = stack()
        while option != 0:
            questions = data.getQuestions(unit, topic, board, qualification, year, paper, orderby)
            question_list = []
            for x in questions:
                x = list(x)
                question_list.append(x)
            try:
                while True:
                    print()
                    print("Choose a question:")
                    print()
                    num = 1
                    for x in question_list:
                        print(str(num) + '. ' + str(x[1:8]))
                        num += 1
                    print(str(len(question_list) + 1) + '. Undo previous change')
                    print(str(len(question_list) + 2) + '. Edit filters and sort')
                    print(str(len(question_list) + 3) + '. Change the order of questions')
                    print(str(len(question_list) + 4) + '. Export paper')
                    print('0. Save and quit')
                    print()
                    option = int(input('Please select an option: '))
                    if option < 0 or option > (len(question_list) + 4):
                        print('That is not a valid option 6')
                    else:
                        break
            except ValueError:
                print('That is not a valid option 7')
            if option == 0:
                # Save paper
                data.execute_read_query('DELETE FROM Links WHERE PaperID=' + str(self._ID))
                counter = 1
                for x in self._questions:
                    data.execute_read_query('INSERT INTO Links (PaperID, QuestionID, QuestionOrder) VALUES (' + str(self._ID) + ', ' + str(x.getID()) + ', ' + str(counter) + ')')
                    counter += 1
                data.save()
                print()
            elif option == len(question_list) + 1:
                # Undo change using stack
                change = changes.pop()
                if change == False:
                    print('There are no changes to undo')
                elif change[0] == 'r':
                    self._questions.append(change[1])
                    print('Question re-added')
                elif change[0] == 'a':
                    self._questions.remove(change[1])
                    print('Question removed')
                elif change[0] == 's':
                    self._questions[change[1]], self._questions[change[2]] = self._questions[change[2]], self._questions[change[1]]
                    print('Unswapped')
            elif option == len(question_list) + 2:
                # Edit filters and sort
                unit = self.filters(data.getUnits(), 'unit')
                topic = self.filters(data.getTopics(unit), 'topic')    
                board = self.filters(data.getBoards(unit, topic), 'exam board')    
                qualification = self.filters(data.getQualifications(unit, topic, board), 'qualification')    
                year = self.filters(data.getYears(unit, topic, board, qualification), 'year')    
                paper = self.filters(data.getQuestionPapers(unit, topic, board, qualification, year), 'paper')    
                option = 0
                while option != 1 and option != 2:
                    print()
                    print('Sort by:')
                    print('1. Marks')
                    print('2. Minutes')
                    try:
                        option = int(input('Please select an option: '))
                    except ValueError:
                        print()
                        print('That is not a valid option 8')
                    else:
                        if option == 1:
                            orderby = 'QuestionMarks'
                        elif option == 2:
                            orderby = 'QuestionMins'
                        else:
                            print('That is not a valid option 9')
            elif option == len(question_list) + 3:
                # Change the order of questions
                print()
                templist = []
                for x in self._questions:
                    templist.append(x)
                while True:
                    print('Choose a question to swap:')
                    possible_options = []
                    for x in templist:
                        print(str(self._questions.index(x)+1) + '. ', list(x.getInfo())[1])
                        possible_options.append(self._questions.index(x)+1)
                    print()
                    try:
                        option = int(input('Please select an option: '))
                    except ValueError:
                        print('That is not a valid option 10')
                        print()
                    if option not in possible_options:
                        print('That is not a valid option 11')
                        print()
                    else:
                        break
                question1 = option-1
                templist.remove(templist[option-1])
                print()
                while True:
                    print('Choose another question to swap with:')
                    possible_options = []
                    for x in templist:
                        print(str(self._questions.index(x)+1) + '. ', list(x.getInfo())[1])
                        possible_options.append(self._questions.index(x)+1)
                    print()
                    try:
                        option = int(input('Please select an option: '))
                    except ValueError:
                        print('That is not a valid option 12')
                        print()
                    if option not in possible_options:
                        print('That is not a valid option 13')
                        print()
                    else:
                        break
                question2 = option-1
                self._questions[question1], self._questions[question2] = self._questions[question2], self._questions[question1]
                print('Swapped')
                changes.push(['s', question1, question2])
            elif option == len(question_list) + 4:
                # Export paper
                while True:
                    print()
                    print('Choose a file format:')
                    print('1. PDF')
                    print('2. DOCX')
                    print('0. Cancel export')
                    print()
                    try:
                        option = int(input('Please select an option: '))
                    except ValueError:
                        print('That is not a valid option 14')
                    else:
                        if option == 1 or option == 2:
                            # Export to PDF
                            pdf = FPDF()
                            cover_page = ''
                            while cover_page != 'Y' and cover_page != 'y' and cover_page != 'N' and cover_page != 'n':
                                cover_page = input('Would you like a cover page (Y/N): ')
                                if cover_page == 'Y' or cover_page == 'y':
                                    pdf.add_page()
                                    pdf.set_font('Arial', 'B', 16)
                                    pdf.cell(190, 266, self._name, 1, 0, 'C')
                                pdf.set_font('Arial', '', 14)
                                for x in self._questions:
                                    pdf.add_page()
                                    if 'txt' in x.getPath():
                                        with open(sys.path[0] + '/Questions/' + x.getPath(), "r") as f:
                                            pdf.write(5, f.read())
                                    else:
                                        pdf.image(sys.path[0] + '/Questions/' + x.getPath(), w = 190)
                                ms = ''
                                while ms != 'Y' and ms != 'y' and ms != 'N' and ms != 'n':
                                    ms = input('Would you like the mark scheme (Y/N): ')
                                    if ms == 'Y' or ms == 'y':
                                        for x in self._questions:
                                            pdf.add_page()
                                            if 'txt' in x.getMSPath():
                                                with open(sys.path[0] + '/Questions/' + x.getMSPath(), "r") as f:
                                                    pdf.write(5, f.read())
                                            else:
                                                pdf.image(sys.path[0] + '/Questions/' + x.getMSPath(), w = 190)
                                    elif ms != 'n' and ms != 'N':
                                        print('That is not a valid option')
                                er = ''
                                while er != 'Y' and er != 'y' and er != 'N' and er != 'n':
                                    er = input("Would you like the examiner's report (Y/N): ")
                                    if er == 'Y' or er == 'y':
                                        for x in self._questions:
                                            pdf.add_page()
                                            if 'txt' in x.getERPath():
                                                with open(sys.path[0] + '/Questions/' + x.getERPath(), "r") as f:
                                                    pdf.write(5, f.read())
                                            else:
                                                pdf.image(sys.path[0] + '/Questions/' + x.getERPath(), w = 190)
                                    elif er != 'n' and er != 'N':
                                        print('That is not a valid option')
                                pdf.output(self._name+'.pdf', 'F')
                                if option == 1:
                                    print('Exported')
                                # Convert PDF file to DOCX then delete PDF file
                                else:
                                    pdf_file = sys.path[0] + '/' + self._name + '.pdf'
                                    docx_file = sys.path[0] + '/' + self._name + '.docx'
                                    cv = Converter(pdf_file)
                                    cv.convert(docx_file)
                                    cv.close()
                                    os.remove(self._name + '.pdf')
                                    print('Exported')
                            break
                        elif option == 0:
                            break
                        else:
                            print('That is not a valid option 15')
                print()
            else:
                option -= 1
                path = question_list[option][9]
                if path[len(path)-1] == 't':
                    current_question = textQuestion(question_list[option][0], question_list[option][1], question_list[option][2], question_list[option][3], question_list[option][4], question_list[option][5], question_list[option][6], question_list[option][7], question_list[option][8], question_list[option][9], question_list[option][10], question_list[option][11])
                else:
                    current_question = imageQuestion(question_list[option][0], question_list[option][1], question_list[option][2], question_list[option][3], question_list[option][4], question_list[option][5], question_list[option][6], question_list[option][7], question_list[option][8], question_list[option][9], question_list[option][10], question_list[option][11])
                while True:
                    try:
                        print()
                        print('1. View Question')
                        print('2. View Mark Scheme')
                        print("3. View Examiner's report")
                        check = False
                        for x in self._questions:
                            if x.getID() == current_question.getID():
                                check = True
                        if check:
                            print('4. Remove from paper')
                        else:
                            print('4. Add to paper')
                        print('0. Go back')
                        print()
                        option = int(input('Please select an option: '))
                    except ValueError:
                        print('That is not a valid option 16')
                    if option == 1:
                        current_question.viewQuestion()
                    elif option == 2:
                        current_question.viewMarkScheme()
                    elif option == 3:
                        current_question.viewExaminersReport()
                    elif option == 4:
                        check = False 
                        for x in self._questions:
                            if x.getID() == current_question.getID():
                                check = True
                                self._questions.remove(x)
                                print('Removed')
                                changes.push(['r', current_question])
                        if not check:                            
                            self._questions.append(current_question)
                            print('Added')
                            changes.push(['a', current_question])
                        break
                    elif option == 0:
                        self.editPaper()
                        break
                    else:
                        print('That is not a valid option 1')

class question:
    def __init__(self, ID, unit, topic, marks, mins, board, qual, year, paper, path, mspath, erpath):
        self._ID = ID
        self._unit = unit
        self._topic = topic
        self._marks = marks
        self._mins = mins
        self._board = board
        self._qual = qual
        self._year = year
        self._paper = paper
        self._path = path
        self._mspath = mspath
        self._erpath = erpath

    def getID(self):
        return self._ID

    def getInfo(self):
        return self._ID, [self._unit, self._topic, self._board, self._qual, self._year, self._paper]

    def getPath(self):
        return self._path

    def getMSPath(self):
        return self._mspath

    def getERPath(self):
        return self._erpath
    
class textQuestion(question):
    def __init__(self, ID, unit, topic, marks, mins, board, qual, year, paper, path, mspath, erpath):
        super().__init__(ID, unit, topic, marks, mins, board, qual, year, paper, path, mspath, erpath)
    
    def viewQuestion(self):
        print()
        with open(sys.path[0] + '/Questions/' + self._path, "r") as f:
            print(f.read())
    
    def viewMarkScheme(self):
        print()
        with open(sys.path[0] + '/Questions/' + self._mspath, "r") as f:
            print(f.read())
    
    def viewExaminersReport(self):
        print()
        if self._erpath == 'N/A':
            print("Examiner's report not available for this question")
        else:
            with open(sys.path[0] + '/Questions/' + self._erpath, "r") as f:
                print(f.read())

class imageQuestion(question):
    def __init__(self, ID, unit, topic, marks, mins, board, qual, year, paper, path, mspath, erpath):
        super().__init__(ID, unit, topic, marks, mins, board, qual, year, paper, path, mspath, erpath)
    
    def viewQuestion(self):
        im = Image.open(sys.path[0] + '/Questions/' + self._path)
        im.show()
    
    def viewMarkScheme(self):
        im = Image.open(sys.path[0] + '/Questions/' + self._mspath)
        im.show()
    
    def viewExaminersReport(self):
        if self._erpath == 'N/A':
            print("Examiner's report not available for this question")
        else:
            im = Image.open(sys.path[0] + '/Questions/' + self._erpath)
            im.show()

class stack:
    def __init__(self):
        self._stack = [' ',' ',' ',' ',' ',' ',' ',' ']
        self._top = 0

    def push(self, item):
        self._stack[self._top] = item
        self._top += 1
        if self._top == len(self._stack):
            self._stack.append(' ')

    def pop(self):
        if self._top == 0:
            return False
        item = self._stack[self._top - 1]
        self._stack[self._top - 1] = ' '
        self._top -= 1
        return item

data = database('database.db')
new_menu = menu()