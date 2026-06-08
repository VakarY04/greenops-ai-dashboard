# greenops-ai-dashboard

# Hurdle 0
What is a Resource Group in Azure, and why do we use one?

It is a logical container that groups related Azure resources (like databases, virtual machines, or web apps) together. We use it to easily manage, monitor, and delete all components of a specific project at once.

What is the difference between a virtual environment and a global Python installation?

A global installation applies packages computer-wide, which can cause version conflicts between different projects. A virtual environment creates an isolated local sandbox for a specific project, ensuring dependencies don't interfere with other applications.

Why is version control important from Day 1 of a project?

It tracks every single change made to the codebase, allows you to roll back to previous working states if something breaks, facilitates seamless collaboration with team members, and acts as a secure backup.

# Hurdle 1
What does CO2e mean and why is it used as the standard unit for carbon accounting?

CO2e stands for Carbon Dioxide Equivalent. Different greenhouse gases (like methane or nitrous oxide) trap varying amounts of heat in the atmosphere. CO2e translates the impact of all different greenhouse gases into the equivalent amount of $CO_2$ based on their global warming potential, creating a single, standardized benchmark for tracking emissions.

Why is it important to separate emission factors by resource type rather than using a single flat rate?

Different hardware components have vastly distinct energy behaviors and carbon profiles. For instance, spinning up high-performance compute processors (CPUs) continuously draws significant power, whereas storing data on resting hardware blocks (Storage) consumes power differently over time. Splitting factors allows businesses to accurately pin down what is causing inefficiency and optimize effectively.

What is the most carbon-intensive service type in your dataset?

(Check your terminal output from step 7. Look at which service_type has the highest summed co2e_kg value and note it down here!)

# Hurdle 2 completed

# Hurdle 3
What is RMSE and what does a lower value indicate?   

Root Mean Squared Error (RMSE) measures the average magnitude of prediction errors made by a model. It calculates the square root of the average squared differences between predictions and actual values. Because errors are squared before averaging, RMSE penalizes large outliers heavily. A lower value indicates that the model's predictions align closer to true observations, signaling higher baseline accuracy.  

Why do we create lag features for time-series prediction instead of using the date directly?   

Standard machine learning models cannot interpret raw, continuously growing calendar dates effectively. Converting dates directly into numerical indexes often causes models to perform poorly outside the training range. In contrast, lag features structure the data to capture sequential dependencies and operational behaviors (e.g., "what happened on this day last week"), transforming a chronological series into a standard tabular setup that maps historic cyclical behaviors directly to future outputs.

What are the risks of using Linear Regression for this task? What assumptions does it make?   

Linear Regression assumes linearity (that relationships between features and emissions are direct straight lines), homoscedasticity (constant error variance), and independence of errors. The key risk here is that cloud workload carbon emissions are frequently non-linear—experiencing dramatic exponential spikes during large batches or scaling events that simple linear equations fail to track accurately.  

# Hurdle 4
What is REST and why is it the standard for building APIs?

REST (Representational State Transfer) is an architectural standard that leverages standard stateless HTTP operations (like GET and POST) to enable independent software applications to seamlessly interact. It is the universal standard because it decouples the front-end interface from your back-end logic, ensuring your system is scalable, platform-agnostic, and incredibly lightweight to maintain.

What is the difference between a GET and a POST request? Which would you use to submit new billing data?

A GET request is designed exclusively to fetch or read information from a server without modifying any backend state. A POST request is explicitly designed to send data payloads to a server to create, append, or update resource states on the backend database. You must use a POST request to submit new billing data since you are introducing fresh entries into your data architecture.

Why run the API and dashboard as two separate processes rather than one combined script?

This enforces the architectural principle of Separation of Concerns. By running the data processing layer (FastAPI) separately from the user presentation interface (Streamlit), you protect your primary analytics engine. If a surge of web traffic overloads or crashes your Streamlit interface, your core data ingestion pipelines, storage services, and underlying machine learning inference services continue running securely without interruption.

# Hurdle 5
Hurdle 5 was the final phase of the project: deploying the FastAPI backend API to Azure App Service (Linux) so it could host your machine learning model and serve live carbon metrics to your frontend dashboard.

The deployment initially failed because a broken GitHub Actions pipeline corrupted the cloud file workspace, leaving the application stuck on a continuous Not Found (404) error. Furthermore, hidden bugs like Linux case-sensitivity issues, missing package dependencies, and container startup shell crashes (source: not found) kept throwing Application Errors.

How We Cleared It
We systematically knocked down each blocker using a 4-step hands-on server patch:

Purged the Corrupted Files: Bypassed the broken pipeline by opening the Kudu File Manager to delete the stuck artifacts and drop the clean project folders directly into Azure's root web directory.

Fixed the Case-Sensitivity Bug: Renamed the lowercase api folder to an uppercase Python module (API) using Git to stop the case-sensitive Linux server from crashing on internal module imports.

Manually Built the Environment via SSH: Opened a live SSH tunnel straight into the active Linux container to manually create the missing virtual environment sandbox (python -m venv antenv) and run pip install -r requirements.txt directly on Azure's hardware.

The Final Result: The live /health link instantly went green returning {"status": "ok"}, allowing your local Streamlit dashboard to successfully connect and fetch real-time cloud analytics (0.42 kg CO2e)!