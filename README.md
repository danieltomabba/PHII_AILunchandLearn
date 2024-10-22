# PHII_AILunchandLearn
**Lunch & Learn: Deploying a Chat LLM System Using Python**

**Overview**
This learning guide will walk your colleagues—who have no prior experience in Python, AI, LLMs, or prompt engineering—through the step-by-step process of deploying a Chat LLM system. This is a hands-on experience designed to be playful and accessible, with every detail included for both macOS and Windows environments. The goal is for everyone to have a fully functional LLM system running on their computer by the end of the session.

---
**Training Outline**

1. **Setting up the Environment**
   - Python Installation (macOS & Windows)
   - Virtual Environment Setup
   - Installing Dependencies
   - Getting the OpenAI API Key
2. **Step-by-Step Guide to Building the Chat LLM App**
   - Application Overview
   - Code Walkthrough (app.py, templates, etc.)
   - Running the Application
3. **Prompts for Building Each Script**
4. **Hands-on Practice**

### Step 1: Environment Setup

**1. Install Python**

- **macOS**:

  1. Open Terminal (`Cmd + Space`, type "Terminal").
  2. Run the command to install Python:
     ```sh
     brew install python3
     ```
     *Prompt*: "How do I install Python on macOS using Terminal?"
  3. Verify installation:
     ```sh
     python3 --version
     ```
     *Prompt*: "How do I check if Python is installed on my Mac?"

