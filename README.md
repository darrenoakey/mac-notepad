![](banner.jpg)

# Mac Notepad

A simple, lightweight text editor for macOS.

## Purpose

Mac Notepad provides a clean, distraction-free text editing experience from the command line. It offers basic text editing functionality without the complexity of full-featured IDEs or text editors.

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Launch the Application

Open the notepad with no file:

```bash
./notepad
```

Open the notepad with an existing file:

```bash
./notepad /path/to/file.txt
```

### Using the Run Script

The `run` script provides additional development commands:

```bash
# Launch the application
./run app

# Launch with a specific file
./run app /path/to/file.txt

# Run linter
./run lint

# Run full verification
./run check

# Run a specific test
./run test src/notepad_test.py::test_something
```

## Examples

### Create a New Document

```bash
./notepad
```

This opens a blank editor where you can start typing immediately.

### Edit an Existing File

```bash
./notepad ~/Documents/notes.txt
```

This opens the specified file for editing.

### Quick Edit from Any Directory

```bash
/path/to/mac-notepad/notepad myfile.txt
```

You can run the notepad command from any directory by specifying the full path to the executable.

## License

This project is licensed under [CC BY-NC 4.0](https://darren-static.waft.dev) - free to use and modify, but no commercial use without permission.
