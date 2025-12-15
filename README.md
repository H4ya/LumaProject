This project is under development by:
Haya Abusaq 
Imtinan Alhajri 
Kholod Al-Attas
Mariam Barakat   
Ruaa Al-Ghamdi
Wesam Kamal 
Zahra Al Thunayan 

---

## How to Run the Project / كيفية تشغيل المشروع

### English Instructions

#### Prerequisites
- Python 3.11 or higher
- Pipenv (install with `pip install pipenv`)
- PostgreSQL database

#### Steps to Run

1. **Navigate to the project directory:**
   ```bash
   cd lumaGenPy
   ```

2. **Install dependencies using Pipenv:**
   ```bash
   pipenv install
   ```

3. **Activate the virtual environment:**
   ```bash
   pipenv shell
   ```

4. **Set up the PostgreSQL database:**
   - Create a database named `lumaDB2`
   - Update the database credentials in `lumaGenPy/settings.py` if needed

5. **Run database migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the application:**
   Open your browser and go to: `http://127.0.0.1:8000/`

---

### التعليمات بالعربي

#### المتطلبات الأساسية
- Python 3.11 أو أحدث
- Pipenv (قم بتثبيته عبر الأمر `pip install pipenv`)
- قاعدة بيانات PostgreSQL

#### خطوات التشغيل

1. **انتقل إلى مجلد المشروع:**
   ```bash
   cd lumaGenPy
   ```

2. **قم بتثبيت المتطلبات باستخدام Pipenv:**
   ```bash
   pipenv install
   ```

3. **قم بتفعيل البيئة الافتراضية:**
   ```bash
   pipenv shell
   ```

4. **قم بإعداد قاعدة البيانات PostgreSQL:**
   - أنشئ قاعدة بيانات باسم `lumaDB2`
   - قم بتحديث بيانات الاتصال في ملف `lumaGenPy/settings.py` إذا لزم الأمر

5. **قم بتطبيق الـ migrations:**
   ```bash
   python manage.py migrate
   ```

6. **قم بتشغيل السيرفر:**
   ```bash
   python manage.py runserver
   ```

7. **افتح التطبيق:**
   افتح المتصفح وانتقل إلى: `http://127.0.0.1:8000/`