- **Windows**:

  1. Download Python from [python.org](https://www.python.org/downloads/windows/).
  2. Run the installer, and make sure to check "Add Python to PATH".
     *Prompt*: "What are the steps to install Python on Windows and add it to PATH?"
  3. Verify installation by opening Command Prompt (`Win + R`, type "cmd"):
     ```cmd
     python --version
     ```
     *Prompt*: "How can I verify that Python is installed on Windows?"

**2. Create and Activate a Virtual Environment**

- **macOS**:

  1. Navigate to your working directory:
     ```sh
     cd ~/Desktop
     ```
  2. Create a virtual environment:
     ```sh
     python3 -m venv venv
     ```
     *Prompt*: "How do I create a virtual environment in Python on macOS?"
  3. Activate it:
     ```sh
     source venv/bin/activate
     ```
     *Prompt*: "How do I activate a Python virtual environment on macOS?"

- **Windows**:

  1. Navigate to your working directory:
     ```cmd
     cd Desktop
     ```
  2. Create a virtual environment:
     ```cmd
     python -m venv venv
     ```
     *Prompt*: "How do I create a virtual environment in Python on Windows?"
  3. Activate it:
     ```cmd
     venv\Scripts\activate
     ```
     *Prompt*: "How do I activate a Python virtual environment on Windows?"

**3. Install Dependencies**

- Both macOS and Windows:
  1. After activating the virtual environment, install the dependencies using the `requirements.txt` file:
     ```sh
     pip install -r requirements.txt
     ```
     *Prompt*: "How do I install all dependencies from a requirements.txt file?"
  2. If you don’t have `requirements.txt`, install the required libraries manually:
     ```sh
     pip install openai flask pandas matplotlib PyPDF2 python-dotenv
     ```
     *Prompt*: "What is the command to install Flask, Pandas, Matplotlib, PyPDF2, and python-dotenv using pip?"

**4. Obtain OpenAI API Key**

- Go to [OpenAI](https://platform.openai.com/account/api-keys) and generate your API key.
- Create a `.env` file in your project directory with the following format to store the API key securely:
  ```
  OPENAI_API_KEY=your_openai_api_key_here
  ```
  *Prompt*: "How do I create a .env file to securely store my OpenAI API key in a Python project?"

---

### Step 2: Building the Chat LLM Application

**1. Understand the Application Structure**

- **`app.py`**: The main Python script that runs the Flask application.
- **`templates/`**: HTML files that control how the application pages are rendered.
- **`static/`**: Stores static assets like images, JavaScript, and CSS.
- **`documents/`**: Stores uploaded documents for processing.

**2. Setting Up the Application**

- Copy all extracted files (`app.py`, `templates`, `static`, etc.) into your project folder on your desktop. Ensure the `.env` file is also in this directory.
- **Prompt for Setup**: "How do I organize a Python Flask project with templates and static files?"

**3. Running the Application**

- **macOS & Windows**:
  1. Make sure your virtual environment is activated.
  2. Run the application:
     ```sh
     python app.py
     ```
     *Prompt*: "How do I run a Flask application using Python?"
  3. Open a browser and navigate to `http://127.0.0.1:5001` to interact with the chat LLM.
     *Prompt*: "Where can I access my Flask application once it is running?"

**4. Example Prompts for Building the Application**

- To understand each component of the app, ask:
  ```
  What does the `app.py` script do in my Flask application? Explain each function and route.
  ```
- To understand how document uploads are handled:
  ```
  Explain the purpose of the `/upload` route in Flask.
  ```
- To know how the OpenAI API is integrated:
  ```
  How does the `/chat` route interact with the OpenAI API?
  ```

**5. Code Walkthrough**
- **Imports**: Explain why each import is necessary (e.g., Flask for the web framework, OpenAI for interacting with the API).
- **Routes**: Walk through each route in `app.py`.
  - `/upload`: Handles document uploads and stores them.
  - `/chat`: Sends the context to the OpenAI API and displays responses.
  - **Prompt for Context**: "How does Flask handle file uploads securely?"
- **Functions**: Discuss helper functions like `extract_text()` to extract content from uploaded documents.
  - **Prompt for Extraction**: "How can I extract text from different file types in Python?"

---

### Step 3: Hands-on Practice

**Exercise 1**: Upload and Chat
- Upload a sample document (e.g., a PDF with some text) and ask a question.
- **Prompt for Upload**: "How do I upload a file and interact with it using a chat feature in Flask?"

**Exercise 2**: Modify the HTML
- Add a personalized message or title to `index.html`.
  - **Prompt**: "How do I edit an HTML file to add a custom title in a Flask app?"

**Exercise 3**: Add a New Route
- Add a new route called `/about` that returns information about the application.
  - **Prompt**: "How do I add a new route in Flask to display an 'About' page?"

---

**Deployment Practice**

**1. Running on a Different Port**
- Modify `app.py` to run on a different port, like 8080:
  ```python
  if __name__ == '__main__':
      app.run(debug=True, host='127.0.0.1', port=8080)
  ```
  *Prompt*: "How do I change the port of my Flask application?"

**2. Creating a Batch File (Windows) and Shell Script (macOS) to Run the App**

- **Windows**:

  1. Open Notepad and paste the following script:
     ```cmd
     @echo off
     call venv\Scripts\activate
     python app.py
     pause
     ```
  2. Save it as `run_app.bat` on your desktop.
  3. Double-click the `.bat` file to run the application.
  - **Prompt**: "How do I create a batch file to automate running my Python app on Windows?"

- **macOS**:

  1. Open Terminal and create a new shell script:
     ```sh
     touch run_app.sh
     ```
  2. Edit the script:
     ```sh
     nano run_app.sh
     ```
  3. Add the following lines:
     ```sh
     #!/bin/bash
     source venv/bin/activate
     python app.py
     ```
  4. Save (`Ctrl + O`) and exit (`Ctrl + X`).
  5. Make the script executable:
     ```sh
     chmod +x run_app.sh
     ```
  6. Run it:
     ```sh
     ./run_app.sh
     ```
  - **Prompt**: "How do I create and run a shell script to automate my Python app on macOS?"

---

**Summary and Q&A**

- Recap: From installing Python and dependencies to running the app and interacting with an LLM.
- Emphasize that mistakes are okay—every error is a learning opportunity.
- Open the floor for questions, providing playful analogies if needed (e.g., "The virtual environment is like putting on your lab coat before experimenting—keeps things clean!").

**Follow-up Resources**

- **Python Basics**: [Learn Python](https://www.learnpython.org/)
- **Flask Documentation**: [Flask Docs](https://flask.palletsprojects.com/)
- **OpenAI API Guide**: [OpenAI API Documentation](https://beta.openai.com/docs/)

**Next Steps**

- Encourage colleagues to extend the app—maybe add a feature to analyze uploaded text sentiment.
- Plan a follow-up session in a month to review progress and celebrate everyone's learning achievements!

