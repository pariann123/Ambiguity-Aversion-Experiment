import random
from os import listdir
from random import randint
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
app = QApplication([])
window = uic.loadUi("assignment2_design.ui")

# Defining variables
window.results_file= "results_file.csv"
window.email_file="email_file.csv"
window.age=0
window.gender=""
window.education=""
window.email=""
window.condition_index=0             # 0= 100 marbles condition, 1=10 marbles condition, 2=2 marbles condition
window.condition_list=[100,10,2]     # By adding any other number here, you can create more conditions
window.condition_index_list=[0, 1, 2]    # Also must add an index to this list to create an additional condition (and that's it!)
window.condition_half_list=[]        # This creates a list that stores half of the number of each condition, for setting the instruction's text
window.urn_position=0                # Position 0 = urn A is 50/50 and urn B is random. Position 1 = urn A is random and urn B is 50/50
window.urn_50_50="Urn A"             # Default urns, this changes randomly for each participant
window.urn_random="Urn B"
window.selected_urn="urn A"          # This is the default urn selected, if urn B is chosen this changes

# Default texts
window.urnA_descrip_lbl.setText("contains 50% blue marbles and 50% red marbles")   #Default description of urn A, this changes if its place changes
window.urnB_descrip_lbl.setText("contains random amount of blue and red marbles")

# Hiding error messages until they are needed
window.error_msg_consent_lbl.hide()
window.error_msg_age_lbl.hide()
window.error_msg_gender_lbl.hide()
window.error_msg_education_lbl.hide()

# If it is the first time running the experiment, it creates the file, otherwise it reads the file to know which was the previous condition
def start_experiment():
    window.page.setCurrentIndex(0)           # Experiment starts on page 1, consent form
    if window.results_file in listdir():
        file = open(window.results_file, 'r')
        all_data = file.readlines()

        for data in all_data:
            data_list=[]
            data_list.append(data.split(","))

        old_cond=int(data_list[0][3]) # This is reading the condition of the last participant to give the next participant's condition accordingly
        window.condition_index=old_cond+1                # Every time add one to the condition
        if old_cond==window.condition_index_list[-1]:    # But if it's the last condition in the list (condition 2 which is 2 marbles) then set to condition 0 (100 marbles)
            window.condition_index=0
    else:
        file = open(window.results_file, 'w')
        columns=("Age,Gender,Education,Condition,Urn position,Selected urn,Marble")
        file.write(columns)

        file = open(window.email_file, 'w')
        columns = ("Emails")
        file.write(columns)

start_experiment()

def save_results():
    if window.results_file in listdir():
        file = open(window.results_file, 'a')
        info=f"\n{window.age},{window.gender},{window.education},{window.condition_index},{window.urn_position},{window.selected_urn},{window.chosen_marble}"
        file.write(info)
        file.close()

# Saving email in a different file so it cannot be traced back to the participant
def save_email():
    next_page()
    window.email = window.email_le.text()
    if window.email !="":                      # Only adds email when it is provided, so that it doesn't add an empty line for participants who did not provide this information
        new_file = open(window.email_file, 'a')
        information = f"\n{window.email}"
        new_file.write(information)
        new_file.close()

# Randomly deciding urn positions per participant
window.urn_position=randint(0,1)   # Position 0 = urn A is 50/50 and urn B is random. Position 1 = urn A is random and urn B is 50/50
if window.urn_position==1:         # Changing the default here if urn_position ==1
    window.urn_50_50="Urn B"
    window.urn_random="Urn A"
    window.urnB_descrip_lbl.setText("Contains 50% blue marbles and 50% red marbles")
    window.urnA_descrip_lbl.setText("Contains random amount of blue and red marbles")

# Working out the distribution by randomly selecting a number between 0 and the condition (100,10,2)
# For example, if in condition 0 random_red_marbs is 80, then random_blue_marbs is equal to 20. This is the distribution for this participant.
window.random_red_marbs=randint(0, window.condition_list[window.condition_index])
window.random_blue_marbs= window.condition_list[window.condition_index] - window.random_red_marbs

