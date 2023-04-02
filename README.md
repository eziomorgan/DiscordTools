# DiscordTools

DiscordTools is a collection of useful tools for Discord, including chat completion, image generation, transcription, translation, and more.

## Installation

1. Clone the repository or download the source code.
2. Create a virtual environment by running `python3 -m venv venv` (or `python -m venv venv` on Windows).
3. Activate the virtual environment by running `source venv/bin/activate` on Linux/macOS or `venv\Scripts\activate` on Windows.
4. Install the required packages by running `pip install -r requirements.txt`.
5. Rename `config_bak.json` to `config.json` and update it with your own Discord token and OpenAI API key.

## Usage

The bot supports the following slash commands:

- `/agi chat_complete`: Perform Q&A chat completion using the GPT-3.5 Turbo model.
- `/agi imagine`: Generate an image from a text prompt.
- `/agi transcribe`: Transcribe an audio file using the Whisper-1 model.
- `/agi translate`: Translate an audio file from other languages to English using the Whisper-1 model.
- `/agi memento`: Clear the `chat_complete` history and reset the bot's memory to start a new conversation.

Additionally, the bot can automatically clear and delete chat messages in a channel.

To run the bot, execute the `launch.bat` file.

