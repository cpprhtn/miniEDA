## miniEDA: A Tool for Simplifying Data Analysis, Preprocessing, and Quality Management

### Overview

**miniEDA** is a lightweight, user-friendly data exploration and analysis tool that leverages the power of `polars` and `FastAPI`. Designed to streamline the process of exploratory data analysis (EDA), miniEDA allows users to perform various data preprocessing and quality assessment tasks efficiently. The tool emphasizes a session-based approach, enabling seamless management and transformation of datasets with detailed logging of each operation.
If you would like to check the existing `streamlit` version, please click [here](https://github.com/cpprhtn/miniEDA/tree/streamlit).

### Key Features

- **No-Code Data Preprocessing and Visualization**: miniEDA allows users to perform data transformations and visualize data easily without writing code, making it accessible to non-technical users.
- **Focus on Data Quality**: The tool incorporates considerations for data quality, including completeness, timeliness, validity, accuracy, consistency, and uniqueness, ensuring high standards are met across datasets.
- **Session-Based Data Management and Logging**: Sessions store datasets and their transformation history, ensuring reproducibility and enabling users to track changes and reapply operations systematically.

### Purpose

In many data organizations, it is estimated that 30-40% of time is spent addressing data quality issues rather than focusing on value-adding activities. miniEDA aims to reduce these costs by providing a reliable tool that mitigates common data quality problems. Furthermore, by offering a user-friendly, no-code interface, the project enables non-developers to actively engage with data, allowing domain experts to explore and utilize data more effectively. This not only democratizes data usage but also enhances the overall efficiency and output of data-driven projects.

### Installation

To install miniEDA, clone the repository and install the necessary dependencies. Python 3.11 or higher is recommended:

```sh
git clone https://github.com/cpprhtn/miniEDA.git
cd miniEDA
pip install -r requirements.txt
```

### Build frontend

Build frontend with gatsby by running:

```sh
cd frontend
npm install
npm run build
```

This will generate a `public` directory inside the `frontend` directory. The files built during this step are served by FastAPI, which references them to deliver the frontend.

### Run

Start the FastAPI server by running:

```sh
uvicorn main:app --reload
```

Then, access the application in your web browser at `http://localhost:8000`.

### Contributing

We welcome contributions! Please fork the repository and submit a pull request with your changes. Ensure your code adheres to the project's coding standards and includes appropriate tests.

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

### Future Enhancements

- **Advanced Analytics**: Adding machine learning and statistical analysis capabilities.
- **Data Visualization**: Enhanced support for data visualization and dashboarding.
- **Integration**: Connect with more data sources and storage solutions.

### Contact

For more information or to report issues, please visit the [issues](https://github.com/cpprhtn/miniEDA/issues) page.
