# jagarlamudi_yuvateja_COMP_699_C

## Street Issue Reporter   

**Project Name:** Street Issue Reporter  
**Author:** Yuva Teja Jagarlamudi  
**Course:** COMP 699 C – Systems Analysis and Design  
**Instructor:** Professor David Pitts  

---

### System Request  
The Street Issue Reporter project was created to help residents quickly report problems such as potholes, broken streetlights, and damaged sidewalks to municipal authorities. Current methods, like phone calls or emails, often cause delays in response and repair times. This system provides a faster and more transparent reporting process through a web-based platform.  

Residents can log in, upload images, select a location, and describe the issue. Municipal staff can view, prioritize, and update tickets, while the admin monitors overall performance and escalations. The system improves communication, speeds up issue resolution, and demonstrates realistic municipal workflows for academic learning.  

**Business Need:** Automate and streamline the street issue reporting process.  
**Business Requirements:**  
- Residents can submit, view, and manage issue reports.  
- Staff can view and update ticket statuses.  
- Admin can configure rules, assign tasks, and generate reports.  

**Expected Benefits:** Faster response, improved safety, and better transparency.  
**Constraints:** Must run locally without paid APIs or external hosting.  

---

### 6. Preliminary Design and Implementation Thoughts  
The preliminary design for the Street Issue Reporter system focuses on simplicity, modularity, and scalability for local demonstration. The user interface will be developed using **HTML and CSS** to create a clean and easy-to-navigate layout for residents, municipal staff, and administrators. The backend will be powered entirely by the **Flask framework in Python**, which is chosen for its lightweight structure, simplicity, and strong support for rapid web application development. A **MySQL database** will be used to manage ticket, user, and notification data securely and efficiently.  

The system will follow the **Model-View-Controller (MVC)** design pattern to separate business logic, interface elements, and database operations. The implementation will be completed incrementally, beginning with user registration and login, followed by issue submission, dashboard functionality for staff, and rule-based ticket prioritization. Reporting features and system testing will be conducted in later phases to validate performance, usability, and accuracy in a local environment.  

---

### Technical Overview  
- **Frontend:** HTML, CSS  
- **Backend:** Python Flask Framework  
- **Database:** MySQL  
- **Deployment:** Localhost environment for classroom demonstration  
- **Version Control:** Managed through GitHub Repository  
- **Privacy and Security:** User data and uploaded images stored securely using role-based access controls.  

---

### Future Enhancements and Learning Goals  
As part of future development, this system can be enhanced with **real-time issue tracking** using location-based APIs and **AI-driven image classification** to automatically identify and categorize reported problems such as potholes or damaged lights. Additionally, integrating **email notifications** or **SMS alerts** for residents when their issues are resolved will increase transparency and engagement.  

From an academic perspective, this project has provided strong hands-on learning in **system analysis, UML modeling, and full-stack development** using Python Flask. It demonstrates how effective design and structured implementation can solve real-world civic problems and improve urban safety through technology-driven communication.  

---

