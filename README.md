# Self-Sovereign AI

Welcome to the Self-Sovereign AI poetry project! This repository houses a demonstration of the L402 protocol using langchain and streamlit. The project allows users to connect to their own OpenAI or Prem (assuming you have access to these services). The goal is to demonstrate a self-sovereign AI approach, where users can interact with AI models directly, ensuring data privacy and control.

## Table of Contents

- [Self-Sovereign AI](#self-sovereign-ai)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Demo](#demo)
  - [Contributing](#contributing)
  - [License](#license)

## Introduction

Self-Sovereign AI is a poetry project that showcases the integration of the L402 protocol, langchain, and streamlit. By running this project, users can experience a decentralized AI interaction, where they connect to their preferred AI models, such as OpenAI or Prem, without sharing data with third-party services.

The L402 protocol allows users to make requests to AI models via a proxy URL. Currently, two proxy options are supported: Aperture and Matador. Users are prompted to pay a Lightning invoice for accessing the AI model. Once the payment is made, the user receives a preimage, which they can then use to obtain the AI model's response.

## Installation

To set up the Self-Sovereign AI project on your local machine, follow these steps:

1. Clone the repository:

```bash
git clone https://github.com/yourusername/self-sovereign-ai.git
cd self-sovereign-ai
```

2. Install dependencies using Poetry:
```bash
poetry install
```

This will create a virtual environment and install all the required dependencies for the project.

## Usage
Once the installation is complete, you can run the Self-Sovereign AI project using the following command:

```bash
poetry run streamlit run main.py
```

This command will start the Streamlit application, and you can interact with the UI to connect to your desired AI model.

## Demo
In the Streamlit application, you will be prompted to select your preferred AI model (OpenAI or Prem). After that, you need to choose a proxy service (Aperture or Matador) to handle your AI requests. When you make a request to the AI model, a Lightning invoice will be generated, and you will be asked to make the payment using Lightning Network.

Once the payment is successful, you will receive a preimage. Copy this preimage and paste it into the application to get the AI model's response. The AI model will process your request without any intermediary, ensuring your data sovereignty and privacy.

Please note that to use the AI models (OpenAI or Prem), you must have valid access credentials for the respective services.

## Contributing
We welcome contributions to the Self-Sovereign AI project. If you find any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request. For major changes, it is recommended to discuss your ideas with the maintainers first.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

We hope you enjoy exploring the Self-Sovereign AI poetry project! If you have any questions or need assistance, please don't hesitate to reach out. Happy AI interactions!