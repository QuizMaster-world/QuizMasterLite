[![License GPLv3](https://img.shields.io/badge/license-GPL_v3-green.svg)](http://www.gnu.org/licenses/gpl-3.0.html)

# QuizMasterLite

QuizMasterLite is a streamlined version of the original QuizMaster app, designed specifically for users who prefer a lighter, faster, and more resource-efficient experience. Unlike [QuizMasterMini](https://github.com/hermonochy/QuizMasterMini.git) though, QuizMasterLite still uses pygame as the main GUI framework, ensuring that the user experience is still aesthetically pleasing.

**Benifits:**

- **Prioritizing Core Features**: Focuses on the fundamental quiz functionalities that matter the most.
- **Streamlined Performance**: Reduces processing demands by eliminating non-essential components.
- **Consistent Usability**: Retains the familiar, user-friendly interface of the original app while trimming unnecessary overhead.
- **Lightweight Design**: Ideal for environments with limited storage or processing power.
- **Smaller Storage Usage**: Only a quarter of the size of QuizMaster.

## Usage

### Installation

1. Clone this repository via terminal: ```git clone --recurse-submodules https://github.com/badguyland/QuizMasterLite```

  If you prefer not to include the example quizzes, you can omit the `--recurse-submodules` flag: ```git clone https://github.com/badguyland/QuizMasterLite```

2. Enter the directory containing the game executable: ```cd QuizMasterLite```

##### Either:

Run the included script `./setup.sh` (Linux) or `setup.bat` script for Windows. 

##### Or: (Advanced, Ubuntu/Debian only):

1. Set up a new virtual environment: ```python3 -m venv venv```
2. Activate the environment: ```source venv/bin/activate``` (To decativate, type `deactivate`)
3. Install tkinter: ```sudo apt-get install python3-tk```
4. Install packages in `requirements.txt`: ```pip3 install -r requirements.txt```

*Steps 1 and 2 are optional, but recommended if you wish to avoid a headache with Python module conflicts.*

### Running QuizMasterLite

To run the program, enter `./run.sh` for Linux or `run.bat` for Windows into the terminal. 
Alternatively, if you did not create a virtual environment, start the application using `./quiz.py` for Linux and `python quiz.py` for Windows.

You'll be greeted by the homepage where you have the option to `Play a Quiz` or `Make a Quiz`. Selecting `Make a Quiz` opens the `QuizCreator` program. Click `Add` to include multiple choice questions and ensure you specify the correct answer followed by wrong answers separated by commas. Tooltips provide helpful guidance throughout the process. Once you have completed it, using the `Save` button to save it to an appropriate location. `Play a Quiz`, on the otherhand, takes you into the game. To select a quiz, simply type the theme you would like to play. Afterwards select the game mode and play!.