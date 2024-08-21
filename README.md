## miniEDA: A Tool for Simplifying Data Analysis, Preprocessing, and Quality Management

### Overview

**miniEDA** is a lightweight, user-friendly data exploration and analysis tool designed to simplify data preprocessing and quality management. Leveraging the power of `polars` for efficient data handling and `FastAPI` for seamless interactions, miniEDA aims to streamline exploratory data analysis (EDA) processes. The platform is designed with a session-based approach, enabling effective dataset management, transformation, and detailed logging of operations.

For an existing version using `streamlit`, please click [here](https://github.com/cpprhtn/miniEDA/tree/streamlit).

### Key Features

- **No-Code Data Preprocessing and Visualization**: miniEDA provides an intuitive interface for data transformations and visualizations without the need for coding, making it accessible to both technical and non-technical users.
- **Enhanced Data Quality Management**: The tool incorporates robust data quality checks, addressing completeness, timeliness, validity, accuracy, consistency, and uniqueness, to ensure high standards across datasets.
- **Session-Based Data Management**: The session-based architecture supports comprehensive data management and transformation history, facilitating reproducibility and efficient tracking of changes.

### Purpose

Data organizations often spend 30-40% of their time addressing data quality issues rather than focusing on value-adding tasks. miniEDA is designed to reduce these overheads by offering a reliable solution to common data quality problems. With its no-code interface, miniEDA empowers domain experts and non-developers to engage more actively with data, promoting more effective exploration and utilization. This approach not only democratizes data access but also boosts overall project efficiency and output.

### Installation

To install miniEDA, clone the repository and install the required dependencies. Python 3.11 or higher is recommended:

```sh
git clone https://github.com/cpprhtn/miniEDA.git
cd miniEDA
pip install -r requirements.txt
```

### Usage

To start the FastAPI server, run the following command:

```sh
uvicorn main:app --reload
```

Access the application in your web browser at `http://localhost:8000`.

### Contributing

We welcome contributions! Please fork the repository and submit a pull request with your changes. Ensure that your code adheres to the project's coding standards and includes relevant tests.

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

### Future Enhancements

- **Advanced Analytics**: Integration of machine learning and advanced statistical analysis features.
- **Enhanced Data Visualization**: Development of advanced data visualization and dashboarding capabilities.
- **Broader Integration**: Expansion to connect with additional data sources and storage solutions.

### Contact

For more information or to report issues, please visit the [issues](https://github.com/cpprhtn/miniEDA/issues) page or contact us directly.
