# Lift Coursework

A simple python based program to run and compare different lift algorithms. This project compares 3 different algorithms:

- SCAN: A simple algorithm which moves up and down, processing any requests it encounters. The lift changes direction at the top and bottom.
- LOOK: Similar to SCAN, however the lift can change direction at any point, rather than just the top and bottom.
- MYLIFT: Processes requests based on the requests priority using priority queues and heaps.

## Requirements

This project is built on Python 3.12.1 but will work on any version above it.
The module requirements can be found in the ```requirements.txt``` file and are also listed here:

```
jsbeautifier
matplotlib
```

To install these modules, navigate to the project directory in the terminal and run ```pip install -r requirements.txt```

## Usage

Download this project as a .zip file, extract it, then run the ```run.bat``` file or run the ```python sources/main.py``` command from the terminal.
