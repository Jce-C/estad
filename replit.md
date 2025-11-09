# Overview

This is a web-based statistical analysis application built with Python and Streamlit. The application enables users to perform descriptive statistical analysis on datasets through automated calculations and interactive visualizations. It targets educational use, specifically for Statistics I coursework in Systems Engineering.

The application supports both quantitative (numerical) and qualitative (categorical) data types, automatically detects data characteristics using AI (OpenAI GPT-5), and provides comprehensive statistical measures including central tendency, dispersion metrics, and frequency distributions. Users can input data manually, upload files (CSV, TXT, XLSX), or use pre-loaded examples.

# User Preferences

Preferred communication style: Simple, everyday language.

# Recent Changes (November 2025)

## Replit Environment Setup (November 9, 2025)
- Configured Streamlit to run on port 5000 with proper host settings for Replit
- Created `.streamlit/config.toml` for production-ready configuration
- Set up UV-based workflow for dependency management
- Configured deployment for autoscale target
- Added comprehensive Python .gitignore

**UI/UX Redesign:**
- Simplified navigation: Reduced to 2 main tabs ("Inicio" and "Manual de Usuario")
- Integrated workflow: Data input and analysis results now on single scrollable page
- Right-aligned sidebar: Information panel moved to right side for better ergonomics
- Floating AI chat widget: Interactive assistant bubble in lower-left corner accessible via button
- Floating "Ver Análisis" button: Quick navigation to results section when data is loaded
- Auto-scroll behavior: Visual indicators guide users to analysis section
- Reorganized input section: Examples moved below manual input for improved workflow

# System Architecture

## Frontend Architecture

**Technology Stack**: Streamlit for web interface
- **Design Pattern**: Single-page scrollable application with minimal tab navigation
- **Styling**: Custom CSS embedded in `app.py` for metric cards, headers, chat widget, and sidebar positioning
- **Layout**: Wide layout with right-aligned expandable sidebar for better data visualization
- **Rationale**: Streamlit chosen for rapid prototyping and built-in interactivity without frontend framework complexity

**UI Components**:
- Data input section supporting multiple formats (manual text, file upload, pre-loaded examples)
- Floating AI chat widget (bottom-left) for contextual help and data interpretation
- Interactive statistical displays using custom-styled metric cards
- Dynamic visualization panels using Plotly for charts
- Auto-scroll functionality to results section after data loading

## Backend Architecture

**Modular Design**: Separated concerns across multiple Python modules
- `app.py`: Main application entry point and UI orchestration
- `stats_utils.py`: Statistical calculations (central tendency, dispersion)
- `data_processor.py`: Data loading, validation, and frequency table generation
- `visualization.py`: Chart generation using Plotly
- `ai_helper.py`: OpenAI integration for data type detection and interpretation

**Data Processing Pipeline**:
1. Data ingestion (text parsing or file reading)
2. Data validation and cleaning
3. Type detection (AI-powered with fallback)
4. Statistical computation
5. Visualization generation
6. AI-powered interpretation (optional)

**Rationale**: Modular architecture enables independent testing, easier maintenance, and clear separation of statistical logic from presentation logic.

## Statistical Computation

**Libraries Used**:
- NumPy: Numerical operations
- Pandas: Data manipulation and series handling
- SciPy: Advanced statistical functions (mode calculation)

**Key Features**:
- Automatic interval calculation using Sturges' Rule for quantitative data
- Support for both sample and population statistics
- Frequency tables with absolute, relative, percentage, and cumulative frequencies
- Comprehensive dispersion metrics (range, variance, standard deviation, IQR, coefficient of variation)

**Design Decision**: Used scipy.stats for statistical functions to ensure accuracy and leverage well-tested implementations rather than custom algorithms.

## AI Integration Strategy

**Primary AI Feature**: Data type classification
- **Model**: OpenAI GPT-5 (latest model as of August 2025)
- **Purpose**: Automatically determine if data is quantitative/qualitative and identify subtypes
- **Input**: Sample of first 20 data points
- **Output**: JSON response with type, subtype, and reasoning

**Secondary AI Feature**: Statistical interpretation
- Generates human-readable explanations of calculated statistics
- Provides context and insights about the data

**Fallback Mechanism**: 
- Built-in rule-based detection when OpenAI API is unavailable
- Attempts numeric conversion to classify as quantitative
- Defaults to qualitative for non-numeric data
- Rationale: Ensures application functionality without external dependencies

**API Key Management**: Environment variable `OPENAI_API_KEY` with graceful degradation

## Visualization Approach

**Library**: Plotly for interactive charts
- Histogram: Quantitative data distribution
- Bar charts: Categorical frequency visualization  
- Pie charts: Proportional representation
- Box plots: Quartile and outlier analysis

**Design Choice**: Plotly selected over Matplotlib for interactivity (hover tooltips, zoom, pan) which enhances educational value for students exploring statistical concepts.

## Data Validation & Error Handling

**Validation Strategy**:
- Type checking and conversion attempts (numeric vs. string)
- Empty data detection
- Delimiter auto-detection (comma, semicolon, tab, space, newline)
- File format validation

**Error Handling**: Try-except blocks with user-friendly error messages throughout data processing pipeline

# External Dependencies

## AI Services

**OpenAI API**
- Purpose: GPT-5 model for data type detection and statistical interpretation
- Authentication: API key via `OPENAI_API_KEY` environment variable
- Model: `gpt-5` (released August 7, 2025)
- Fallback: Application continues functioning without API access using rule-based logic

## Python Packages

**Core Framework**:
- `streamlit`: Web application framework

**Data Processing**:
- `pandas`: DataFrame operations and data manipulation
- `numpy`: Numerical computations
- `scipy`: Statistical functions (specifically `scipy.stats`)

**Visualization**:
- `plotly`: Interactive chart generation (`plotly.graph_objects`, `plotly.express`)

**File Handling**:
- `openpyxl` (implicit): Excel file support through pandas

**Standard Library**:
- `io`: In-memory file operations
- `json`: JSON parsing for AI responses
- `os`: Environment variable access
- `base64`: Data encoding (if needed for file downloads)

## File Format Support

**Input Formats**:
- CSV files (comma-separated values)
- TXT files (various delimiters)
- XLSX/XLS files (Microsoft Excel)
- Manual text input (flexible delimiter detection)

**Sample Data**:
- Pre-generated example datasets in `ejemplos_datos/` directory
- Includes quantitative examples (ages, grades, heights, incomes)
- Includes qualitative examples (colors, satisfaction levels)

## No Database Dependency

The application operates in-memory with no persistent database. All data processing is session-based through Streamlit's state management.