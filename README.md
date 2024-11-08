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

2. Create a virtual environment:
    ```bash
    python -m venv venv
    ```

3. Activate the virtual environment:
    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

4. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. Run the application:
    ```bash
    python src/main.py
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



