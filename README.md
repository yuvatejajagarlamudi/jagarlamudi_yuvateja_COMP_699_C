# Street Issue Reporter

Street Issue Reporter is a web-based application developed using Django. The system allows residents to report street-related issues, enables municipal staff to manage assigned tasks, and provides an administrative panel for overseeing the entire workflow. The project is designed to improve communication, transparency, and response efficiency within city service operations.

## Project Overview

The application offers a structured method for submitting and managing public service requests. Residents can report issues with details and images, staff members can update the progress of assigned tickets, and administrators can manage users, assign tickets, and monitor system status. The project follows a three-role structure: Resident, Municipal Staff, and Administrator.

## Key Features

1. Resident registration and secure login  
2. Issue submission with description, location, and optional image  
3. Automated priority scoring based on predefined rules  
4. Ticket assignment by administrators  
5. Staff workflow for updating issue status  
6. Dashboard views tailored to each user role  
7. Ticket history download option  
8. RuleConfig system for modifying scoring rules  
9. Full ticket lifecycle tracking from submission to resolution  

## System Architecture

The project is built using Django’s Model-View-Template (MVT) architecture.  
The folder structure includes:

- accounts: user registration, authentication, and role management  
- tickets: issue reporting, ticket processing, priority scoring, and assignment  
- street_issue_reporter: project configuration and settings  
- templates: HTML files for all user interfaces  
- static: CSS files and supporting resources  
- db.sqlite3: default development database  

This layered organization helps maintain clarity and supports future scalability.

## Technology Stack

- Python and Django framework  
- SQLite database for development  
- HTML and CSS for interface layouts  
- Django built-in authentication for secure login  
- Git and GitHub for version control  

## Ticket Priority Logic

Ticket priority is computed automatically using the RuleConfig model.  
Priority is influenced by several factors:

- Issue description length  
- Presence of an uploaded image  
- Keywords that indicate urgency  
- Days overdue or pending  
- Overall severity indicators  

Administrators may adjust scoring rules as needed.

## User Roles

Resident: submits issues and views personal issue history  
Staff: handles assigned tickets and updates status  
Administrator: manages users, assigns tickets, configures rules, and monitors overall activity

## How to Run the Application

git clone https://github.com/yuvatejajagarlamudi/jagarlamudi_yuvateja_COMP_699_C.git
cd jagarlamudi_yuvateja_COMP_699_C
2. Create and Activate a Virtual Environment
python -m venv venv
venv\Scripts\activate




3. Install Required Packages
 pip install -r requirements.txt
4. Apply Database Migrations
python manage.py migrate

5. Start the Development Server
python manage.py runserver
Access the Application

Open your browser and go to:
http://127.0.0.1:8000/




CONCLUSION:
Street Issue Reporter provides a structured platform for reporting and managing community service issues.
The system enhances communication between residents and municipal staff, streamlines ticket handling, and improves administrative oversight.
This project offers a scalable foundation suitable for future enhancements and advanced civic management features.

