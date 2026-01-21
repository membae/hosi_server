# Hosi Server

Hosi Server is the backend service for the **Hosi** application. It is responsible for handling authentication, core business logic, database operations, media uploads, and API communication with the frontend.

The server is built with **Python (Flask)** and follows a RESTful API architecture.

---

## 🚀 Features

* User authentication and authorization (JWT)
* User management (Admin / Doctor roles)
* Patient records management
* Appointment scheduling and management
* Medical reports creation with multiple images
* Cloudinary image upload and storage
* Relational database with clear entity relationships
* RESTful API architecture

---

## 🛠 Tech Stack

* **Backend Framework:** Flask
* **Database:** SQLite / PostgreSQL (configurable)
* **ORM:** SQLAlchemy
* **Authentication:** JWT
* **File Storage:** Cloudinary
* **Migrations:** Flask-Migrate
* **API Testing:** Thunder Client / Postman

---

## 📁 Project Structure

```text
hosi_server/
│
├── models.py          # Database models
├── app.py / run.py    # Application entry point & routes
├── migrations/        # Database migrations
├── instance/
│   └── config.py
│
├── static/
├── .env
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/hosi_server.git
cd hosi_server
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux / macOS
.venv\\Scripts\\activate   # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Variables

Create a `.env` file in the root directory and add:

```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///hosi.db
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
JWT_SECRET_KEY=your_jwt_secret
```

---

## 🗄 Database Setup

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

---

## ▶️ Running the Server

```bash
flask run
```

or

```bash
python run.py
```

The API will be available at:

```
http://127.0.0.1:5000
```

---

## 🔌 API Endpoints

### 🔐 Authentication

| Method | Endpoint  | Description                  |
| ------ | --------- | ---------------------------- |
| POST   | `/signup` | Register a new user          |
| POST   | `/login`  | Login and receive JWT tokens |

---

### 👤 Users

| Method | Endpoint     | Description    |
| ------ | ------------ | -------------- |
| GET    | `/users`     | Get all users  |
| GET    | `/user/<id>` | Get user by ID |
| PATCH  | `/user/<id>` | Update user    |
| DELETE | `/user/<id>` | Delete user    |

---

### 🧑‍⚕️ Patients

| Method | Endpoint        | Description       |
| ------ | --------------- | ----------------- |
| GET    | `/patients`     | Get all patients  |
| POST   | `/patients`     | Create patient    |
| GET    | `/patient/<id>` | Get patient by ID |
| PATCH  | `/patient/<id>` | Update patient    |
| DELETE | `/patient/<id>` | Delete patient    |

---

### 📅 Appointments

| Method | Endpoint            | Description                                  |
| ------ | ------------------- | -------------------------------------------- |
| GET    | `/appointment`      | Get all appointments                         |
| POST   | `/appointment`      | Create appointment                           |
| GET    | `/appointment/<id>` | Get appointments with doctor & patient names |
| PATCH  | `/appointment/<id>` | Update appointment                           |
| DELETE | `/appointment/<id>` | Delete appointment                           |

---

### 🧾 Reports & Images

| Method | Endpoint        | Description                        |
| ------ | --------------- | ---------------------------------- |
| GET    | `/reports`      | Get all reports                    |
| POST   | `/reports`      | Create report with multiple images |
| GET    | `/reports/<id>` | Get report by ID                   |
| PATCH  | `/reports/<id>` | Update report & images             |
| DELETE | `/reports/<id>` | Delete report                      |

---

## 📸 Image Upload (Cloudinary)

* Images are sent as `multipart/form-data`
* Stored securely on Cloudinary
* The returned URL is saved in the database and linked to related resources

---

## 🧪 Testing

```bash
pytest
```

(If tests are configured)

---

## 🧠 Common Issues

* Use `multipart/form-data` when uploading images
* Dates must be ISO format (e.g. `2025-01-21T10:00:00`)
* Ensure `patient_id` and `user_id` exist before creating records
* Run migrations after modifying models
* Check Cloudinary credentials if image uploads fail

---

## 🤝 Contributing

1. Fork the repository
2. Create a new branch (`feature/your-feature`)
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 🗂 Database Models

### User

* `id`, `first_name`, `last_name`, `email`, `password`, `role`
* Relationships: Appointments, Reports

### Patient

* `id`, `first_name`, `last_name`, `phone_number`, `status`
* `doctor_summary`, `diagnosis`, `admitted_at`, `discharged_at`
* Relationships: Appointments, Reports

### Appointment

* `appointment_datetime`, `status`, `reason`
* Foreign keys: `patient_id`, `user_id`

### Report

* `diagnosis`, `created_at`
* Foreign keys: `patient_id`, `user_id`
* One-to-many: Images

### Images

* `image_url`
* Foreign key: `report_id`

---

## 👤 Author

**Philip Memba**
Full‑Stack Developer
GitHub: [https://github.com/membae](https://github.com/membae)

---

> Hosi Server is the backbone of the Hosi platform — designed for scalability, security, and clean architecture.
