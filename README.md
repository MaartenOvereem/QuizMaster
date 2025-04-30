# Project Title
**QuizMaster** aids your study of large amounts of material by allowing you to store relevant questions and topics in a concise format and review them later in the form of a quiz.
You can take screenshots of questions and answers you'd like to revisit. When the time comes, QuizMaster will present them to you — showing the question first, and only revealing the answer after you've had a chance to try answering it yourself.

## Project Description
The project consists of three modules: Internal, Interface, and Incoming, each serving a specific purpose.

-The **Internal module** manages the storage of saved screenshots using a .json file.

-The **Interface module** handles user interactions and facilitates communication between the Internal and Incoming modules.

-The **Incoming module** monitors and retrieves new screenshots as they are taken.

-Additionally, users can store images that are already saved on their computer, not just newly taken screenshots.

**Internal Module**<br>
The Internal module is responsible for managing both the stored screenshots and the directory path that the Incoming module monitors for new screenshots. It updates the .json storage file using a recursive algorithm. When it's time to quiz yourself, the Internal module retrieves the relevant questions.

Each question or answer can consist of multiple images. This is especially useful when dealing with extensive content, such as detailed explanations or derivations. You can also store pre-existing images (not just screenshots) directly through the Internal module.

**Interface module**<br>
The Interface module consists of a Tkinter-based GUI, allowing for seamless user interaction with both the Internal and Incoming modules. Additionally, it manages communication between these modules behind the scenes.

There are three types of items in the interface: Map, Set, and Question.

A Map represents a general directory. It serves as a way to organize your images by course, book, or semester. A Map can contain other Maps as well as Sets.

A Set stores the questions you want to revise later. These are the items the Internal module retrieves when you're ready to quiz yourself.

A Question holds the actual study material, split into two parts: question and answer. The question is shown first, followed by the answer. Both sections can contain multiple images, which can also be added manually.

At the top level, the Directory head allows you to add items directly to the root directory and change the folder path that the Incoming module monitors for new screenshots.

Interaction with all items is facilitated through right-click context menus.

Note: when adding images there is a sequence of pop-ups that allow the user to accurately place the image, when closing these pop-ups through pressing "x" in the top-right corner the sequence continues. However, this does not interfere with the running of the programm as simply closing the pop-ups that appear later in the sequence does not impede running.

**Incoming module**<br>
The Incoming module uses the Watchdog library to monitor incoming screenshots in the folder you have specified through the Directory head.

Monitoring begins when you choose to add a new image by means of scanning. It automatically stops either when a screenshot is detected or when you cancel the process without adding an image.

## How to Install and Run the Project
To get started with the **QuizMaster** project, follow these steps to install and run it locally on your machine.

### Prerequisites
Before you begin, ensure you have the following software installed:
- **Python 3.13.3+**: You can download it from [python.org](https://www.python.org/), when installing make sure to select the Tcl/Tk option which allows you to use Tkinter
- **Pip**: Python's package manager (usually comes with Python installation).

### Installation Steps
1. **Clone the Repository**<br>  
   First, clone this repository to your local machine by running:<br>
   ```bash<br>
   git clone https://github.com/your-username/quizmaster.git

2. **Install packages**<br>
   Install the required packages by running:<bt>
   ```bash
   pip install -r requirements.txt

4. **Run main.py**<br>
   In the terminal run
   ```bash
    pyton main.py
   ```
    Or run main.py in your IDE
   
6. **Get .exe**<br>
   When pyinstaller is installed, see requirement.txt for required version<br>
   Run following command in the terminal:<br>
   ```bash
   pyinstaller --onefile --noconsole main.py
   ```
   This will create a dist folder with main.exe inside, which can be used to run QuizMaster from your desktop<br>
   Note that the .exe file will be unsigned, meaning anti-virus software could detect it as malware<br>
   This is however a false positive

## When Contributing

Be aware that both the Tkinter and Watchdog packages rely on multithreading to run their operations, which can easily interfere with the execution of your code if not managed properly.

Tkinter runs its main GUI application on the main thread, while pop-ups and similar components may run on separate subthreads.<br>  
Watchdog performs its monitoring on a dedicated subthread.

If not handled carefully, the subthreads from these packages can become intertwined, potentially causing your program to stop running.