# This calculates the 50% number of each of the conditions
# This will be used to set the text of the instructions according to the condition participants are in
for number in window.condition_list:
    window.condition_half_list.append(int(number/2))

# Setting the instructions according to the conditions
window.text_50_50=window.condition_half_list[window.condition_index]
window.text_num_marbles=window.condition_list[window.condition_index]
window.text_012=f"0,1,2,...,{window.condition_list[window.condition_index]}"
if window.condition_index == 2:      # This is only needed for the 2 marbles condition as it doesn't have the same structure in writing as the other conditions
    window.text_012 = "0,1,2"

window.description_lbl.setText(f"Consider the following problem carefully, then click start.\n\nOn the screen will be two urns, labeled A and B, containing red and blue marbles, and you have to draw a marble from one of the urns without knowing what's inside. If you get a blue marble, you will be entered in a £30 lottery draw.\n\n{window.urn_50_50} contains {window.text_50_50} red marbles and {window.text_50_50} blue marbles. {window.urn_random} contains {window.text_num_marbles} marbles in an unknown color ratio, from {window.text_num_marbles} red marbles and 0 blue marbles to 0 red marbles and {window.text_num_marbles} blue marbles. The mixture of red and blue marbles in {window.urn_random} has been decided by writing the numbers {window.text_012} on separate slips of paper, shuffling the slips thoroughly, and then drawing one of them at random. The number chosen was used to determine the number of blue marbles to be put into {window.urn_random}, but you do not know the number. Every possible mixture of red and blue marbles in {window.urn_random} is equally likely.\n\nYou have to decide whether you prefer to draw a marble at random from Urn A or Urn B. What you hope is to draw a blue marble and be entered for the £30 lottery draw. Consider very carefully from which urn you prefer to draw the marble, then click on your chosen urn. You will draw a marble from your chosen urn straight afterwards.\n\nWhen you are ready to begin the experiment, press 'Start'.")

# This function is called when we need to go to the next page
def next_page():
    page_index = window.page.currentIndex()
    page_index += 1
    window.page.setCurrentIndex(page_index)

# Page 1 = consent form
def page1():
    if window.gives_consent_cb.isChecked():
        next_page()
    else:
        window.error_msg_consent_lbl.show()

#Page 2 = demographics
def page2():
    error=False     # if all errors are false, then can proceed to the next page

    part_age = int(window.age_sb.text())
    if part_age<16:
        window.error_msg_age_lbl.show()
        error = True
    else:
        window.age =window.age_sb.text()
        window.error_msg_age_lbl.hide()

    if not window.female_rb.isChecked() and not window.male_rb.isChecked() and not window.prefer_not_say_rb.isChecked():
        window.error_msg_gender_lbl.show()
        error = True

    if window.female_rb.isChecked():
        window.error_msg_gender_lbl.hide()
        window.gender="Female"
    elif window.male_rb.isChecked():
        window.error_msg_gender_lbl.hide()
        window.gender = "Male"
    elif window.prefer_not_say_rb.isChecked():
        window.error_msg_gender_lbl.hide()
        window.gender = "Prefer not to say"

    if window.education_cb.currentText() == "Select...":
        window.error_msg_education_lbl.show()
        error = True
    else:
        window.error_msg_education_lbl.hide()
        window.education=window.education_cb.currentText()

    if error==False:
        page3()
    window.repaint()

# Page 3 = instructions
# Timer set at 10 seconds, participant cannot proceed for 10s to ensure that they read the instructions
def page3():
    next_page()
    window.start_pb.setEnabled(False)   # Start button disabled for 10s
    window.timerPage1 = QTimer()
    window.seconds = 10
    window.timerPage1.start(1000)
    window.timerPage1.timeout.connect(page3_timer)

def page3_timer():
    window.seconds -= 1          # Timer starts from 10 until it reaches 0
    if window.seconds == 0:
        window.timerPage1.stop()
        window.start_pb.setEnabled(True)  # Once 0 is reached, start button is enabled
    display()

def display():
    window.timer_lbl.setText(str(window.seconds))

