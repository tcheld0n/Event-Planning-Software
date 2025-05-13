# Event Manager Software

This project is an event management system that allows you to create, edit, list, and delete events, as well as manage participants, speakers, vendors, feedback, and budgets. The application includes a REST API built with Flask, a web front-end using Jinja2 templates (with modular CSS files for each component), and a terminal-based client for direct interaction.

**Run create_table.py to create the database structure and remember to configure db.py**
---

## Features

### Event Management
- **Create Event:** Add a new event by providing its name, date (in DD-MM-YYYY format), and initial budget.
- **Edit Event:** Modify event details such as name, date, and budget.
- **List Events:** Display all registered events.
- **Delete Event:** Remove an event from the system.

### Participant Management
- **Register Participant:** Associate a participant with an event.
- **List Participants:** Display all participants registered for an event.
- **Edit Participant:** Update the name of a participant.

### Speaker/Performer Management
- **Register Speaker:** Add a speaker/performer to an event with a description.
- **List Speakers:** Show all speakers registered for an event.
- **Edit Speaker:** Edit a speaker’s details while retaining original information if a field is left blank.

### Vendor Management
- **Register Vendor:** Add a vendor by providing its name and the services/products offered.
- **List Vendors:** Display all vendors associated with an event.
- **Edit Vendor:** Update vendor details while retaining original information if a field is left blank.

### Feedback & Surveys
- **Submit Feedback:** Allow attendees to leave feedback for an event.

### Budget & Financial Management
- **Update Budget:** Increase the event’s budget by adding a specified amount.
- **View Budget:** Retrieve the current budget for an event.
- **Edit Budget:** Overwrite the event’s budget with a new value, retaining the original if no new value is provided.

## Checklist of Implemented and Missing Features

### Implemented Features
- ✅ **Event Creation and Management:** Users can create, edit, list, and delete event details.
- ✅ **Attendee Registration:** Participants can be registered and listed for events.
- ✅ **Speaker & Performer Management:** Speakers/Performers can be registered, listed, and edited.
- ✅ **Vendor Management:** Vendors can be registered, listed, and edited.
- ✅ **Feedback & Surveys:** Attendees can submit feedback for events.
- ✅ **Budget & Financial Management:** Users can update, view, and edit event budgets.
- ✅ **Schedule and Agenda Management:** Event creation includes scheduling via dates.

### Missing Features
- ❌ **Venue Booking:** Not implemented because it would require using a real booking platform like Airbnb, which is not ideal for an academic project.
- ❌ **Social Media Integration:** Not implemented due to lack of time.
- ❌ **Email and Notification System:** Not implemented due to lack of time.

---

## Technologies Used

- **Back-end:** Flask, SQLAlchemy (for ORM and database management), Python.
- **Front-end:** Flask Templates (Jinja2), HTML5, CSS (modular CSS files for each component).
- **Terminal Client:** A Python client (`event_client.py`) for terminal-based interaction.
- **Other Libraries:** Requests (for HTTP communication in the client).

---

## Project Structure

```plaintext
.
├── README.md
├── app.py
├── client
│   └── event_client.py
├── controllers
│   ├── budget_controller.py
│   ├── event_controller.py
│   ├── feedback_controller.py
│   ├── participant_controller.py
│   ├── speaker_controller.py
│   └── vendor_controller.py
├── database
│   └── db.py
├── models
│   ├── event.py
│   ├── participant.py
│   ├── speaker.py
│   └── vendor.py
├── requirements.txt
├── services
│   ├── base_service.py
│   ├── event_service.py
│   ├── feedback_service.py
│   ├── participant_service.py
│   ├── speaker_service.py
│   └── vendor_service.py
├── templates
│   ├── index.html
│   ├── criar_evento.html
│   ├── eventos.html
│   ├── editar_evento.html
│   ├── registrar_participante.html
│   ├── participantes.html
│   ├── editar_participante.html
│   ├── registrar_palestrante.html
│   ├── palestrantes.html
│   ├── editar_palestrante.html
│   ├── registrar_fornecedor.html
│   ├── fornecedores.html
│   ├── editar_fornecedor.html
│   ├── atualizar_orcamento.html
│   ├── ver_orcamento.html
│   ├── editar_orcamento.html
│   └── adicionar_feedback.html
├── static
│   └── css
│       ├── styles.css
│       ├── index.css
│       ├── criarEvento.css
│       ├── listarParticipantes.css
│       ├── registrarParticipantes.css
│       ├── registrarPalestrantes.css
│       ├── listarPalestrantes.css
│       ├── registrarFornecedores.css
│       ├── listarFornecedores.css
│       ├── atualizarOrcamento.css
│       ├── verOrcamento.css
│       ├── editarOrcamento.css
│       └── adicionarFeedback.css
└── views
