# Event Planning Software

## Disclaimer
This version of the project is based on the original work by Marcelo Palmeira.
All credits for the initial version go to the original author. This repository aims to refactor and restructure the code for learning and improvement purposes.

## Overview
This project is an event management system that allows you to create, edit, list, and delete events, as well as manage participants, speakers, vendors, feedback, and budgets. The application includes a REST API built with Flask, a web front-end using Jinja2 templates (with modular CSS files for each component), and a terminal-based client for direct interaction.

## 🔍 Design Patterns Implementation

**The main purpose of this project is to demonstrate the implementation of key design patterns in a real-world application:**

### Creational Patterns
- **Factory Pattern**: Implemented in the `EntityFactory` class to create domain objects (events, participants, speakers, etc.) with a consistent interface, promoting loose coupling and allowing for future extensions of entity types.

### Structural Patterns
- **Facade Pattern**: Implemented in the service layer (`EventService`, `ParticipantService`, etc.) to provide a simplified interface to the complex subsystem of repositories, models, and notifications. This pattern significantly reduces client-subsystem coupling.
- **Repository Pattern**: Used to abstract the data access layer, providing a collection-like interface for domain objects and decoupling the business logic from data persistence concerns.

### Behavioral Patterns
- **Observer Pattern**: Implemented in the notification system to establish a publisher-subscriber relationship, allowing multiple objects to be notified when state changes occur, without tight coupling between components.

## Requirements Implemented

- ✅ **Event Creation and Management**: Create, edit, and manage event details
- ✅ **Attendee Registration**: Register and manage event participants
- ✅ **Speaker and Performer Profiles**: Manage profiles and information for speakers
- ✅ **Vendor Management**: Coordinate with vendors for services like catering and equipment
- ✅ **Feedback and Survey Tools**: Collect attendee feedback post-event
- ✅ **Budget and Financial Management**: Track and manage event budgets and expenses

## Technical Scope Limitations

Some features were considered but excluded from implementation due to technical constraints:

- Email delivery functionality (while notification infrastructure is in place using the Observer pattern)
- External system integrations (venue booking, payment processing)
- Authentication flows required for social media integration
- Complex temporal data modeling for detailed schedules

These features would add significant complexity without contributing to the primary goal of demonstrating design patterns.

## Prerequisites

- Python 3.8+ ([Download Python](https://www.python.org/downloads/))
- PostgreSQL 12+ ([Download PostgreSQL](https://www.postgresql.org/download/))

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/tcheld0n/Event-Planning-Software.git
cd Event-Planning-Software
```

### 2. Create a virtual environment (optional but recommended)

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install flask psycopg2-binary sqlalchemy
```

or if a requirements.txt file exists:

```bash
pip install -r requirements.txt
```

### 4. Install and configure PostgreSQL

1. Download and install PostgreSQL from: https://www.postgresql.org/download/
2. During installation:
   - Set password to `123456` for the postgres user
   - Keep the default port `5432`
   - Complete the installation

## Running the System

### First-time use or after PostgreSQL installation

Follow these steps for first-time execution or after installing PostgreSQL:

1. **Verify PostgreSQL installation**:
   ```bash
   python utils/check_postgres_simplified.py
   ```
   This script checks if PostgreSQL is installed and functioning correctly.

2. **Start the system**:
   ```bash
   python main.py
   ```
   This command checks the database, creates necessary tables, and starts the web server. Access http://localhost:5000 in your browser.

### Regular use

For subsequent uses, simply run:

```bash
python main.py
```

### System Maintenance

#### Troubleshooting PostgreSQL connection issues

If you encounter connection problems with PostgreSQL:

```bash
python utils/fix_postgres.py
```

This script diagnoses and attempts to fix common PostgreSQL issues.

#### Clearing system data

To clear all data and start fresh (preserving the structure):

```bash
python utils/reset_tables.py
```

## Project Structure

```
EVENT-PLANNING-SOFTWARE/
├── src/                      # Main source code
│   ├── controllers/          # Request handlers
│   ├── models/               # Domain models (entities)
│   ├── repositories/         # Data access (Repository pattern)
│   ├── services/             # Business services (Facade pattern)
│   ├── factory/              # Object creation (Factory pattern)
│   ├── database/             # Database configuration
│   └── notifications/        # Notification system (Observer pattern)
│
├── utils/                    # Utilities and tools
│   ├── create_table.py       # Database and table creation
│   ├── reset_db.py           # Complete database reset
│   ├── reset_tables.py       # Clear table data
│   ├── check_postgres.py     # PostgreSQL installation verification
│   └── fix_postgres.py       # PostgreSQL troubleshooting
│
├── static/                   # Static files (CSS, JS)
├── templates/                # HTML templates
├── app.py                    # Flask application
├── main.py                   # Application entry point
├── README.md                 # Documentation
└── requirements.txt          # Project dependencies
```

## Features

### Events
- Create events with name, date, and budget
- List registered events
- Edit event details
- Delete events

### Participants
- Register participants for specific events
- List participants by event
- Update participant information
- Remove participants

### Speakers
- Register speakers with name and description
- List speakers by event
- Update speaker information
- Remove speakers

### Vendors
- Register vendors with offered services
- List vendors by event
- Update vendor information
- Remove vendors

### Budget
- View event budgets
- Update budget
- Edit budget value

### Feedback
- Add feedback for events
- View received feedback

## Conclusion

This system demonstrates the implementation of various creational, structural, and behavioral design patterns in a Python application with Flask and PostgreSQL. The focus is on code organization, separation of concerns, and proper implementation of design patterns.

The implemented architecture provides a solid foundation for future expansion of features, such as integration with payment systems for ticket sales or social media APIs for event promotion.

## License

[MIT](LICENSE)
