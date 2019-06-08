# Chat categorizer 1.0

Chat categorizer is a tool for easily categorizing chat interactions.

## Installation

You need Python 3 installed on your computer, you can run the program through the python folder. This option works for any operating system. 

## Usage

Run the following in command line :

```bash
python chat-categorizer.py
```

Chat content must be structured in the following form : option1;option2;name;speech in a text file. One line per chat interaction. See the example **chat.txt**

Categories must be specified in the file **categories_file.txt** (one category per line)

The program reads the chat and displays the name, the related speech and a bunch a buttons corresponding to your categories. Left click to choose a category, right click to come back to a previous line, middle click to change the button layout. One you have changed the layout, this latter is stored in the file **buttons_config_file.cfg**. Remove this file to set again the default layout.

Previous coded lines are displayed in the console. 

If you have any question, send a message to sunny.avry@gmail.com

## Contributing

Chat categorizer 1.0 is the very first version of the software. New contributions are welcome.