#Page 4 = animation and experiment page
my_timer = QTimer()
def page4():
    next_page()
    my_timer.start(50)
    my_timer.timeout.connect(animate)

def animate():
    marbles=[window.red_marb_1,window.red_marb_2,window.red_marb_3,window.red_marb_4,window.red_marb_5,window.red_marb_6,window.blue_marb_1,window.blue_marb_2,window.blue_marb_3,window.blue_marb_4,window.blue_marb_5,window.blue_marb_6]
    for each_marb in marbles:
        if each_marb.y()<210:
            each_marb.setGeometry(each_marb.x(), each_marb.y()+5, 20,20)
    window.repaint()

class click_label(QLabel):
    clicked = pyqtSignal()
    def mousePressEvent(self, mouseEvent):
        self.clicked.emit()

def urnA_pressed():
    next_page()
    if window.urn_position==0: #urn A=50/50 and urn B=random
        blue_red_amount = ['red'] * 50 + ['blue'] * 50       # probability of red and blue are both 50%
        window.chosen_marble = random.choice(blue_red_amount)
        if window.chosen_marble=="blue":
            win()
        else:
            lose()
    else:                      #urn A=random and urn B=50/50
        blue_red_amount = ['red'] * window.random_red_marbs + ['blue'] * window.random_blue_marbs # Calculating the amount of red and blue marbles by basing it on the distribution we computed above
        window.chosen_marble = random.choice(blue_red_amount)
        if window.chosen_marble=="blue":
            win()
        else:
            lose()

def urnB_pressed():
    next_page()
    window.selected_urn="Urn B"
    if window.urn_position==0: #urn A=50/50 and urn B=random
        blue_red_amount = ['red'] * window.random_red_marbs + ['blue'] * window.random_blue_marbs
        window.chosen_marble = random.choice(blue_red_amount)
        if window.chosen_marble == "blue":
            win()
        else:
            lose()
    else:                      #urn A=random and urn B=50/50
        blue_red_amount = ['red'] * 50 + ['blue'] * 50
        window.chosen_marble = random.choice(blue_red_amount)
        if window.chosen_marble == "blue":
            win()
        else:
            lose()

# Creating a clickable label for the urns
window.urnA = click_label(window.experiment)
pixmap = QPixmap("urn.png")
window.urnA.setPixmap(pixmap)
window.urnA.setScaledContents(True)
window.urnA.setGeometry(385, 200, 140, 170)
window.urnA.setCursor(Qt.OpenHandCursor)  # Changing to open hand cursor is an indication to participant that this can be clicked
window.urnA.clicked.connect(urnA_pressed)

window.urnB = click_label(window.experiment)
pixmap = QPixmap("urn.png")
window.urnB.setPixmap(pixmap)
window.urnB.setScaledContents(True)
window.urnB.setGeometry(573, 200, 140, 170)
window.urnB.setCursor(Qt.OpenHandCursor)
window.urnB.clicked.connect(urnB_pressed)

def win():
    window.win_lose_lbl.setText("Well done you drew a blue marble!\n\nYou now have a chance to be entered in the £30 draw.\n\nIf you want to be entered enter your email.")
    pal = QPalette(window.win_lose_lbl.palette())             # Changing the colour of the message according to winning or losing
    pal.setColor(QPalette.WindowText, QColor(Qt.darkGreen))
    window.win_lose_lbl.setPalette(pal)
    save_results()

def lose():
    window.win_lose_lbl.setText("Sorry you drew a red marble, you did not win.")
    pal = QPalette(window.win_lose_lbl.palette())
    pal.setColor(QPalette.WindowText, QColor(Qt.red))
    window.win_lose_lbl.setPalette(pal)

    window.email_le.hide()             # Anything to do with providing email is hidden for those who did not win
    window.email_lbl.hide()
    window.save_email_lbl.hide()
    save_results()

# Connecting the buttons to their functions
window.submitted_pb.clicked.connect(page1)
window.submit_pb.clicked.connect(page2)
window.start_pb.clicked.connect(page4)
window.debrief_pb.clicked.connect(save_email)
window.terminate_pb.clicked.connect(exit)

window.show()
app.exec_()
