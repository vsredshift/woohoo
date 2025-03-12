# Woohoo Blog

Woohoo Blog is a fictional blog website where users can log in to read, like, comment on, and save posts. Staff members can update existing posts or create new ones.

This project is based on the [Django Documentation](https://docs.djangoproject.com/en/stable/) tutorial,  
with additional structure and styling inspired by Corey Schafer's YouTube channel.

---

## 🚀 Features

- ✅ User authentication (login, logout, registration)
- ✅ Create, read, update, and delete (CRUD) functionality for blog posts
- ✅ Like and save posts
- ✅ Nested commenting system (users can reply to replies)
- ✅ Staff can manage blog content

---

## 🛠 Installation & Setup

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/vsredshift/woohoo.git
cd woohoo
```

### 2️⃣ Set Up a Virtual Environment (Optional but Recommended)
```sh
python -m venv .venv
source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 4️⃣ Configure the Database
```sh
python manage.py migrate
```

### 5️⃣ Create a Superuser (Admin)
```sh
python manage.py createsuperuser
```
Follow the prompts to create an admin account.

### 6️⃣ Run the Development Server
```sh
python manage.py runserver
```
The site should now be accessible at http://127.0.0.1:8000/blog/
Access admin with the superuser at http://127.0.0.1:8000/admin/

Visit the [Django Documentation](https://docs.djangoproject.com/en/stable/) for more info.