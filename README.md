
# Blockchain-PoW-Consensus

Simple implementation of the Blockchain: Consensus Mechanism Proof-of-Work

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)
- [Troubleshooting](#troubleshooting)

## Introduction
This project is a simple implementation of a blockchain with a Proof-of-Work (PoW) consensus mechanism. It includes a graphical user interface (GUI) for configuring and running the blockchain.

## Features
- Blockchain with PoW consensus mechanism
- GUI for configuring blockchain parameters
- Visualization of mining times and difficulty adjustments
- Logging of blockchain statistics

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/antoniooreany/Blockchain-PoW-Consensus.git
    cd Blockchain-PoW-Consensus
    ```

2. Ensure Python 3.7 or higher is installed. You can check your Python version with:
    ```bash
    python --version
    ```
    - If Python 3.6 or lower is installed, install Python 3.7 or higher:
      - **macOS**: Install Python via [Homebrew](https://brew.sh/):
        ```bash
        brew install python
        ```
      - **Windows**: Download the latest Python installer from the [official Python website](https://www.python.org/downloads/), run the installer, and ensure you check the box to **Add Python to PATH** during installation.
      - **Linux**: Use your package manager to install Python 3.7 or higher. For example:
        - **Ubuntu/Debian**:
          ```bash
          sudo apt update
          sudo apt install python3
          ```
        - **Fedora**:
          ```bash
          sudo dnf install python3
          ```

3. Create a virtual environment:
    ```bash
    python -m venv venv
    ```

4. Activate the virtual environment:
    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

5. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Set the `PYTHONPATH` environment variable to include the project directory. This ensures that Python recognizes `src` as a module:
    ```bash
    export PYTHONPATH="${PYTHONPATH}:$(pwd)"
    ```

2. Run the application:
    ```bash
    python src/main.py
    ```

3. Use the GUI to configure the blockchain parameters and start the blockchain.

## Configuration
The following parameters can be configured through the GUI:
- Initial Bit Difficulty
- Target Block Mining Time
- Adjustment Block Interval
- Clamp Factor
- Smallest Bit Difficulty
- Number of Blocks to Add
- Number of Blocks Slice

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the GNU GENERAL PUBLIC LICENSE. See the `LICENSE` file for details.

## Troubleshooting

- If you encounter the following issue on Windows:
    ```plaintext
    PS ~\Blockchain-PoW-Consensus> python3 --version
    Python was not found; run without arguments to install from the Microsoft Store, or disable this shortcut from Settings > Manage App Execution Aliases.
    PS ~\Blockchain-PoW-Consensus> python --version
    Python 3.13.0
    PS ~\Blockchain-PoW-Consensus>
    ```
    This indicates that `python3` is not recognized as a command. You can use `python` instead of `python3` for all commands.

- If you encounter the following issue on Windows:
    ```plaintext
    venv\Scripts\activate : File ~\Blockchain-PoW-Consensus\venv\Scripts\Activate.ps1 cannot be loaded because running scripts is disabled on this system. For more information,
    see about_Execution_Policies at https:/go.microsoft.com/fwlink/?LinkID=135170.
    ```
    This indicates that the execution policy is preventing the script from running. To resolve this, open PowerShell as an administrator and run:
    ```powershell
    Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
    ```
    Confirm the change by typing `Y` and pressing Enter. Then, you should be able to activate the virtual environment with:
    ```powershell
    venv\Scripts\activate
    ```

- If you encounter the following issue while installing `numpy` on Windows:
    ```plaintext
    error: subprocess-exited-with-error

    × Preparing metadata (pyproject.toml) did not run successfully.
    │ exit code: 1
    ╰─> [21 lines of output]
        ...
        ERROR: Unknown compiler(s): [['icl'], ['cl'], ['cc'], ['gcc'], ['clang'], ['clang-cl'], ['pgcc']]
        ...
    ```
    This indicates that the necessary build tools are not installed. To resolve this, follow these steps:
    1. Install Microsoft Visual C++ Build Tools:
       - Download and install the [Microsoft Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/).
       - During installation, ensure you select the "Desktop development with C++" workload.

    2. Upgrade `pip` to the latest version:
       ```powershell
       python -m pip install --upgrade pip
       ```

    3. Install `numpy`:
       ```powershell
       pip install numpy
       ```

    4. Install the dependencies from `requirements.txt`:
       ```powershell
       pip install -r requirements.txt
       ```

- If you encounter the following issue on Windows:
    ```plaintext
    export : The term 'export' is not recognized as the name of a cmdlet, function, script file, or operable program. Check the spelling of the name, or if a path was included, verify that the path is correct and try again.
    ```
    This indicates that the `export` command is not recognized in PowerShell. Use the following command instead:
    ```powershell
    $env:PYTHONPATH = "${env:PYTHONPATH};$(pwd)"
    ```

- If you encounter the following issue:
    ```plaintext
    _tkinter.TclError: Can't find a usable init.tcl in the following directories:
    ```
    This indicates that the `init.tcl` file, which is part of the Tcl/Tk library used by `tkinter`, is missing or not found in the expected directories. This usually happens when the Tcl/Tk installation is incomplete or not properly configured. To resolve this, ensure that Tcl/Tk is properly installed and configured.