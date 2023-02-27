# TGParserVisualizer - Visualize your Telegram chat history
🚀🐍💬 TGParserVisualizer is Python script that can help you create word clouds and tables from your Telegram chat history! 📊 With its features, you can easily analyze your chat data and gain insights into your communication patterns! 👥

## How to Use ?

Before you can start visualizing your Telegram chat history, you need to export your chat history from Telegram. Here's how:
* Open Telegram and go to the chat, bot, channel, or group whose chat history you want to export.
* Click on the three dots menu at the top right corner of the chat window.
* Select "Export chat history" from the menu.
* Choose the format in which you want to export your chat history (e.g. HTML) and select the date range for which you want to export the chat history.
* Click "Export" to save the chat history to your computer.
* Once you've exported your chat history, you need to copy all the HTML files to the "messages" folder located in "/downloads/Telegram/Telegram Desktop/Chat_Export/".


### Environment Setup

Download Python 3.10. While other versions may work, compatibility cannot be guaranteed.

&emsp; 1. Create a new virtual environment by running the following command:<br />
	&emsp;&emsp;&emsp;```python -m venv myenv```

&emsp; 2. Activate the virtual environment. Depending on your operating system, use one of the following commands:<br />
    &emsp;On Windows:<br />
        &emsp;&emsp;```myenv\Scripts\activate.bat```<br />
    &emsp;On Unix or Linux:<br />
        &emsp;&emsp;`source myenv/bin/activate`<br />

3. Install the required modules listed in the requirements.txt file by running the following command:

	`pip install -r requirements.txt`


### Parsing and Visualizing
Once you have your chat history exported and the HTML files copied to the "messages" folder, you can start parsing and visualizing your chat history with TGParserVisualizer.

### 💻Parsing 
The first step is to parse the messages and save them to a file. To do this, open the command prompt and navigate to the folder where you downloaded TGParserVisualizer. Then, run the following command:<br />
&emsp;`python main.py -a parse`

After parsing, a file named "users.txt" will be generated. This file contains a list of all the users in your chat history. You can remove users that you don't want to include in the visualization by deleting their names from the "users.txt" file.

### 💭Word Cloud
To generate a word cloud image, run the following command:<br />
`main.py -a image --dpi 300 --len 3 --max_words 100`

You can adjust the parameters to customize the word cloud image: <br />
&emsp;`--dpi`: Change the DPI of the image to get a more informative image (default is 300).<br />
&emsp;`--len`: Change the minimum length of the words in the image (default is 3).<br />
&emsp;`--max_words`: Change the maximum count of words in the image. Be cautious when increasing this value, as larger numbers will slow down the process.<br />
For example, you can run the following command to generate an image with a DPI of 320, a minimum word length of 4, and a maximum word count of 200:

&emsp;`main.py -a image --dpi 320 -l 4 -m 200`

### 📊Table
To generate a table, run the following command:

&emsp;`main.py -a table --columns 10 --unic_words --len 3`


You can adjust the parameters to customize the table:<br />
&emsp;--columns: Change the number of columns in the table (default is 10).<br />
&emsp;--unic_words: If this flag is set, only words in "unicwords.txt" will be returned.<br />
&emsp;--len: Change the minimum length of the words in the table (default is 3).<br />

For example, you can run the following command to generate a table with 15 columns, a minimum word length of 4, and only words in "unicwords.txt":<br />
&emsp;`main.py -a table -c 15 -l`