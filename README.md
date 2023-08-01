# Self-Sovereign AI

Welcome to the Self-Sovereign AI project! This repository houses a demonstration of the L402 protocol using langchain and streamlit.

Unfortunately there are some problems on the Replit dependencies, so at the moment it only works locally. 

The application allows you to chat with ChatGPT through an OpenAI api key or with Prem.AI models if you have an instance running with a GPU.

If you do not have an API key or a Prem instance, you can still chat with OpenAI through a 402 Proxy. 
Set the desired proxy and for each request you will be prompted to pay an invoice and paste the pre-image of the payment.
After that you can enjoy calls to OpenAI without the need to set up a credit card! 
Be Self-Sovereign!


## Table of Contents

- [Self-Sovereign AI](#self-sovereign-ai)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Proxy 402](#proxy-402)
  - [Demo](#demo)
  - [License](#license)

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


## Proxy 402

- [Matador](https://github.com/Kodylow/matador)
- [Aperture](https://github.com/lightninglabs/aperture)

To use Aperture you need to connect an LND node and have a passthrough service to OpenAI, here you can find a simple server that does that. https://github.com/waltermaffy/self-sovereign-ai/blob/main/openai_server.py


## Demo

[YouTube Demo - Streamlit L402 ChatBot](https://www.youtube.com/watch?v=MT-L4b5x8Ls)


In the Streamlit application, you will be prompted to select your preferred AI model (OpenAI or Prem). After that, you need to choose a proxy service (Aperture or Matador) to handle your AI requests. When you make a request to the AI model, a Lightning invoice will be generated, and you will be asked to make the payment using Lightning Network.

Once the payment is successful, you will receive a preimage. Copy this preimage and paste it into the application to get the AI model's response. The proxy will check if the payment has been made and if paid will forward the request to the AI model. The AI model will then generate a response, which will be displayed in the application.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
If you have any questions or need assistance, please don't hesitate to reach out.


\#AI4ALL