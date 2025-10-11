Magic Shell - Softablitz 2025

This repository contains the Magic Shell application developed for Softablitz 2025 hackathon.
Description

Magic Shell is a natural language command interpreter that converts human-friendly instructions into shell commands using AI/NLP techniques. It includes both a GUI and CLI version.

Contents

   * dist/ - https://drive.google.com/drive/folders/16iFxgn_U2WyevcjM_wtNQWWaaf2jVnzs?usp=drive_link

   * docs - ...

How to Use

Running the GUI

    Extract the ZIP file.

    Navigate to dist folder.

    Run main.exe (on Windows).

Running the CLI

    Extract the ZIP file.

    Go to the dist folder.

    Run main_cli.exe via terminal.

Ollama Server Integration

Magic Shell leverages the Ollama server to run AI models locally, providing powerful natural language processing capabilities.
What you need to know

    Ollama Server: The system requires an Ollama server instance running locally or accessible remotely to serve the AI models.

    Model Setup: Before running Magic Shell, ensure you have pulled the necessary AI model(tinyllama) using Ollama tooling.



Starting Ollama Server: Run the Ollama server on your machine:

    text
    ollama serve

    or provide the server address in your app configuration environment variable OLLAMA_HOST.

    Configuration: You can customize Ollama server URL and access tokens in your app’s settings to connect to the appropriate endpoint.

Benefits

    Running Ollama locally keeps all AI processing private and does not send data to external cloud services.

    Allows for faster, reliable, and customizable AI model interaction within Magic Shell
