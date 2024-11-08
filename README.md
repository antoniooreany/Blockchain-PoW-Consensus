[//]: # ([//]: # &#40;[//]: # &#40;# Blockchain-PoW-Consensus&#41;&#41;)
[//]: # ([//]: # &#40;&#41;)
[//]: # ([//]: # &#40;[//]: # &#40;&#41;&#41;)
[//]: # ([//]: # &#40;[//]: # &#40;Simple implementation of the Blockchain: Consensus Mechanism Proof-of-Work&#41;&#41;)
[//]: # ([//]: # &#40;&#41;)
[//]: # ([//]: # &#40;&#41;)
[//]: # ([//]: # &#40;# Blockchain-PoW-Consensus&#41;)
[//]: # ()
[//]: # ([//]: # &#40;&#41;)
[//]: # ([//]: # &#40;Simple implementation of the Blockchain: Consensus Mechanism Proof-of-Work&#41;)
[//]: # ()
[//]: # ([//]: # &#40;&#41;)
[//]: # ([//]: # &#40;## Table of Contents&#41;)
[//]: # ()
[//]: # ([//]: # &#40;- [Introduction]&#40;#introduction&#41;&#41;)
[//]: # ()
[//]: # ([//]: # &#40;- [Features]&#40;#features&#41;&#41;)
[//]: # ()
[//]: # ([//]: # &#40;- [Installation]&#40;#installation&#41;&#41;)
[//]: # ()
[//]: # ([//]: # &#40;- [Usage]&#40;#usage&#41;&#41;)
[//]: # ()
[//]: # ([//]: # &#40;- [Configuration]&#40;#configuration&#41;&#41;)
[//]: # ()
[//]: # ([//]: # &#40;- [Contributing]&#40;#contributing&#41;&#41;)
[//]: # ()
[//]: # ([//]: # &#40;- [License]&#40;#license&#41;&#41;)
[//]: # ()
[//]: # ([//]: # &#40;&#41;)
[//]: # ([//]: # &#40;## Introduction&#41;)
[//]: # ()
[//]: # ([//]: # &#40;This project is a simple implementation of a blockchain with a Proof-of-Work &#40;PoW&#41; consensus mechanism. It includes a graphical user interface &#40;GUI&#41; for configuring and running the blockchain.&#41;)
[//]: # ()
[//]: # ([//]: # &#40;&#41;)
[//]: # ([//]: # &#40;## Features&#41;)
[//]: # ()
[//]: # ([//]: # &#40;- Blockchain with PoW consensus mechanism&#41;)
[//]: # ()
[//]: # ([//]: # &#40;- GUI for configuring blockchain parameters&#41;)
[//]: # ()
[//]: # ([//]: # &#40;- Visualization of mining times and difficulty adjustments&#41;)
[//]: # ()
[//]: # ([//]: # &#40;- Logging of blockchain statistics&#41;)
[//]: # ()
[//]: # ([//]: # &#40;&#41;)
[//]: # ([//]: # &#40;## Installation&#41;)
[//]: # ()
[//]: # ([//]: # &#40;1. Clone the repository:&#41;)
[//]: # ()
[//]: # ([//]: # &#40;    ```bash&#41;)
[//]: # ()
[//]: # ([//]: # &#40;    git clone https://github.com/antoniooreany/Blockchain-PoW-Consensus.git&#41;)
[//]: # ()
[//]: # ([//]: # &#40;    cd Blockchain-PoW-Consensus&#41;)
[//]: # ()
[//]: # ([//]: # &#40;    ```&#41;)
[//]: # ()
[//]: # ([//]: # &#40;&#41;)
[//]: # ([//]: # &#40;2. Create a virtual environment:&#41;)
[//]: # ()
[//]: # ([//]: # &#40;    ```bash&#41;)
[//]: # ()
[//]: # ([//]: # &#40;    python -m venv venv&#41;)
[//]: # ()
[//]: # ([//]: # &#40;    ```&#41;)
[//]: # ()
[//]: # ([//]: # &#40;&#41;)
[//]: # ([//]: # &#40;3. Activate the virtual environment:&#41;)
[//]: # ()
[//]: # ([//]: # &#40;    - On Windows:&#41;)
[//]: # ()
[//]: # ([//]: # &#40;        ```bash&#41;)
[//]: # ()
[//]: # ([//]: # &#40;        venv\Scripts\activate&#41;)
[//]: # ()
[//]: # ([//]: # &#40;        ```&#41;)
[//]: # ()
[//]: # ([//]: # &#40;    - On macOS/Linux:&#41;)
[//]: # ()
[//]: # ([//]: # &#40;        ```bash&#41;)
[//]: # ()
[//]: # ([//]: # &#40;        source venv/bin/activate&#41;)
[//]: # ()
[//]: # ([//]: # &#40;        ```&#41;)
[//]: # ()
[//]: # ([//]: # &#40;&#41;)
[//]: # ([//]: # &#40;4. Install the required dependencies:&#41;)
[//]: # ()
[//]: # ([//]: # &#40;    ```bash&#41;)
[//]: # ()
[//]: # ([//]: # &#40;    pip install -r requirements.txt&#41;)
[//]: # ()
[//]: # ([//]: # &#40;    ```&#41;)
[//]: # ()
[//]: # ([//]: # &#40;&#41;)
[//]: # ([//]: # &#40;## Usage&#41;)
[//]: # ()
[//]: # ([//]: # &#40;1. Run the application:&#41;)
[//]: # ()
[//]: # ([//]: # &#40;    ```bash&#41;)
[//]: # ()
[//]: # ([//]: # &#40;    python src/main.py&#41;)
[//]: # ()
[//]: # ([//]: # &#40;    ```&#41;)
[//]: # ()
[//]: # ([//]: # &#40;&#41;)
[//]: # ([//]: # &#40;2. Use the GUI to configure the blockchain parameters and start the blockchain.&#41;)
[//]: # ()
[//]: # ([//]: # &#40;&#41;)
[//]: # ([//]: # &#40;## Configuration&#41;)
[//]: # ()
[//]: # ([//]: # &#40;The following parameters can be configured through the GUI:&#41;)
[//]: # ()
[//]: # ([//]: # &#40;- Initial Bit Difficulty&#41;)
[//]: # ()
[//]: # ([//]: # &#40;- Target Block Mining Time&#41;)
[//]: # ()
[//]: # ([//]: # &#40;- Adjustment Block Interval&#41;)
[//]: # ()
[//]: # ([//]: # &#40;- Clamp Factor&#41;)
[//]: # ()
[//]: # ([//]: # &#40;- Smallest Bit Difficulty&#41;)
[//]: # ()
[//]: # ([//]: # &#40;- Number of Blocks to Add&#41;)
[//]: # ()
[//]: # ([//]: # &#40;- Number of Blocks Slice&#41;)
[//]: # ()
[//]: # ([//]: # &#40;&#41;)
[//]: # ([//]: # &#40;## Contributing&#41;)
[//]: # ()
[//]: # ([//]: # &#40;Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.&#41;)
[//]: # ()
[//]: # ([//]: # &#40;&#41;)
[//]: # ([//]: # &#40;## License&#41;)
[//]: # ()
[//]: # ([//]: # &#40;This project is licensed under the GNU GENERAL PUBLIC LICENSE. See the `LICENSE` file for details.&#41;)
[//]: # ()
[//]: # ([//]: # &#40;&#41;)
[//]: # ([//]: # &#40;&#41;)
[//]: # ([//]: # &#40;&#41;)
[//]: # ()
[//]: # ()
[//]: # ([//]: # &#40;# Blockchain-PoW-Consensus&#41;)
[//]: # ()
[//]: # ([//]: # &#40;&#41;)
[//]: # ([//]: # &#40;Simple implementation of the Blockchain: Consensus Mechanism Proof-of-Work&#41;)
[//]: # ()
[//]: # (# Blockchain-PoW-Consensus)

[//]: # ()
[//]: # (Simple implementation of the Blockchain: Consensus Mechanism Proof-of-Work)

[//]: # ()
[//]: # (## Table of Contents)

[//]: # (- [Introduction]&#40;#introduction&#41;)

[//]: # (- [Features]&#40;#features&#41;)

[//]: # (- [Installation]&#40;#installation&#41;)

[//]: # (- [Usage]&#40;#usage&#41;)

[//]: # (- [Configuration]&#40;#configuration&#41;)

[//]: # (- [Contributing]&#40;#contributing&#41;)

[//]: # (- [License]&#40;#license&#41;)

[//]: # ()
[//]: # (## Introduction)

[//]: # (This project is a simple implementation of a blockchain with a Proof-of-Work &#40;PoW&#41; consensus mechanism. It includes a graphical user interface &#40;GUI&#41; for configuring and running the blockchain.)

[//]: # ()
[//]: # (## Features)

[//]: # (- Blockchain with PoW consensus mechanism)

[//]: # (- GUI for configuring blockchain parameters)

[//]: # (- Visualization of mining times and difficulty adjustments)

[//]: # (- Logging of blockchain statistics)

[//]: # ()
[//]: # (## Installation)

[//]: # (1. Clone the repository:)

[//]: # (    ```bash)

[//]: # (    git clone https://github.com/antoniooreany/Blockchain-PoW-Consensus.git)

[//]: # (    cd Blockchain-PoW-Consensus)

[//]: # (    ```)

[//]: # ()
[//]: # (2. Ensure Python 3.7 or higher is installed. You can check your Python version with:)

[//]: # (    ```bash)

[//]: # (    python3 --version)

[//]: # (    ```)

[//]: # ()
[//]: # (3. Create a virtual environment:)

[//]: # (    ```bash)

[//]: # (    python3 -m venv venv)

[//]: # (    ```)

[//]: # ()
[//]: # (4. Activate the virtual environment:)

[//]: # (    - On Windows:)

[//]: # (        ```bash)

[//]: # (        venv\Scripts\activate)

[//]: # (        ```)

[//]: # (    - On macOS/Linux:)

[//]: # (        ```bash)

[//]: # (        source venv/bin/activate)

[//]: # (        ```)

[//]: # ()
[//]: # (5. Install the required dependencies:)

[//]: # (    ```bash)

[//]: # (    pip install -r requirements.txt)

[//]: # (    ```)

[//]: # ()
[//]: # (## Usage)

[//]: # (1. Run the application:)

[//]: # (    ```bash)

[//]: # (    python3 src/main.py)

[//]: # (    ```)

[//]: # ()
[//]: # (2. Use the GUI to configure the blockchain parameters and start the blockchain.)

[//]: # ()
[//]: # (## Configuration)

[//]: # (The following parameters can be configured through the GUI:)

[//]: # (- Initial Bit Difficulty)

[//]: # (- Target Block Mining Time)

[//]: # (- Adjustment Block Interval)

[//]: # (- Clamp Factor)

[//]: # (- Smallest Bit Difficulty)

[//]: # (- Number of Blocks to Add)

[//]: # (- Number of Blocks Slice)

[//]: # ()
[//]: # (## Contributing)

[//]: # (Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.)

[//]: # ()
[//]: # (## License)

[//]: # (This project is licensed under the GNU GENERAL PUBLIC LICENSE. See the `LICENSE` file for details.)

[//]: # ()
[//]: # ()
[//]: # ()



[//]: # (# Blockchain-PoW-Consensus)

[//]: # ()
[//]: # (Simple implementation of the Blockchain: Consensus Mechanism Proof-of-Work)

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
    python3 --version
    ```
    - If Python 3.6 or lower is installed, install Python 3.7 or higher. On macOS, you can install it via [Homebrew](https://brew.sh/):
      ```bash
      brew install python
      ```

3. Create a virtual environment:
    ```bash
    python3 -m venv venv
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
1. Run the application:
    ```bash
    python3 src/main.py
    ```

2. Use the GUI to configure the blockchain parameters and start the blockchain.

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
[//]: # (# Blockchain-PoW-Consensus)

[//]: # ()
[//]: # (Simple implementation of the Blockchain: Consensus Mechanism Proof-of-Work)

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

[//]: # (2. Ensure Python 3.7 or higher is installed. You can check your Python version with:)

[//]: # (    ```bash)

[//]: # (    python3 --version)

[//]: # (    ```)

[//]: # (    - If Python 3.6 or lower is installed, install Python 3.7 or higher. On macOS, you can install it via [Homebrew]&#40;https://brew.sh/&#41;:)

[//]: # (      ```bash)

[//]: # (      brew install python)

[//]: # (      ```)


2. Ensure Python 3.7 or higher is installed. You can check your Python version with:
    ```bash
    python3 --version
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
    python3 -m venv venv
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
1. Run the application:
    ```bash
    python3 src/main.py
    ```

2. Use the GUI to configure the blockchain parameters and start the blockchain.

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


