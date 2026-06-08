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

# Interpreting Your Results (For My README)
The prompt requires you to interpret your RMSE relative to the 10% target:  
Your Results: Your model generated an RMSE of 14.2749 kg against a daily mean of 32.3656 kg, yielding an error percentage of 44.11%.
Interpretation: Because 44.11% is greater than 10%, the model currently exceeds the target error threshold.  
Why this happened & how to fix it: Because we are training on highly dynamic, simulated mock patterns with deliberate weekly variations, a basic Linear Regression model struggles to capture non-linear jumps smoothly. To drop that error below 10%, we can engineer additional calendar variables (such as flagging weekend drops directly) or upgrade our model to a RandomForestRegressor to track complex resource usage spikes better.  

# Hurdle 4
What is REST and why is it the standard for building APIs?

REST (Representational State Transfer) is an architectural standard that leverages standard stateless HTTP operations (like GET and POST) to enable independent software applications to seamlessly interact. It is the universal standard because it decouples the front-end interface from your back-end logic, ensuring your system is scalable, platform-agnostic, and incredibly lightweight to maintain.

What is the difference between a GET and a POST request? Which would you use to submit new billing data?

A GET request is designed exclusively to fetch or read information from a server without modifying any backend state. A POST request is explicitly designed to send data payloads to a server to create, append, or update resource states on the backend database. You must use a POST request to submit new billing data since you are introducing fresh entries into your data architecture.

Why run the API and dashboard as two separate processes rather than one combined script?

This enforces the architectural principle of Separation of Concerns. By running the data processing layer (FastAPI) separately from the user presentation interface (Streamlit), you protect your primary analytics engine. If a surge of web traffic overloads or crashes your Streamlit interface, your core data ingestion pipelines, storage services, and underlying machine learning inference services continue running securely without interruption.