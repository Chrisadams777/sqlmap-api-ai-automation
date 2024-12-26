# **SQLMap API Scanner**

### Tagline: 
A robust tool for automating SQL injection tests using SQLMap via an easy-to-use API interface.

---

## **Overview**
SQLMap API Scanner is a powerful tool designed for penetration testing and automated SQL injection scanning. It interfaces with the popular SQLMap tool through a simple, efficient API, enabling you to easily integrate it into your workflows.

### **New Features:**
- **Enhanced Scan Management**: Seamless start, monitor, and retrieval of scan results via API endpoints.
- **Tamper History Management**: Ability to manage tamper history logs with reset and view options.
- **Task Handling**: Manage tasks through creation, deletion, and result extraction using simple API requests.

### **Why It's Better**:
- **Ease of Use**: Using an API makes SQL injection testing more accessible for automation, DevOps pipelines, or integration into larger security testing systems.
- **Scalability**: You can run multiple tasks concurrently without worrying about manually interacting with SQLMap.
- **Automation-Friendly**: Ideal for integrating into CI/CD pipelines or running repeated tests.

---

## **Installation**

### **1. Windows**

1. **Install Dependencies:**
   - Make sure **Python 3** is installed. You can download it from the [official website](https://www.python.org/downloads/).
   - Install **pip** (Python package installer) by running:
     ```bash
     python -m ensurepip --upgrade
     ```
   - Install **SQLMap** from [the official repository](https://github.com/sqlmapproject/sqlmap).

2. **Clone the Repository:**
   - Clone the repository using Git:
     ```bash
     git clone https://github.com/Chrisadams777/sqlmap-api-ai-automation.git
     cd sqlmap-api-scanner
     ```

3. **Install Required Python Packages:**
   - Install the necessary Python packages by running:
     ```bash
     pip install -r requirements.txt
     ```

4. **Run the API Server:**
   - Start the API server:
     ```bash
     python app.py
     ```

   The API will start running locally at `http://127.0.0.1:8775`.

---

### **2. macOS**

1. **Install Dependencies:**
   - Install **Homebrew** if it's not already installed. Use the following command in your terminal:
     ```bash
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
     ```
   - Install **Python** using Homebrew:
     ```bash
     brew install python
     ```
   - Install **SQLMap** using the following:
     ```bash
     git clone https://github.com/sqlmapproject/sqlmap.git
     ```

2. **Clone the Repository:**
   - Clone the repository with:
     ```bash
     git clone https://github.com/your-repository/sqlmap-api-scanner.git
     cd sqlmap-api-scanner
     ```

3. **Install Required Python Packages:**
   - Install the necessary Python packages by running:
     ```bash
     pip install -r requirements.txt
     ```

4. **Run the API Server:**
   - Start the API server:
     ```bash
     python app.py
     ```

   The API will start running locally at `http://127.0.0.1:8775`.

---

### **3. Linux**

1. **Install Dependencies:**
   - Make sure you have **Python 3** installed. You can install it using:
     ```bash
     sudo apt install python3
     sudo apt install python3-pip
     ```
   - Install **SQLMap** using:
     ```bash
     git clone https://github.com/sqlmapproject/sqlmap.git
     ```

2. **Clone the Repository:**
   - Clone the repository with:
     ```bash
     git clone https://github.com/your-repository/sqlmap-api-scanner.git
     cd sqlmap-api-scanner
     ```

3. **Install Required Python Packages:**
   - Install the necessary Python packages by running:
     ```bash
     pip3 install -r requirements.txt
     ```

4. **Run the API Server:**
   - Start the API server:
     ```bash
     python3 app.py
     ```

   The API will start running locally at `http://127.0.0.1:8775`.

---

### **4. Termux (Android)**

1. **Install Dependencies:**
   - Install **Python** in Termux:
     ```bash
     pkg install python
     pkg install git
     ```
   - Install **SQLMap** using:
     ```bash
     git clone https://github.com/sqlmapproject/sqlmap.git
     ```

2. **Clone the Repository:**
   - Clone the repository with:
     ```bash
     git clone https://github.com/your-repository/sqlmap-api-scanner.git
     cd sqlmap-api-scanner
     ```

3. **Install Required Python Packages:**
   - Install the necessary Python packages by running:
     ```bash
     pip install -r requirements.txt
     ```

4. **Run the API Server:**
   - Start the API server:
     ```bash
     python app.py
     ```

   The API will start running locally at `http://127.0.0.1:8775`.

---

## **Usage**

Once the API is running on your local server, you can use the endpoints for various tasks.

### **1. Start a New Scan**
To start a new scan, send a `GET` request to create a new task:
```bash
curl -X GET "http://127.0.0.1:8775/task/new"
```

### **2. Start Scan with Task ID**
To start a new scan, send a `GET` request to create a new task:
```bash
curl -X POST "http://127.0.0.1:8775/scan/{taskid}/start" -d '{"url": "http://example.com"}' -H "Content-Type: application/json"
```

### **3. Get Scan Status**
To start a new scan, send a `GET` request to create a new task:
```bash
curl -X GET "http://127.0.0.1:8775/scan/{taskid}/status"
```

