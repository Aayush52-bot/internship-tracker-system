import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
import os
import shutil
from tkinter import filedialog
import webbrowser
from PIL import Image, ImageTk
import datetime # ### NEW ### - Needed for ticket timestamps

# ... (Keep THEME dictionary and get_db function as before) ...
# Color scheme for modern light theme
THEME = {
    "bg": "#FFFFFF",      # White background
    "fg": "#333333",      # Dark grey text
    "highlight": "#007BFF",  # Blue highlight
    "secondary": "#6C757D",  # Medium grey for secondary elements
    "success": "#28A745",    # Green for success
    "error": "#DC3545",      # Red for errors
    "warning": "#FFC107",    # Yellow for warnings
    "button_border": "#E9ECEF" # Light grey for borders
}

# Database connection
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="internship_db"
    )
# ... (Keep show_popup, center_window, add_logo functions as before) ...
# Custom popup for messages
def show_popup(title, message, type="info"):
    popup = tk.Toplevel()
    popup.title(title)
    popup.geometry("350x150")
    popup.configure(bg=THEME["bg"])
    popup.resizable(False, False)
    popup.lift()
    popup.grab_set()

    # Logo
    logo_path = "logo.png"  # Replace with actual logo path
    if os.path.exists(logo_path):
        logo_img = Image.open(logo_path).resize((40, 40), Image.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_img)
        tk.Label(popup, image=logo_photo, bg=THEME["bg"]).pack(pady=5)
        popup.logo = logo_photo  # Keep reference to avoid garbage collection

    # Message
    color = THEME["success"] if type == "success" else THEME["error"] if type == "error" else THEME["highlight"]
    tk.Label(popup, text=message, bg=THEME["bg"], fg=THEME["fg"], wraplength=300, font=("Arial", 11)).pack(pady=10)

    # OK Button
    btn = tk.Button(popup, text="OK", command=popup.destroy, bg=color, fg=THEME["bg"],
                    relief="flat", font=("Arial", 10, "bold"), bd=0, width=10)
    btn.pack(pady=10)
    btn.configure(activebackground=THEME["secondary"], cursor="hand2")
    btn.bind("<Enter>", lambda e: btn.configure(bg=THEME["secondary"]))
    btn.bind("<Leave>", lambda e: btn.configure(bg=color))
    btn.focus_set()  # Ensure button has focus

# Helper function to center a window
def center_window(window, width, height):
    # Get screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate position x and y coordinates
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))

    # Set the geometry
    window.geometry(f'{width}x{height}+{x}+{y}')

# Add logo to window
def add_logo(window):
    logo_path = "logo.png"  # Replace with actual logo path
    if os.path.exists(logo_path):
        logo_img = Image.open(logo_path).resize((40, 40), Image.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_img)
        logo_label = tk.Label(window, image=logo_photo, bg=THEME["bg"])
        logo_label.place(x=10, y=10)
        window.logo = logo_photo  # Keep reference

# UNIVERSAL SCROLLING FUNCTION
def setup_scrolling(canvas):
    """Binds mouse wheel and keyboard arrows for scrolling a canvas."""

    def on_key_press(event):
        if event.keysym == 'Down':
            canvas.yview_scroll(1, "units")
        elif event.keysym == 'Up':
            canvas.yview_scroll(-1, "units")

    def on_mouse_wheel(event):
        # For Windows/macOS
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def on_linux_scroll(event):
        # For Linux
        if event.num == 4:
            canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            canvas.yview_scroll(1, "units")

    # Bind arrow keys
    canvas.bind("<Key-Down>", on_key_press)
    canvas.bind("<Key-Up>", on_key_press)

    # Bind mouse wheel (use bind_all carefully, might need adjustment if causing issues)
    # Using bind on the canvas itself is often safer if focus is managed well.
    canvas.bind("<MouseWheel>", on_mouse_wheel)  # Windows/macOS
    canvas.bind("<Button-4>", on_linux_scroll)   # Linux scroll up
    canvas.bind("<Button-5>", on_linux_scroll)   # Linux scroll down

    # Give focus to the canvas so key bindings work immediately
    # We'll set focus when the specific canvas becomes active (e.g., tab change)
    # canvas.focus_set() # Removed from here, set focus contextually


# ... (Keep open_admin_login, login, open_register functions as before) ...
# ADMIN LOGIN FUNCTION
def open_admin_login():
    admin_win = tk.Toplevel(root)
    admin_win.title("Internship Tracker - Admin Login")
    center_window(admin_win, 400, 350)
    admin_win.configure(bg=THEME["bg"])
    add_logo(admin_win)
    admin_win.lift()
    admin_win.grab_set()

    def on_closing():
        root.deiconify()
        admin_win.destroy()

    admin_win.protocol("WM_DELETE_WINDOW", on_closing)

    frame = tk.Frame(admin_win, bg=THEME["bg"])
    frame.pack(padx=20, pady=20, fill="both")

    tk.Label(frame, text="Admin Login", font=("Arial", 14, "bold"), fg=THEME["fg"], bg=THEME["bg"]).pack(pady=10)

    tk.Label(frame, text="Username", font=("Arial", 10), fg=THEME["fg"], bg=THEME["bg"]).pack(anchor="w", padx=10)
    entry_user = tk.Entry(frame, width=30, font=("Arial", 10), relief="flat", bg="#F8F9FA", fg=THEME["fg"],
                          highlightthickness=1, highlightbackground=THEME["button_border"])
    entry_user.pack(pady=5, padx=10, fill="x")

    tk.Label(frame, text="Password", font=("Arial", 10), fg=THEME["fg"], bg=THEME["bg"]).pack(anchor="w", padx=10)
    entry_pass = tk.Entry(frame, width=30, show="*", font=("Arial", 10), relief="flat", bg="#F8F9FA", fg=THEME["fg"],
                          highlightthickness=1, highlightbackground=THEME["button_border"])
    entry_pass.pack(pady=5, padx=10, fill="x")
    entry_pass.bind("<Return>", lambda event: admin_login())

    def admin_login():
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM admin WHERE username=%s AND password=%s",
                         (entry_user.get(), entry_pass.get()))
        admin = cursor.fetchone()
        cursor.close()
        db.close()
        if admin:
            show_popup("Success", "Admin Login Successful!", "success")
            admin_win.destroy()
            root.withdraw()
            open_admin_panel()
        else:
            show_popup("Error", "Invalid Admin Login!", "error")

    btn = tk.Button(frame, text="Login", command=admin_login, bg=THEME["highlight"], fg=THEME["bg"],
                    font=("Arial", 10, "bold"), relief="flat", bd=0, width=15)
    btn.pack(pady=20)
    btn.bind("<Enter>", lambda e: btn.configure(bg=THEME["secondary"]))
    btn.bind("<Leave>", lambda e: btn.configure(bg=THEME["highlight"]))

# LOGIN FUNCTION
def login():
    email = entry_email.get()
    password = entry_password.get()

    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students WHERE email=%s AND password=%s", (email, password))
    user = cursor.fetchone()
    cursor.close()
    db.close()


    if user:
        root.withdraw()
        open_student_dashboard(user['id'], user['name'])
    else:
        show_popup("Error", "Invalid email or password!", "error")

# REGISTER FUNCTION
def open_register():
    reg_win = tk.Toplevel(root)
    reg_win.title("Internship Tracker - Register Student")
    reg_win.state('zoomed')
    reg_win.configure(bg=THEME["bg"])
    add_logo(reg_win)
    reg_win.lift()
    reg_win.grab_set()

    def on_closing():
        root.deiconify()
        reg_win.destroy()

    reg_win.protocol("WM_DELETE_WINDOW", on_closing)

    canvas = tk.Canvas(reg_win, bg=THEME["bg"], highlightthickness=0)
    scrollbar = tk.Scrollbar(reg_win, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg=THEME["bg"])

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    setup_scrolling(canvas)

    # Frame to center the content
    frame = tk.Frame(scroll_frame, bg=THEME["bg"])
    frame.pack(pady=20, padx=50)

    tk.Label(frame, text="Register New Student", font=("Arial", 16, "bold"), fg=THEME["fg"], bg=THEME["bg"]).pack(pady=20)

    fields = ["Name", "Email", "Password", "Confirm Password", "Roll No", "Course"]
    entries = {}
    for field in fields:
        tk.Label(frame, text=field, font=("Arial", 11), fg=THEME["fg"], bg=THEME["bg"]).pack(anchor="w", padx=10)
        entry = tk.Entry(frame, width=50, font=("Arial", 11), relief="flat", bg="#F8F9FA", fg=THEME["fg"],
                         highlightthickness=1, highlightbackground=THEME["button_border"],
                         show="*" if "Password" in field else None)
        entry.pack(pady=5, padx=10, fill="x", ipady=4)
        entries[field.lower().replace(" ", "_")] = entry

    def register():
        if entries["password"].get() != entries["confirm_password"].get():
            show_popup("Error", "Passwords do not match!", "error")
            return

        for field in fields:
            if not entries[field.lower().replace(" ", "_")].get():
                show_popup("Error", f"{field} is required.", "error")
                return

        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("INSERT INTO students (name, email, password, roll_no, course) VALUES (%s, %s, %s, %s, %s)",
                           (entries["name"].get(), entries["email"].get(), entries["password"].get(),
                            entries["roll_no"].get(), entries["course"].get()))
            db.commit()
            show_popup("Success", "Student Registered Successfully!", "success")
            reg_win.destroy()
        except Exception as e:
            show_popup("Error", f"Registration failed: {e}", "error")
        finally:
            cursor.close()
            db.close()

    btn = tk.Button(frame, text="Register", command=register, bg=THEME["highlight"], fg=THEME["bg"],
                    font=("Arial", 11, "bold"), relief="flat", bd=0, width=15, pady=5)
    btn.pack(pady=20)
    entries["course"].bind("<Return>", lambda event: register())
    btn.configure(activebackground=THEME["secondary"], cursor="hand2")
    btn.bind("<Enter>", lambda e: btn.configure(bg=THEME["secondary"]))
    btn.bind("<Leave>", lambda e: btn.configure(bg=THEME["highlight"]))

# ... (Keep MAIN LOGIN WINDOW code as before) ...
# MAIN LOGIN WINDOW
root = tk.Tk()
root.title("Internship Tracker - Login")
center_window(root, 400, 350)
root.configure(bg=THEME["bg"])
add_logo(root)

frame = tk.Frame(root, bg=THEME["bg"])
frame.pack(padx=20, pady=20, fill="both")

tk.Label(frame, text="Student Login", font=("Arial", 14, "bold"), fg=THEME["fg"], bg=THEME["bg"]).pack(pady=10)

tk.Label(frame, text="Email", font=("Arial", 10), fg=THEME["fg"], bg=THEME["bg"]).pack(anchor="w", padx=10)
entry_email = tk.Entry(frame, width=30, font=("Arial", 10), relief="flat", bg="#F8F9FA", fg=THEME["fg"],
                       highlightthickness=1, highlightbackground=THEME["button_border"])
entry_email.pack(pady=5, padx=10, fill="x")

tk.Label(frame, text="Password", font=("Arial", 10), fg=THEME["fg"], bg=THEME["bg"]).pack(anchor="w", padx=10)
entry_password = tk.Entry(frame, width=30, show="*", font=("Arial", 10), relief="flat", bg="#F8F9FA", fg=THEME["fg"],
                          highlightthickness=1, highlightbackground=THEME["button_border"])
entry_password.pack(pady=5, padx=10, fill="x")
entry_password.bind("<Return>", lambda event: login())

btn_login = tk.Button(frame, text="Login", command=login, bg=THEME["highlight"], fg=THEME["bg"],
                       font=("Arial", 10, "bold"), relief="flat", bd=0, width=15)
btn_login.pack(pady=10)
btn_login.configure(activebackground=THEME["secondary"], cursor="hand2")
btn_login.bind("<Enter>", lambda e: btn_login.configure(bg=THEME["secondary"]))
btn_login.bind("<Leave>", lambda e: btn_login.configure(bg=THEME["highlight"]))

btn_register = tk.Button(frame, text="Register", command=open_register, bg=THEME["highlight"], fg=THEME["bg"],
                         font=("Arial", 10, "bold"), relief="flat", bd=0, width=15)
btn_register.pack(pady=10)
btn_register.configure(activebackground=THEME["secondary"], cursor="hand2")
btn_register.bind("<Enter>", lambda e: btn_register.configure(bg=THEME["secondary"]))
btn_register.bind("<Leave>", lambda e: btn_register.configure(bg=THEME["highlight"]))

btn_admin = tk.Button(frame, text="Admin Login", command=open_admin_login, bg=THEME["highlight"], fg=THEME["bg"],
                      font=("Arial", 10, "bold"), relief="flat", bd=0, width=15)
btn_admin.pack(pady=10)
btn_admin.configure(activebackground=THEME["secondary"], cursor="hand2")
btn_admin.bind("<Enter>", lambda e: btn_admin.configure(bg=THEME["secondary"]))
btn_admin.bind("<Leave>", lambda e: btn_admin.configure(bg=THEME["highlight"]))

# ... (Keep UPLOAD_DIR setup) ...
# Make sure uploads folder exists
UPLOAD_DIR = os.path.join(os.getcwd(), "uploads")
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# ... (Keep ENHANCED open_student_profile function) ...
def open_student_profile(student_id):
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM students WHERE id=%s", (student_id,))
    student = cur.fetchone()
    cur.close()
    db.close()

    prof = tk.Toplevel(root)
    prof.title("Internship Tracker - My Profile")
    prof.state('zoomed')
    prof.configure(bg=THEME["bg"])
    add_logo(prof)
    prof.lift()
    prof.grab_set()

    def on_closing():
        root.deiconify()
        prof.destroy()

    prof.protocol("WM_DELETE_WINDOW", on_closing)

    canvas = tk.Canvas(prof, bg=THEME["bg"], highlightthickness=0)
    scrollbar = tk.Scrollbar(prof, orient="vertical", command=canvas.yview)

    wrapper_frame = tk.Frame(canvas, bg=THEME["bg"])
    wrapper_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    frame = tk.Frame(wrapper_frame, bg=THEME["bg"])
    frame.pack(padx=20, pady=20)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    scrollbar.pack(side="right", fill="y")

    # Function to re-center the frame on resize
    def center_frame(event):
        canvas_width = event.width
        # Place frame in the center horizontally
        canvas.create_window((canvas_width/2, 0), window=wrapper_frame, anchor='n')

    canvas.bind('<Configure>', center_frame)
    setup_scrolling(canvas)

    tk.Label(frame, text="My Profile", font=("Arial", 16, "bold"), fg=THEME["fg"], bg=THEME["bg"]).pack(pady=20)

    def save_file(field_name, filetypes):
        prof.grab_release()
        path = filedialog.askopenfilename(parent=prof, filetypes=filetypes)
        prof.grab_set()
        if not path:
            return None
        ext = os.path.splitext(path)[1].lower()
        allowed = ['.pdf', '.docx', '.jpg', '.jpeg', '.png']
        if ext not in allowed:
            show_popup("Error", "Only PDF, DOCX, JPG, PNG allowed.", "error")
            return None
        student_folder = os.path.join(UPLOAD_DIR, str(student_id))
        os.makedirs(student_folder, exist_ok=True)
        dest = os.path.join(student_folder, os.path.basename(path))
        try:
            shutil.copy(path, dest)
        except Exception as e:
            show_popup("Error", f"File copy failed: {e}", "error")
            return None
        return dest.replace("\\", "/")

    # --- Helper for creating form rows ---
    def create_form_row(parent, label_text):
        row_frame = tk.Frame(parent, bg=THEME["bg"])
        row_frame.pack(fill="x", pady=2)
        tk.Label(row_frame, text=label_text, font=("Arial", 11), fg=THEME["fg"], bg=THEME["bg"], width=25, anchor="e").pack(side="left", padx=5)
        return row_frame

    # --- Personal Info ---
    lf_personal = ttk.LabelFrame(frame, text="  Personal Information  ", style="TLabelframe")
    lf_personal.pack(fill="x", expand=True, pady=10, padx=10)

    row = create_form_row(lf_personal, "Full Name:")
    entry_fullname = tk.Entry(row, width=50, font=("Arial", 11), relief="flat", bg="#F8F9FA", fg=THEME["fg"], highlightthickness=1, highlightbackground=THEME["button_border"])
    entry_fullname.pack(side="left", fill="x", expand=True, padx=5, ipady=4)
    entry_fullname.insert(0, student.get("name","") if student else "")

    row = create_form_row(lf_personal, "Date of Birth (YYYY-MM-DD):")
    dob_val = student.get("dob").strftime("%Y-%m-%d") if student and student.get("dob") else ""
    entry_dob = tk.Entry(row, width=50, font=("Arial", 11), relief="flat", bg="#F8F9FA", fg=THEME["fg"], highlightthickness=1, highlightbackground=THEME["button_border"])
    entry_dob.pack(side="left", fill="x", expand=True, padx=5, ipady=4)
    entry_dob.insert(0, dob_val)

    row = create_form_row(lf_personal, "Gender:")
    gender_var = tk.StringVar(value=student.get("gender","") if student else "")
    gender_menu = ttk.OptionMenu(row, gender_var, student.get("gender","") or "Select", "Male", "Female", "Other")
    gender_menu.pack(side="left", padx=5, pady=3)

    row = create_form_row(lf_personal, "Contact Number:")
    entry_contact = tk.Entry(row, width=50, font=("Arial", 11), relief="flat", bg="#F8F9FA", fg=THEME["fg"], highlightthickness=1, highlightbackground=THEME["button_border"])
    entry_contact.pack(side="left", fill="x", expand=True, padx=5, ipady=4)
    entry_contact.insert(0, student.get("contact","") if student else "")

    row = create_form_row(lf_personal, "Email ID:")
    entry_email = tk.Entry(row, width=50, font=("Arial", 11), relief="flat", bg="#F8F9FA", fg=THEME["fg"], highlightthickness=1, highlightbackground=THEME["button_border"])
    entry_email.pack(side="left", fill="x", expand=True, padx=5, ipady=4)
    entry_email.insert(0, student.get("email","") if student else "")

    row = create_form_row(lf_personal, "Address:")
    entry_address = tk.Text(row, width=38, height=3, font=("Arial", 11), relief="flat", bg="#F8F9FA", fg=THEME["fg"], highlightthickness=1, highlightbackground=THEME["button_border"])
    entry_address.pack(side="left", fill="x", expand=True, padx=5, ipady=4)
    if student and student.get("address"):
        entry_address.insert("1.0", student.get("address"))

    # --- Academic Info ---
    lf_academic = ttk.LabelFrame(frame, text="  Academic Information  ", style="TLabelframe")
    lf_academic.pack(fill="x", expand=True, pady=10, padx=10)

    row = create_form_row(lf_academic, "College Name:")
    entry_college = tk.Entry(row, width=50, font=("Arial", 11), relief="flat", bg="#F8F9FA", fg=THEME["fg"], highlightthickness=1, highlightbackground=THEME["button_border"])
    entry_college.pack(side="left", fill="x", expand=True, padx=5, ipady=4)
    entry_college.insert(0, student.get("college_name","") if student else "")

    row = create_form_row(lf_academic, "Enrollment / Roll No:")
    entry_enroll = tk.Entry(row, width=50, font=("Arial", 11), relief="flat", bg="#F8F9FA", fg=THEME["fg"], highlightthickness=1, highlightbackground=THEME["button_border"])
    entry_enroll.pack(side="left", fill="x", expand=True, padx=5, ipady=4)
    entry_enroll.insert(0, student.get("enrollment_no","") if student else "")

    row = create_form_row(lf_academic, "Course & Specialization:")
    entry_course = tk.Entry(row, width=50, font=("Arial", 11), relief="flat", bg="#F8F9FA", fg=THEME["fg"], highlightthickness=1, highlightbackground=THEME["button_border"])
    entry_course.pack(side="left", fill="x", expand=True, padx=5, ipady=4)
    entry_course.insert(0, student.get("course","") if student else "")

    row = create_form_row(lf_academic, "Year of Study / Passing Year:")
    entry_year = tk.Entry(row, width=50, font=("Arial", 11), relief="flat", bg="#F8F9FA", fg=THEME["fg"], highlightthickness=1, highlightbackground=THEME["button_border"])
    entry_year.pack(side="left", fill="x", expand=True, padx=5, ipady=4)
    entry_year.insert(0, student.get("year_of_study","") if student else "")

    row = create_form_row(lf_academic, "Aggregate % / CGPA:")
    entry_aggregate = tk.Entry(row, width=50, font=("Arial", 11), relief="flat", bg="#F8F9FA", fg=THEME["fg"], highlightthickness=1, highlightbackground=THEME["button_border"])
    entry_aggregate.pack(side="left", fill="x", expand=True, padx=5, ipady=4)
    entry_aggregate.insert(0, student.get("aggregate","") if student else "")

    row = create_form_row(lf_academic, "10th Marks (%):")
    entry_10th = tk.Entry(row, width=50, font=("Arial", 11), relief="flat", bg="#F8F9FA", fg=THEME["fg"], highlightthickness=1, highlightbackground=THEME["button_border"])
    entry_10th.pack(side="left", fill="x", expand=True, padx=5, ipady=4)
    entry_10th.insert(0, student.get("marks_10th","") if student else "")

    row = create_form_row(lf_academic, "12th / Diploma Marks (%):")
    entry_12th = tk.Entry(row, width=50, font=("Arial", 11), relief="flat", bg="#F8F9FA", fg=THEME["fg"], highlightthickness=1, highlightbackground=THEME["button_border"])
    entry_12th.pack(side="left", fill="x", expand=True, padx=5, ipady=4)
    entry_12th.insert(0, student.get("marks_12th","") if student else "")

    # --- Professional Info ---
    lf_prof = ttk.LabelFrame(frame, text="  Professional Information  ", style="TLabelframe")
    lf_prof.pack(fill="x", expand=True, pady=10, padx=10)

    row = create_form_row(lf_prof, "Technical Skills (comma separated):")
    tech_txt = tk.Text(row, width=38, height=3, font=("Arial", 11), relief="flat", bg="#F8F9FA", fg=THEME["fg"], highlightthickness=1, highlightbackground=THEME["button_border"])
    tech_txt.pack(side="left", fill="x", expand=True, padx=5, ipady=4)
    if student and student.get("technical_skills"):
        tech_txt.insert("1.0", student.get("technical_skills"))

    row = create_form_row(lf_prof, "Soft Skills:")
    soft_txt = tk.Text(row, width=38, height=2, font=("Arial", 11), relief="flat", bg="#F8F9FA", fg=THEME["fg"], highlightthickness=1, highlightbackground=THEME["button_border"])
    soft_txt.pack(side="left", fill="x", expand=True, padx=5, ipady=4)
    if student and student.get("soft_skills"):
        soft_txt.insert("1.0", student.get("soft_skills"))

    row = create_form_row(lf_prof, "Certifications (comma separated):")
    cert_txt = tk.Text(row, width=38, height=2, font=("Arial", 11), relief="flat", bg="#F8F9FA", fg=THEME["fg"], highlightthickness=1, highlightbackground=THEME["button_border"])
    cert_txt.pack(side="left", fill="x", expand=True, padx=5, ipady=4)
    if student and student.get("certifications"):
        cert_txt.insert("1.0", student.get("certifications"))

    row = create_form_row(lf_prof, "Experience (company, role, duration):")
    exp_txt = tk.Text(row, width=38, height=3, font=("Arial", 11), relief="flat", bg="#F8F9FA", fg=THEME["fg"], highlightthickness=1, highlightbackground=THEME["button_border"])
    exp_txt.pack(side="left", fill="x", expand=True, padx=5, ipady=4)
    if student and student.get("experience"):
        exp_txt.insert("1.0", student.get("experience"))

    # --- Job Preferences ---
    lf_prefs = ttk.LabelFrame(frame, text="  Job Preferences  ", style="TLabelframe")
    lf_prefs.pack(fill="x", expand=True, pady=10, padx=10)

    row = create_form_row(lf_prefs, "Desired Job Role:")
    entry_role = tk.Entry(row, width=50, font=("Arial", 11), relief="flat", bg="#F8F9FA", fg=THEME["fg"], highlightthickness=1, highlightbackground=THEME["button_border"])
    entry_role.pack(side="left", fill="x", expand=True, padx=5, ipady=4)
    entry_role.insert(0, student.get("desired_role","") if student else "")

    row = create_form_row(lf_prefs, "Preferred Location(s):")
    entry_location = tk.Entry(row, width=50, font=("Arial", 11), relief="flat", bg="#F8F9FA", fg=THEME["fg"], highlightthickness=1, highlightbackground=THEME["button_border"])
    entry_location.pack(side="left", fill="x", expand=True, padx=5, ipady=4)
    entry_location.insert(0, student.get("preferred_location","") if student else "")

    row = create_form_row(lf_prefs, "Willing to Relocate:")
    relocate_var = tk.StringVar(value=student.get("willing_to_relocate","No") if student else "No")
    ttk.OptionMenu(row, relocate_var, student.get("willing_to_relocate","No") or "No", "Yes", "No").pack(side="left", padx=5, pady=3)

    # --- Document Uploads ---
    lf_docs = ttk.LabelFrame(frame, text="  Document Uploads  ", style="TLabelframe")
    lf_docs.pack(fill="x", expand=True, pady=10, padx=10)

    def create_upload_row(parent, label_text, var, command):
        row_frame = tk.Frame(parent, bg=THEME["bg"])
        row_frame.pack(fill="x", pady=5)
        tk.Label(row_frame, text=label_text, font=("Arial", 11), fg=THEME["fg"], bg=THEME["bg"], width=25, anchor="e").pack(side="left", padx=5)
        tk.Entry(row_frame, textvariable=var, width=40, font=("Arial", 11), relief="flat", bg="#F8F9FA", fg=THEME["fg"], highlightthickness=1, highlightbackground=THEME["button_border"]).pack(side="left", fill="x", expand=True, padx=5, ipady=4)
        btn = tk.Button(row_frame, text="Upload", command=command, bg=THEME["highlight"], fg=THEME["bg"], font=("Arial", 10, "bold"), relief="flat", bd=0, pady=3)
        btn.pack(side="left", padx=5)
        btn.bind("<Enter>", lambda e: btn.configure(bg=THEME["secondary"]))
        btn.bind("<Leave>", lambda e: btn.configure(bg=THEME["highlight"]))

    photo_path_var = tk.StringVar(value=student.get("photo_path","") if student else "")
    create_upload_row(lf_docs, "Passport Photo:", photo_path_var, lambda: photo_path_var.set(save_file("photo", [("Images","*.jpg *.jpeg *.png")])))

    resume_var = tk.StringVar(value=student.get("resume_path","") if student else "")
    create_upload_row(lf_docs, "Resume (PDF/DOCX):", resume_var, lambda: resume_var.set(save_file("resume", [("Docs","*.pdf *.docx")])))

    certs_path_var = tk.StringVar(value=student.get("certificates_path","") if student else "")
    create_upload_row(lf_docs, "Certificates:", certs_path_var, lambda: certs_path_var.set(save_file("certs", [("Docs","*.pdf *.docx *.jpg *.png")])))

    id_path_var = tk.StringVar(value=student.get("idproof_path","") if student else "")
    create_upload_row(lf_docs, "ID Proof:", id_path_var, lambda: id_path_var.set(save_file("idproof", [("Docs","*.pdf *.jpg *.png")])))

    # --- Save Button ---
    def save_profile():
        dbs = get_db()
        cur = dbs.cursor()
        try:
            cur.execute("""
                UPDATE students SET
                    name=%s, dob=%s, gender=%s, contact=%s, address=%s, photo_path=%s,
                    college_name=%s, enrollment_no=%s, course=%s, year_of_study=%s,
                    aggregate=%s, marks_10th=%s, marks_12th=%s, technical_skills=%s,
                    soft_skills=%s, certifications=%s, experience=%s, desired_role=%s,
                    preferred_location=%s, willing_to_relocate=%s, resume_path=%s,
                    certificates_path=%s, idproof_path=%s
                WHERE id=%s
            """, (
                entry_fullname.get(), entry_dob.get(), gender_var.get(), entry_contact.get(),
                entry_address.get("1.0", "end").strip(), photo_path_var.get(),
                entry_college.get(), entry_enroll.get(), entry_course.get(), entry_year.get(),
                entry_aggregate.get(), entry_10th.get(), entry_12th.get(), tech_txt.get("1.0","end").strip(),
                soft_txt.get("1.0","end").strip(), cert_txt.get("1.0","end").strip(), exp_txt.get("1.0","end").strip(),
                entry_role.get(), entry_location.get(), relocate_var.get(), resume_var.get(),
                certs_path_var.get(), id_path_var.get(), student_id
            ))
            dbs.commit()
            show_popup("Success", "Profile updated successfully.", "success")
            prof.destroy()
        except Exception as e:
            show_popup("Error", f"Failed to save profile: {e}", "error")
        finally:
            cur.close()
            dbs.close()

    btn_save = tk.Button(frame, text="Save Profile", command=save_profile, bg=THEME["success"], fg=THEME["bg"],
                         font=("Arial", 11, "bold"), relief="flat", bd=0, width=20, pady=5)
    btn_save.pack(pady=20)
    btn_save.bind("<Enter>", lambda e: btn_save.configure(bg=THEME["secondary"]))
    btn_save.bind("<Leave>", lambda e: btn_save.configure(bg=THEME["success"]))
# ... (Keep ENHANCED open_admin_view_profile function) ...
def open_admin_view_profile(student_id):
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM students WHERE id=%s", (student_id,))
    s = cur.fetchone()
    cur.close()
    db.close()
    if not s:
        show_popup("Error", "Student not found.", "error")
        return

    prof = tk.Toplevel(root)
    prof.title(f"Internship Tracker - Profile - {s.get('name','')}")
    prof.state('zoomed')
    prof.configure(bg=THEME["bg"])
    add_logo(prof)
    prof.lift()
    prof.grab_set()

    canvas = tk.Canvas(prof, bg=THEME["bg"], highlightthickness=0)
    scrollbar = tk.Scrollbar(prof, orient="vertical", command=canvas.yview)

    wrapper_frame = tk.Frame(canvas, bg=THEME["bg"])
    wrapper_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    frame = tk.Frame(wrapper_frame, bg=THEME["bg"])
    frame.pack(padx=20, pady=20)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    scrollbar.pack(side="right", fill="y")

    def center_frame(event):
        canvas_width = event.width
        canvas.create_window((canvas_width/2, 0), window=wrapper_frame, anchor='n')

    canvas.bind('<Configure>', center_frame)
    setup_scrolling(canvas)

    tk.Label(frame, text=f"Profile - {s.get('name','')}", font=("Arial", 16, "bold"), fg=THEME["fg"], bg=THEME["bg"]).pack(pady=20)

    # --- Helper for creating display rows ---
    def create_display_row(parent, label_text, value_text):
        row_frame = tk.Frame(parent, bg=THEME["bg"])
        row_frame.pack(fill="x", pady=3)
        tk.Label(row_frame, text=f"{label_text}:", font=("Arial", 11, "bold"), fg=THEME["fg"], bg=THEME["bg"], width=25, anchor="e").pack(side="left", padx=5)
        tk.Label(row_frame, text=value_text if value_text else "-", wraplength=500, justify="left", font=("Arial", 11), fg=THEME["fg"], bg=THEME["bg"], anchor="w").pack(side="left", fill="x", expand=True, padx=5)

    # --- Personal Info ---
    lf_personal = ttk.LabelFrame(frame, text="  Personal Information  ", style="TLabelframe")
    lf_personal.pack(fill="x", expand=True, pady=10, padx=10)
    create_display_row(lf_personal, "Full Name", s.get("name",""))
    create_display_row(lf_personal, "Date of Birth", str(s.get("dob","")))
    create_display_row(lf_personal, "Gender", s.get("gender",""))
    create_display_row(lf_personal, "Contact", s.get("contact",""))
    create_display_row(lf_personal, "Email", s.get("email",""))
    create_display_row(lf_personal, "Address", s.get("address",""))

    # --- Academic Info ---
    lf_academic = ttk.LabelFrame(frame, text="  Academic Information  ", style="TLabelframe")
    lf_academic.pack(fill="x", expand=True, pady=10, padx=10)
    create_display_row(lf_academic, "College", s.get("college_name",""))
    create_display_row(lf_academic, "Enrollment / Roll No", s.get("enrollment_no",""))
    create_display_row(lf_academic, "Course", s.get("course",""))
    create_display_row(lf_academic, "Year / Passing", s.get("year_of_study",""))
    create_display_row(lf_academic, "Aggregate (CGPA)", s.get("aggregate",""))
    create_display_row(lf_academic, "10th Marks (%)", s.get("marks_10th",""))
    create_display_row(lf_academic, "12th / Diploma Marks (%)", s.get("marks_12th",""))

    # --- Professional Info ---
    lf_prof = ttk.LabelFrame(frame, text="  Professional Information  ", style="TLabelframe")
    lf_prof.pack(fill="x", expand=True, pady=10, padx=10)
    create_display_row(lf_prof, "Technical Skills", s.get("technical_skills",""))
    create_display_row(lf_prof, "Soft Skills", s.get("soft_skills",""))
    create_display_row(lf_prof, "Certifications", s.get("certifications",""))
    create_display_row(lf_prof, "Experience", s.get("experience",""))

    # --- Job Preferences ---
    lf_prefs = ttk.LabelFrame(frame, text="  Job Preferences  ", style="TLabelframe")
    lf_prefs.pack(fill="x", expand=True, pady=10, padx=10)
    create_display_row(lf_prefs, "Desired Role", s.get("desired_role",""))
    create_display_row(lf_prefs, "Preferred Location(s)", s.get("preferred_location",""))
    create_display_row(lf_prefs, "Willing to Relocate", s.get("willing_to_relocate",""))

    # --- Document Uploads ---
    lf_docs = ttk.LabelFrame(frame, text="  Uploaded Documents  ", style="TLabelframe")
    lf_docs.pack(fill="x", expand=True, pady=10, padx=10)

    def create_file_row(parent, label_text, path):
        row_frame = tk.Frame(parent, bg=THEME["bg"])
        row_frame.pack(fill="x", pady=3)
        tk.Label(row_frame, text=f"{label_text}:", font=("Arial", 11, "bold"), fg=THEME["fg"], bg=THEME["bg"], width=25, anchor="e").pack(side="left", padx=5)

        if path:
            display = tk.Label(row_frame, text=os.path.basename(path), fg=THEME["highlight"], cursor="hand2", font=("Arial", 11, "underline"), bg=THEME["bg"], anchor="w")
            display.pack(side="left", fill="x", expand=True, padx=5)
            def open_file(p=path):
                try:
                    full_path = os.path.join(os.getcwd(), p) # Ensure path is absolute
                    if not os.path.exists(full_path):
                         show_popup("Error", f"File not found: {os.path.basename(p)}", "error")
                         return
                    if os.name == 'nt':
                        os.startfile(full_path)
                    else:
                        # For macOS/Linux, try webbrowser first, then specific commands if needed
                        try:
                            webbrowser.open(f"file://{full_path}")
                        except Exception:
                             # Fallback for Linux if webbrowser fails
                             if sys.platform == "linux" or sys.platform == "linux2":
                                 os.system(f"xdg-open '{full_path}'")
                             # Fallback for macOS
                             elif sys.platform == "darwin":
                                 os.system(f"open '{full_path}'")
                             else:
                                 raise # Re-raise error if platform unknown
                except Exception as e:
                    show_popup("Error", f"Cannot open file: {e}", "error")
            display.bind("<Button-1>", lambda e, p=path: open_file(p))
        else:
            tk.Label(row_frame, text="-", font=("Arial", 11), fg=THEME["fg"], bg=THEME["bg"], anchor="w").pack(side="left", fill="x", expand=True, padx=5)

    create_file_row(lf_docs, "Passport Photo", s.get("photo_path"))
    create_file_row(lf_docs, "Resume", s.get("resume_path"))
    create_file_row(lf_docs, "Certificates", s.get("certificates_path"))
    create_file_row(lf_docs, "ID Proof", s.get("idproof_path"))

    btn_close = tk.Button(frame, text="Close", command=prof.destroy, bg=THEME["secondary"], fg=THEME["bg"],
                          font=("Arial", 11, "bold"), relief="flat", bd=0, width=15, pady=5)
    btn_close.pack(pady=20)
    btn_close.bind("<Enter>", lambda e: btn_close.configure(bg=THEME["highlight"]))
    btn_close.bind("<Leave>", lambda e: btn_close.configure(bg=THEME["secondary"]))
# HELP & SUPPORT FUNCTIONS (Student)
def open_support_window(student_id):
    support_win = tk.Toplevel(root)
    support_win.title("Help & Support")
    center_window(support_win, 450, 400)
    support_win.configure(bg=THEME["bg"])
    support_win.lift()
    support_win.grab_set()

    frame = tk.Frame(support_win, bg=THEME["bg"])
    frame.pack(padx=20, pady=20, fill="both", expand=True)

    tk.Label(frame, text="Contact Support", font=("Arial", 14, "bold"), fg=THEME["fg"], bg=THEME["bg"]).pack(pady=10)

    tk.Label(frame, text="Subject", font=("Arial", 10), fg=THEME["fg"], bg=THEME["bg"]).pack(anchor="w", padx=10)
    entry_subject = tk.Entry(frame, width=50, font=("Arial", 10), relief="flat", bg="#F8F9FA", fg=THEME["fg"],
                             highlightthickness=1, highlightbackground=THEME["button_border"])
    entry_subject.pack(pady=5, padx=10, fill="x")

    tk.Label(frame, text="Message", font=("Arial", 10), fg=THEME["fg"], bg=THEME["bg"]).pack(anchor="w", padx=10)
    text_message = tk.Text(frame, width=50, height=10, font=("Arial", 10), relief="flat", bg="#F8F9FA", fg=THEME["fg"],
                           highlightthickness=1, highlightbackground=THEME["button_border"])
    text_message.pack(pady=5, padx=10, fill="both", expand=True)

    def submit_ticket():
        subject = entry_subject.get()
        message = text_message.get("1.0", "end").strip()

        if not subject or not message:
            show_popup("Error", "Subject and Message are required.", "error")
            return

        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute("INSERT INTO support_tickets (student_id, subject, message, status) VALUES (%s, %s, %s, 'Open')",
                           (student_id, subject, message))
            db.commit()
            cursor.close()
            db.close()
            show_popup("Success", "Support ticket submitted successfully!", "success")
            support_win.destroy()
        except Exception as e:
            show_popup("Error", f"Failed to submit ticket: {e}", "error")

    btn = tk.Button(frame, text="Submit Ticket", command=submit_ticket, bg=THEME["success"], fg=THEME["bg"],
                    font=("Arial", 10, "bold"), relief="flat", bd=0, width=15)
    btn.pack(pady=20)
    btn.bind("<Enter>", lambda e: btn.configure(bg=THEME["secondary"]))
    btn.bind("<Leave>", lambda e: btn.configure(bg=THEME["success"]))

# ===================================================================
# ### NEW ### - STUDENT VIEW FOR THEIR TICKETS
# ===================================================================
def open_my_tickets(student_id):
    my_tickets_win = tk.Toplevel(root)
    my_tickets_win.title("My Support Tickets")
    my_tickets_win.geometry("800x600") # Larger window
    my_tickets_win.configure(bg=THEME["bg"])
    my_tickets_win.lift()
    my_tickets_win.grab_set()

    tk.Label(my_tickets_win, text="My Support Tickets", font=("Arial", 16, "bold"), fg=THEME["fg"], bg=THEME["bg"]).pack(pady=15)

    toolbar = tk.Frame(my_tickets_win, bg=THEME["bg"])
    toolbar.pack(fill="x", padx=10, pady=5)
    btn_refresh = tk.Button(toolbar, text="Refresh",
                             bg=THEME["highlight"], fg=THEME["bg"], font=("Arial", 10, "bold"), relief="flat", bd=0)
    btn_refresh.pack(side="left")
    btn_refresh.bind("<Enter>", lambda e: btn_refresh.configure(bg=THEME["secondary"]))
    btn_refresh.bind("<Leave>", lambda e: btn_refresh.configure(bg=THEME["highlight"]))

    tickets_container = tk.Frame(my_tickets_win, bg=THEME["bg"])
    tickets_container.pack(fill="both", expand=True, padx=10, pady=10)
    canvas_tickets = tk.Canvas(tickets_container, bg=THEME["bg"], highlightthickness=0)
    scrollbar_tickets = tk.Scrollbar(tickets_container, orient="vertical", command=canvas_tickets.yview)
    scroll_frame_tickets = tk.Frame(canvas_tickets, bg=THEME["bg"])
    scroll_frame_tickets.bind("<Configure>", lambda e: canvas_tickets.configure(scrollregion=canvas_tickets.bbox("all")))
    canvas_tickets.create_window((0, 0), window=scroll_frame_tickets, anchor="nw")
    canvas_tickets.configure(yscrollcommand=scrollbar_tickets.set)
    canvas_tickets.pack(side="left", fill="both", expand=True)
    scrollbar_tickets.pack(side="right", fill="y")
    setup_scrolling(canvas_tickets)

    def load_tickets():
        for widget in scroll_frame_tickets.winfo_children():
            widget.destroy()

        try:
            db = get_db()
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM support_tickets WHERE student_id = %s ORDER BY created_at DESC", (student_id,))
            tickets = cursor.fetchall()
            cursor.close()
            db.close()

            if not tickets:
                tk.Label(scroll_frame_tickets, text="You have not submitted any support tickets.", font=("Arial", 11), fg=THEME["fg"], bg=THEME["bg"]).pack(pady=10)
                return

            for ticket in tickets:
                frame = tk.Frame(scroll_frame_tickets, bg="#F0F0F0", bd=1, relief="solid") # Slightly different background
                frame.pack(fill="x", pady=5, padx=5)

                tk.Label(frame, text=f"Subject: {ticket['subject']}", font=("Arial", 11, "bold"), fg=THEME["fg"], bg="#F0F0F0").pack(anchor="w", padx=10, pady=(5,0))
                tk.Label(frame, text=f"Submitted: {ticket['created_at'].strftime('%Y-%m-%d %H:%M')}", font=("Arial", 9, "italic"), fg=THEME["secondary"], bg="#F0F0F0").pack(anchor="w", padx=10)

                tk.Label(frame, text="Your Message:", font=("Arial", 10, "bold"), fg=THEME["fg"], bg="#F0F0F0").pack(anchor="w", padx=10, pady=(5,0))
                tk.Label(frame, text=ticket['message'], wraplength=700, justify="left", font=("Arial", 10), fg=THEME["fg"], bg="#F0F0F0").pack(anchor="w", padx=10, pady=(0,5))

                status_color = THEME["success"] if ticket['status'] == 'Closed' else THEME["error"]
                tk.Label(frame, text=f"Status: {ticket['status']}", font=("Arial", 10, "bold"), fg=status_color, bg="#F0F0F0").pack(anchor="w", padx=10, pady=(0,5))

                if ticket['admin_reply']:
                    tk.Label(frame, text="Admin Reply:", font=("Arial", 10, "bold"), fg=THEME["fg"], bg="#F0F0F0").pack(anchor="w", padx=10, pady=(5,0))
                    reply_bg = "#E0FFE0" # Light green for reply
                    tk.Label(frame, text=ticket['admin_reply'], wraplength=700, justify="left", font=("Arial", 10), fg=THEME["fg"], bg=reply_bg, relief="groove", borderwidth=1).pack(anchor="w", padx=10, pady=(0,10), fill="x")

        except Exception as e:
            tk.Label(scroll_frame_tickets, text=f"Error loading your tickets: {e}", font=("Arial", 11), fg=THEME["error"], bg=THEME["bg"]).pack(pady=10)

    btn_refresh.config(command=load_tickets)
    load_tickets() # Initial load
    canvas_tickets.focus_set()

# ===================================================================
# END OF STUDENT TICKET VIEW
# ===================================================================

# ... (rest of the code, including open_admin_panel, open_student_dashboard, mainloop) ...

def open_admin_panel():
    panel = tk.Toplevel(root)
    panel.title("Internship Tracker - Admin Panel")
    panel.state('zoomed')
    panel.configure(bg=THEME["bg"])
    add_logo(panel)

    def on_closing():
        root.deiconify()
        panel.destroy()

    panel.protocol("WM_DELETE_WINDOW", on_closing)

    notebook = ttk.Notebook(panel)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)

    # ===================================================================
    # TAB 1: Dashboard
    # ===================================================================
    dashboard_frame = tk.Frame(notebook, bg=THEME["bg"])
    notebook.add(dashboard_frame, text="Dashboard")

    dash_container = tk.Frame(dashboard_frame, bg=THEME["bg"])
    dash_container.pack(fill="both", expand=True, padx=10, pady=10)

    canvas_dash = tk.Canvas(dash_container, bg=THEME["bg"], highlightthickness=0)
    scrollbar_dash = tk.Scrollbar(dash_container, orient="vertical", command=canvas_dash.yview)
    scroll_frame_dash = tk.Frame(canvas_dash, bg=THEME["bg"])

    scroll_frame_dash.bind("<Configure>", lambda e: canvas_dash.configure(scrollregion=canvas_dash.bbox("all")))
    canvas_dash.create_window((0, 0), window=scroll_frame_dash, anchor="nw")
    canvas_dash.configure(yscrollcommand=scrollbar_dash.set)

    canvas_dash.pack(side="left", fill="both", expand=True)
    scrollbar_dash.pack(side="right", fill="y")
    setup_scrolling(canvas_dash)

    stats_frame = tk.Frame(scroll_frame_dash, bg=THEME["bg"])
    stats_frame.pack(pady=20, padx=20, fill="x")

    tk.Label(stats_frame, text="Application Analytics", font=("Arial", 18, "bold"), fg=THEME["fg"], bg=THEME["bg"]).pack(pady=10)

    # --- ### MODIFIED ### Stats Layout (2x3 Grid) ---
    top_row_frame = tk.Frame(stats_frame, bg=THEME["bg"])
    top_row_frame.pack(fill="x", pady=5)
    bottom_row_frame = tk.Frame(stats_frame, bg=THEME["bg"])
    bottom_row_frame.pack(fill="x", pady=5)

    def create_stat_box(parent, title, value_var, color):
        box_container = tk.Frame(parent, bg=THEME["bg"]) # Container to help with packing
        box_container.pack(side="left", fill="x", expand=True, padx=10)
        box = tk.Frame(box_container, bg=color, bd=5, relief="groove")
        box.pack(fill="x") # Fill within its container
        tk.Label(box, text=title, font=("Arial", 14, "bold"), fg="white", bg=color).pack(pady=(10,0))
        tk.Label(box, textvariable=value_var, font=("Arial", 22, "bold"), fg="white", bg=color).pack(pady=(0,10))
    # --- End Modified Stats Layout ---

    total_students_var = tk.StringVar(value="0")
    total_jobs_var = tk.StringVar(value="0")
    total_apps_var = tk.StringVar(value="0")
    total_selected_var = tk.StringVar(value="0")
    total_rejected_var = tk.StringVar(value="0")
    total_tickets_var = tk.StringVar(value="0")

    # Pack into rows
    create_stat_box(top_row_frame, "Total Registered Students", total_students_var, THEME["secondary"])
    create_stat_box(top_row_frame, "Total Jobs Posted", total_jobs_var, THEME["highlight"])
    create_stat_box(top_row_frame, "Total Applications Received", total_apps_var, THEME["warning"])
    create_stat_box(bottom_row_frame, "Total Students Selected", total_selected_var, THEME["success"])
    create_stat_box(bottom_row_frame, "Total Applications Rejected", total_rejected_var, THEME["error"])
    create_stat_box(bottom_row_frame, "Open Support Tickets", total_tickets_var, THEME["highlight"])


    def update_dashboard_stats():
        try:
            db = get_db()
            cursor = db.cursor()

            cursor.execute("SELECT COUNT(*) FROM students")
            total_students_var.set(str(cursor.fetchone()[0]))

            cursor.execute("SELECT COUNT(*) FROM jobs")
            total_jobs_var.set(str(cursor.fetchone()[0]))

            cursor.execute("SELECT COUNT(*) FROM applications")
            total_apps_var.set(str(cursor.fetchone()[0]))

            cursor.execute("SELECT COUNT(*) FROM applications WHERE status = 'Selected'")
            total_selected_var.set(str(cursor.fetchone()[0]))

            cursor.execute("SELECT COUNT(*) FROM applications WHERE status = 'Rejected'")
            total_rejected_var.set(str(cursor.fetchone()[0]))

            cursor.execute("SELECT COUNT(*) FROM support_tickets WHERE status = 'Open'")
            total_tickets_var.set(str(cursor.fetchone()[0]))

            cursor.close()
            db.close()
        except Exception as e:
            show_popup("Error", f"Could not load dashboard stats: {e}", "error")

    btn_refresh_dash = tk.Button(stats_frame, text="Refresh Stats", command=update_dashboard_stats,
                                 bg=THEME["highlight"], fg=THEME["bg"], font=("Arial", 10, "bold"), relief="flat", bd=0)
    btn_refresh_dash.pack(pady=20)
    btn_refresh_dash.bind("<Enter>", lambda e: btn_refresh_dash.configure(bg=THEME["secondary"]))
    btn_refresh_dash.bind("<Leave>", lambda e: btn_refresh_dash.configure(bg=THEME["highlight"]))

    # ... (Keep TAB 2: Post Job, TAB 3: Manage Jobs, TAB 4: Manage Students code) ...
     # ===================================================================
    # TAB 2: Post Job
    # ===================================================================
    post_frame = tk.Frame(notebook, bg=THEME["bg"])
    notebook.add(post_frame, text="Post Job")

    form_frame = tk.Frame(post_frame, bg=THEME["bg"])
    form_frame.pack(padx=20, pady=20, fill="x")

    tk.Label(form_frame, text="Post a New Job", font=("Arial", 14, "bold"), fg=THEME["fg"], bg=THEME["bg"]).grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(form_frame, text="Job Title", font=("Arial", 10), fg=THEME["fg"], bg=THEME["bg"]).grid(row=1, column=0, sticky="w", padx=10)
    job_title = tk.Entry(form_frame, width=40, font=("Arial", 10), relief="flat", bg="#F8F9FA", fg=THEME["fg"],
                         highlightthickness=1, highlightbackground=THEME["button_border"])
    job_title.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(form_frame, text="Company Name", font=("Arial", 10), fg=THEME["fg"], bg=THEME["bg"]).grid(row=2, column=0, sticky="w", padx=10)
    company_name = tk.Entry(form_frame, width=40, font=("Arial", 10), relief="flat", bg="#F8F9FA", fg=THEME["fg"],
                            highlightthickness=1, highlightbackground=THEME["button_border"])
    company_name.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(form_frame, text="Description", font=("Arial", 10), fg=THEME["fg"], bg=THEME["bg"]).grid(row=3, column=0, sticky="w", padx=10)
    desc = tk.Text(form_frame, width=60, height=4, font=("Arial", 10), relief="flat", bg="#F8F9FA", fg=THEME["fg"],
                   highlightthickness=1, highlightbackground=THEME["button_border"])
    desc.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(form_frame, text="Last Date (YYYY-MM-DD)", font=("Arial", 10), fg=THEME["fg"], bg=THEME["bg"]).grid(row=4, column=0, sticky="w", padx=10)
    last_date = tk.Entry(form_frame, width=40, font=("Arial", 10), relief="flat", bg="#F8F9FA", fg=THEME["fg"],
                         highlightthickness=1, highlightbackground=THEME["button_border"])
    last_date.grid(row=4, column=1, padx=10, pady=5)

    def post_job():
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("INSERT INTO jobs (title, company_name, description, last_date_to_apply) VALUES (%s,%s,%s,%s)",
                           (job_title.get(), company_name.get(), desc.get("1.0", "end").strip(), last_date.get()))
            db.commit()
            show_popup("Success", "Job Posted Successfully!", "success")
            job_title.delete(0, "end")
            company_name.delete(0, "end")
            desc.delete("1.0", "end")
            last_date.delete(0, "end")
            load_jobs_admin()
            update_dashboard_stats()
        except Exception as e:
            show_popup("Error", f"Failed to post job: {e}", "error")
        finally:
            cursor.close()
            db.close()

    btn_post = tk.Button(form_frame, text="Post Job", command=post_job, bg=THEME["highlight"], fg=THEME["bg"],
                         font=("Arial", 10, "bold"), relief="flat", bd=0, width=15)
    btn_post.grid(row=5, column=1, pady=20)
    btn_post.bind("<Enter>", lambda e: btn_post.configure(bg=THEME["secondary"]))
    btn_post.bind("<Leave>", lambda e: btn_post.configure(bg=THEME["highlight"]))

    # ===================================================================
    # TAB 3: Manage Jobs
    # ===================================================================
    manage_frame = tk.Frame(notebook, bg=THEME["bg"])
    notebook.add(manage_frame, text="Manage Jobs & Applications")

    search_frame = tk.Frame(manage_frame, bg=THEME["bg"])
    search_frame.pack(fill="x", padx=10, pady=5)
    tk.Label(search_frame, text="Search Jobs:", font=("Arial", 10), fg=THEME["fg"], bg=THEME["bg"]).pack(side="left")
    search_job_entry = tk.Entry(search_frame, width=30, font=("Arial", 10), relief="flat", bg="#F8F9FA", fg=THEME["fg"],
                                highlightthickness=1, highlightbackground=THEME["button_border"])
    search_job_entry.pack(side="left", padx=5)

    jobs_container = tk.Frame(manage_frame, bg=THEME["bg"])
    jobs_container.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    canvas_jobs = tk.Canvas(jobs_container, bg=THEME["bg"], highlightthickness=0)
    scrollbar_jobs = tk.Scrollbar(jobs_container, orient="vertical", command=canvas_jobs.yview)
    scroll_frame_jobs = tk.Frame(canvas_jobs, bg=THEME["bg"])
    scroll_frame_jobs.bind("<Configure>", lambda e: canvas_jobs.configure(scrollregion=canvas_jobs.bbox("all")))
    canvas_jobs.create_window((0, 0), window=scroll_frame_jobs, anchor="nw")
    canvas_jobs.configure(yscrollcommand=scrollbar_jobs.set)
    canvas_jobs.pack(side="left", fill="both", expand=True)
    scrollbar_jobs.pack(side="right", fill="y")
    setup_scrolling(canvas_jobs)

    right_frame = tk.Frame(manage_frame, bg=THEME["bg"])
    right_frame.pack(side="left", fill="both", expand=True, padx=10)
    apps_container = tk.Frame(right_frame, bg=THEME["bg"])
    apps_container.pack(fill="both", expand=True)
    canvas_apps = tk.Canvas(apps_container, bg=THEME["bg"], highlightthickness=0)
    scrollbar_apps = tk.Scrollbar(apps_container, orient="vertical", command=canvas_apps.yview)
    scroll_frame_apps = tk.Frame(canvas_apps, bg=THEME["bg"])
    scroll_frame_apps.bind("<Configure>", lambda e: canvas_apps.configure(scrollregion=canvas_apps.bbox("all")))
    canvas_apps.create_window((0, 0), window=scroll_frame_apps, anchor="nw")
    canvas_apps.configure(yscrollcommand=scrollbar_apps.set)
    canvas_apps.pack(side="left", fill="both", expand=True)
    scrollbar_apps.pack(side="right", fill="y")
    setup_scrolling(canvas_apps)

    # ===================================================================
    # TAB 4: Manage Students
    # ===================================================================
    student_frame = tk.Frame(notebook, bg=THEME["bg"])
    notebook.add(student_frame, text="Registered Students")

    search_student_frame = tk.Frame(student_frame, bg=THEME["bg"])
    search_student_frame.pack(fill="x", padx=10, pady=5)
    tk.Label(search_student_frame, text="Search Students:", font=("Arial", 10), fg=THEME["fg"], bg=THEME["bg"]).pack(side="left")
    search_student_entry = tk.Entry(search_student_frame, width=30, font=("Arial", 10), relief="flat", bg="#F8F9FA", fg=THEME["fg"],
                                    highlightthickness=1, highlightbackground=THEME["button_border"])
    search_student_entry.pack(side="left", padx=5)
    tk.Label(search_student_frame, text="Filter by Course:", font=("Arial", 10), fg=THEME["fg"], bg=THEME["bg"]).pack(side="left", padx=10)
    course_filter = tk.Entry(search_student_frame, width=20, font=("Arial", 10), relief="flat", bg="#F8F9FA", fg=THEME["fg"],
                             highlightthickness=1, highlightbackground=THEME["button_border"])
    course_filter.pack(side="left", padx=5)

    student_container = tk.Frame(student_frame, bg=THEME["bg"])
    student_container.pack(fill="both", expand=True, padx=10, pady=10)
    canvas_students = tk.Canvas(student_container, bg=THEME["bg"], highlightthickness=0)
    scrollbar_students = tk.Scrollbar(student_container, orient="vertical", command=canvas_students.yview)
    scroll_frame_students = tk.Frame(canvas_students, bg=THEME["bg"])
    scroll_frame_students.bind("<Configure>", lambda e: canvas_students.configure(scrollregion=canvas_students.bbox("all")))
    canvas_students.create_window((0, 0), window=scroll_frame_students, anchor="nw")
    canvas_students.configure(yscrollcommand=scrollbar_students.set)
    canvas_students.pack(side="left", fill="both", expand=True)
    scrollbar_students.pack(side="right", fill="y")
    setup_scrolling(canvas_students)

    # ===================================================================
    # TAB 5: Help & Support (Admin View) - ### MODIFIED ###
    # ===================================================================
    support_frame = tk.Frame(notebook, bg=THEME["bg"])
    notebook.add(support_frame, text="Help & Support")

    support_toolbar = tk.Frame(support_frame, bg=THEME["bg"])
    support_toolbar.pack(fill="x", padx=10, pady=5)
    btn_refresh_tickets = tk.Button(support_toolbar, text="Refresh Tickets",
                                    bg=THEME["highlight"], fg=THEME["bg"], font=("Arial", 10, "bold"), relief="flat", bd=0)
    btn_refresh_tickets.pack(side="left")
    btn_refresh_tickets.bind("<Enter>", lambda e: btn_refresh_tickets.configure(bg=THEME["secondary"]))
    btn_refresh_tickets.bind("<Leave>", lambda e: btn_refresh_tickets.configure(bg=THEME["highlight"]))

    support_container = tk.Frame(support_frame, bg=THEME["bg"])
    support_container.pack(fill="both", expand=True, padx=10, pady=10)
    canvas_support = tk.Canvas(support_container, bg=THEME["bg"], highlightthickness=0)
    scrollbar_support = tk.Scrollbar(support_container, orient="vertical", command=canvas_support.yview)
    scroll_frame_support = tk.Frame(canvas_support, bg=THEME["bg"])
    scroll_frame_support.bind("<Configure>", lambda e: canvas_support.configure(scrollregion=canvas_support.bbox("all")))
    canvas_support.create_window((0, 0), window=scroll_frame_support, anchor="nw")
    canvas_support.configure(yscrollcommand=scrollbar_support.set)
    canvas_support.pack(side="left", fill="both", expand=True)
    scrollbar_support.pack(side="right", fill="y")
    setup_scrolling(canvas_support)
    # ===================================================================
    # END OF TABS
    # ===================================================================

    def load_jobs_admin(search_term=""):
        # ... (keep existing load_jobs_admin code) ...
        for widget in scroll_frame_jobs.winfo_children():
            widget.destroy()
        db = get_db()
        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM jobs WHERE title LIKE %s OR company_name LIKE %s ORDER BY last_date_to_apply ASC"
        cursor.execute(query, (f"%{search_term}%", f"%{search_term}%"))
        jobs = cursor.fetchall()
        cursor.close()
        db.close()
        for job in jobs:
            frame = tk.Frame(scroll_frame_jobs, bg="#F8F9FA", bd=1, relief="solid")
            frame.pack(fill="x", pady=5, padx=5)
            label = tk.Label(frame, text=f"{job['id']}. {job['title']} - {job['company_name']}", font=("Arial", 11), fg=THEME["fg"], bg="#F8F9FA")
            label.pack(anchor="w", padx=10, pady=5)
            def select_job(j_id=job['id']):
                for w in scroll_frame_jobs.winfo_children():
                    w.configure(bg="#F8F9FA")
                frame.configure(bg="#E9ECEF")
                load_applicants_for_job(j_id)
            frame.bind("<Button-1>", lambda e, j_id=job['id']: select_job(j_id))
            label.bind("<Button-1>", lambda e, j_id=job['id']: select_job(j_id))

    def load_students(search_term="", course_term=""):
        # ... (keep existing load_students code) ...
        for widget in scroll_frame_students.winfo_children():
            widget.destroy()
        db = get_db()
        cursor = db.cursor(dictionary=True)
        query = "SELECT id, name, email, course FROM students WHERE name LIKE %s AND course LIKE %s ORDER BY id DESC"
        cursor.execute(query, (f"%{search_term}%", f"%{course_term}%"))
        students = cursor.fetchall()
        cursor.close()
        db.close()
        for student in students:
            frame = tk.Frame(scroll_frame_students, bg="#F8F9FA", bd=1, relief="solid")
            frame.pack(fill="x", pady=5, padx=5)
            info = f"{student['id']}. {student['name']} - {student['email']} ({student['course']})"
            tk.Label(frame, text=info, font=("Arial", 11), fg=THEME["fg"], bg="#F8F9FA").pack(side="left", padx=10)
            btn_view = tk.Button(frame, text="View Profile", command=lambda s_id=student['id']: open_admin_view_profile(s_id),
                                 bg=THEME["highlight"], fg=THEME["bg"], font=("Arial", 10, "bold"), relief="flat", bd=0)
            btn_view.pack(side="right", padx=10)
            btn_view.bind("<Enter>", lambda e, b=btn_view: b.configure(bg=THEME["secondary"]))
            btn_view.bind("<Leave>", lambda e, b=btn_view: b.configure(bg=THEME["highlight"]))

    def load_applicants_for_job(job_id):
        # ... (keep existing load_applicants_for_job code) ...
        for widget in scroll_frame_apps.winfo_children():
            widget.destroy()
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT a.id as app_id, s.id as student_id, s.name, s.email, s.technical_skills, a.status
            FROM applications a
            JOIN students s ON a.student_id = s.id
            WHERE a.job_id = %s
            ORDER BY CASE a.status
                WHEN 'Under Review' THEN 1
                WHEN 'Selected' THEN 2
                WHEN 'Rejected' THEN 3
                ELSE 4 END, a.apply_date DESC
        """, (job_id,))
        apps = cursor.fetchall()
        cursor.close()
        db.close()
        if not apps:
            tk.Label(scroll_frame_apps, text="No applications for this job.", font=("Arial", 11), fg=THEME["fg"], bg=THEME["bg"]).pack(pady=10)
            return
        for app in apps:
            frame = tk.Frame(scroll_frame_apps, bg="#F8F9FA", bd=1, relief="solid")
            frame.pack(fill="x", pady=5, padx=5)
            tk.Label(frame, text=f"Name: {app['name']}", font=("Arial", 11), fg=THEME["fg"], bg="#F8F9FA").pack(anchor="w", padx=10)
            tk.Label(frame, text=f"Email: {app['email']}", font=("Arial", 10), fg=THEME["fg"], bg="#F8F9FA").pack(anchor="w", padx=10)
            tk.Label(frame, text=f"Skills: {app['technical_skills']}", font=("Arial", 10), fg=THEME["fg"], bg="#F8F9FA").pack(anchor="w", padx=10)
            status_color = THEME["warning"] if app['status'] == "Under Review" else THEME["success"] if app['status'] == "Selected" else THEME["error"]
            tk.Label(frame, text=f"Status: {app['status']}", font=("Arial", 10, "bold"), fg=status_color, bg="#F8F9FA").pack(anchor="w", padx=10)
            btn_frame = tk.Frame(frame, bg="#F8F9FA")
            btn_frame.pack(anchor="e", padx=10, pady=5)
            btn_view = tk.Button(btn_frame, text="View Profile", command=lambda sid=app['student_id']: open_admin_view_profile(sid),
                                 bg=THEME["highlight"], fg=THEME["bg"], font=("Arial", 10, "bold"), relief="flat", bd=0)
            btn_view.pack(side="left", padx=2)
            btn_view.bind("<Enter>", lambda e, b=btn_view: b.configure(bg=THEME["secondary"]))
            btn_view.bind("<Leave>", lambda e, b=btn_view: b.configure(bg=THEME["highlight"]))

            def make_status_changer(app_id):
                def change_status(new_status):
                    db2 = get_db()
                    cur2 = db2.cursor()
                    cur2.execute("UPDATE applications SET status=%s WHERE id=%s", (new_status, app_id))
                    db2.commit()
                    cur2.close()
                    db2.close()
                    load_applicants_for_job(job_id)
                    update_dashboard_stats() # Refresh dashboard on status change
                return change_status

            changer = make_status_changer(app['app_id'])

            btn_selected = tk.Button(btn_frame, text="Selected", command=lambda c=changer: c("Selected"),
                                     bg=THEME["success"], fg=THEME["bg"], font=("Arial", 10, "bold"), relief="flat", bd=0)
            btn_selected.pack(side="left", padx=2)
            btn_selected.bind("<Enter>", lambda e, b=btn_selected: b.configure(bg=THEME["secondary"]))
            btn_selected.bind("<Leave>", lambda e, b=btn_selected: b.configure(bg=THEME["success"]))

            btn_rejected = tk.Button(btn_frame, text="Rejected", command=lambda c=changer: c("Rejected"),
                                     bg=THEME["error"], fg=THEME["bg"], font=("Arial", 10, "bold"), relief="flat", bd=0)
            btn_rejected.pack(side="left", padx=2)
            btn_rejected.bind("<Enter>", lambda e, b=btn_rejected: b.configure(bg=THEME["secondary"]))
            btn_rejected.bind("<Leave>", lambda e, b=btn_rejected: b.configure(bg=THEME["error"]))

            btn_review = tk.Button(btn_frame, text="Under Review", command=lambda c=changer: c("Under Review"),
                                   bg=THEME["warning"], fg=THEME["bg"], font=("Arial", 10, "bold"), relief="flat", bd=0)
            btn_review.pack(side="left", padx=2)
            btn_review.bind("<Enter>", lambda e, b=btn_review: b.configure(bg=THEME["secondary"]))
            btn_review.bind("<Leave>", lambda e, b=btn_review: b.configure(bg=THEME["warning"]))

    # ===================================================================
    # ### MODIFIED ### - ADMIN SUPPORT TICKET FUNCTIONS (Added Reply)
    # ===================================================================
    def reply_and_close_ticket(ticket_id, reply_text_widget):
        reply_message = reply_text_widget.get("1.0", "end").strip()
        if not reply_message:
            show_popup("Error", "Please enter a reply message.", "error")
            return

        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute("UPDATE support_tickets SET status = 'Closed', admin_reply = %s WHERE ticket_id = %s",
                           (reply_message, ticket_id))
            db.commit()
            cursor.close()
            db.close()
            load_support_tickets() # Refresh the list
            update_dashboard_stats() # Refresh the dashboard count
            show_popup("Success", "Reply sent and ticket closed.", "success")
        except Exception as e:
            show_popup("Error", f"Failed to reply and close ticket: {e}", "error")

    def load_support_tickets():
        for widget in scroll_frame_support.winfo_children():
            widget.destroy()

        try:
            db = get_db()
            cursor = db.cursor(dictionary=True)
            query = """
                SELECT t.*, s.name, s.email
                FROM support_tickets t
                JOIN students s ON t.student_id = s.id
                ORDER BY CASE WHEN t.status = 'Open' THEN 1 ELSE 2 END, t.created_at DESC
            """
            cursor.execute(query)
            tickets = cursor.fetchall()
            cursor.close()
            db.close()

            if not tickets:
                tk.Label(scroll_frame_support, text="No support tickets found.", font=("Arial", 11), fg=THEME["fg"], bg=THEME["bg"]).pack(pady=10)
                return

            for ticket in tickets:
                frame = tk.Frame(scroll_frame_support, bg="#F8F9FA", bd=1, relief="solid")
                frame.pack(fill="x", pady=5, padx=5)

                header_frame = tk.Frame(frame, bg="#F8F9FA")
                header_frame.pack(fill="x", padx=10, pady=5)

                tk.Label(header_frame, text=f"From: {ticket['name']} ({ticket['email']})", font=("Arial", 11, "bold"), fg=THEME["fg"], bg="#F8F9FA").pack(anchor="w")
                tk.Label(header_frame, text=f"Subject: {ticket['subject']}", font=("Arial", 10, "bold"), fg=THEME["fg"], bg="#F8F9FA").pack(anchor="w")
                tk.Label(header_frame, text=f"Submitted: {ticket['created_at'].strftime('%Y-%m-%d %H:%M')}", font=("Arial", 9, "italic"), fg=THEME["secondary"], bg="#F8F9FA").pack(anchor="w")

                tk.Label(frame, text="Student Message:", font=("Arial", 10, "bold"), fg=THEME["fg"], bg="#F8F9FA").pack(anchor="w", padx=10, pady=(5,0))
                tk.Label(frame, text=ticket['message'], wraplength=panel.winfo_width() - 100, justify="left", font=("Arial", 10), fg=THEME["fg"], bg="#F8F9FA").pack(anchor="w", padx=10, pady=(0,5))

                status_color = THEME["success"] if ticket['status'] == 'Closed' else THEME["error"]
                tk.Label(frame, text=f"Status: {ticket['status']}", font=("Arial", 10, "bold"), fg=status_color, bg="#F8F9FA").pack(anchor="w", padx=10, pady=5)

                if ticket['status'] == 'Open':
                    # Add reply section for open tickets
                    reply_label = tk.Label(frame, text="Your Reply:", font=("Arial", 10, "bold"), fg=THEME["fg"], bg="#F8F9FA")
                    reply_label.pack(anchor="w", padx=10, pady=(5,0))
                    reply_text = tk.Text(frame, height=3, width=60, font=("Arial", 10), relief="flat", bg="#FFFFFF", fg=THEME["fg"],
                                         highlightthickness=1, highlightbackground=THEME["button_border"])
                    reply_text.pack(fill="x", padx=10, pady=(0,5))

                    btn_reply_close = tk.Button(frame, text="Send Reply & Close Ticket",
                                                 command=lambda t_id=ticket['ticket_id'], rt=reply_text: reply_and_close_ticket(t_id, rt),
                                                 bg=THEME["success"], fg=THEME["bg"], font=("Arial", 10, "bold"), relief="flat", bd=0)
                    btn_reply_close.pack(anchor="e", padx=10, pady=5)
                    btn_reply_close.bind("<Enter>", lambda e, b=btn_reply_close: b.configure(bg=THEME["secondary"]))
                    btn_reply_close.bind("<Leave>", lambda e, b=btn_reply_close: b.configure(bg=THEME["success"]))
                elif ticket['admin_reply']:
                    # Show existing reply for closed tickets
                    tk.Label(frame, text="Admin Reply:", font=("Arial", 10, "bold"), fg=THEME["fg"], bg="#F8F9FA").pack(anchor="w", padx=10, pady=(5,0))
                    reply_bg = "#E0FFE0" # Light green for reply
                    tk.Label(frame, text=ticket['admin_reply'], wraplength=panel.winfo_width() - 100, justify="left", font=("Arial", 10), fg=THEME["fg"], bg=reply_bg, relief="groove", borderwidth=1).pack(anchor="w", padx=10, pady=(0,10), fill="x")


        except Exception as e:
            tk.Label(scroll_frame_support, text=f"Error loading tickets: {e}", font=("Arial", 11), fg=THEME["error"], bg=THEME["bg"]).pack(pady=10)

    btn_refresh_tickets.config(command=load_support_tickets)
    # ===================================================================
    # END OF ADMIN SUPPORT TICKET FUNCTIONS
    # ===================================================================

    def search_jobs(event=None):
        load_jobs_admin(search_job_entry.get())

    def search_students(event=None):
        load_students(search_student_entry.get(), course_filter.get())

    search_job_entry.bind("<KeyRelease>", search_jobs)
    search_student_entry.bind("<KeyRelease>", search_students)
    course_filter.bind("<KeyRelease>", search_students)

    def on_tab_changed(event):
        # ... (keep existing on_tab_changed code) ...
        selected_tab_index = notebook.index(notebook.select())
        # Give focus to the primary scrollable canvas in each tab
        if selected_tab_index == 0: # Dashboard
            canvas_dash.focus_set()
        elif selected_tab_index == 2: # Manage Jobs
            canvas_jobs.focus_set() # Focus left panel (jobs list)
        elif selected_tab_index == 3: # Manage Students
            canvas_students.focus_set()
        elif selected_tab_index == 4: # Help & Support
            canvas_support.focus_set()
        # No specific focus needed for 'Post Job' tab

    notebook.bind("<<NotebookTabChanged>>", on_tab_changed)

    # Initial data load
    update_dashboard_stats()
    load_jobs_admin()
    load_students()
    load_support_tickets()
    canvas_dash.focus_set() # Set initial focus


def open_student_dashboard(student_id, student_name):
    dash = tk.Toplevel(root)
    dash.title(f"Internship Tracker - Student Dashboard - {student_name}")
    dash.state('zoomed')
    dash.configure(bg=THEME["bg"])
    add_logo(dash)

    def on_closing():
        root.deiconify()
        dash.destroy()

    dash.protocol("WM_DELETE_WINDOW", on_closing)

    header = tk.Frame(dash, bg=THEME["bg"])
    header.pack(fill="x", pady=10)
    tk.Label(header, text=f"Welcome {student_name}", font=("Arial", 16, "bold"), fg=THEME["fg"], bg=THEME["bg"]).pack(side="left", padx=20)

    # --- ### MODIFIED ### - Added "My Support Tickets" Button ---
    btn_my_tickets = tk.Button(header, text="My Support Tickets", command=lambda: open_my_tickets(student_id),
                             bg=THEME["secondary"], fg=THEME["bg"], font=("Arial", 10, "bold"), relief="flat", bd=0)
    btn_my_tickets.pack(side="right", padx=10)
    btn_my_tickets.bind("<Enter>", lambda e: btn_my_tickets.configure(bg=THEME["highlight"]))
    btn_my_tickets.bind("<Leave>", lambda e: btn_my_tickets.configure(bg=THEME["secondary"]))
    # --- End Modified ---

    btn_help = tk.Button(header, text="Help & Support", command=lambda: open_support_window(student_id),
                         bg=THEME["warning"], fg=THEME["bg"], font=("Arial", 10, "bold"), relief="flat", bd=0)
    btn_help.pack(side="right", padx=10)
    btn_help.bind("<Enter>", lambda e: btn_help.configure(bg=THEME["secondary"]))
    btn_help.bind("<Leave>", lambda e: btn_help.configure(bg=THEME["warning"]))

    btn_profile = tk.Button(header, text="My Profile", command=lambda: open_student_profile(student_id),
                            bg=THEME["highlight"], fg=THEME["bg"], font=("Arial", 10, "bold"), relief="flat", bd=0)
    btn_profile.pack(side="right", padx=10)
    btn_profile.bind("<Enter>", lambda e: btn_profile.configure(bg=THEME["secondary"]))
    btn_profile.bind("<Leave>", lambda e: btn_profile.configure(bg=THEME["highlight"]))

    # ... (Keep rest of student dashboard code, including load_jobs, apply_job, load_applications, etc.) ...
    btn_frame = tk.Frame(dash, bg=THEME["bg"])
    btn_frame.pack(fill="x", pady=10)
    btn_jobs = tk.Button(btn_frame, text="Jobs", width=15, bg=THEME["highlight"], fg=THEME["bg"],
                         font=("Arial", 10, "bold"), relief="flat", bd=0)
    btn_jobs.pack(side="left", padx=10)
    btn_jobs.bind("<Enter>", lambda e: btn_jobs.configure(bg=THEME["secondary"]))
    btn_jobs.bind("<Leave>", lambda e: btn_jobs.configure(bg=THEME["highlight"]))
    btn_apps = tk.Button(btn_frame, text="My Applications", width=15, bg=THEME["highlight"], fg=THEME["bg"],
                         font=("Arial", 10, "bold"), relief="flat", bd=0)
    btn_apps.pack(side="left", padx=10)
    btn_apps.bind("<Enter>", lambda e: btn_apps.configure(bg=THEME["secondary"]))
    btn_apps.bind("<Leave>", lambda e: btn_apps.configure(bg=THEME["highlight"]))
    btn_refresh = tk.Button(btn_frame, text="Refresh", width=15, bg=THEME["highlight"], fg=THEME["bg"],
                            font=("Arial", 10, "bold"), relief="flat", bd=0)
    btn_refresh.pack(side="left", padx=10)
    btn_refresh.bind("<Enter>", lambda e: btn_refresh.configure(bg=THEME["secondary"]))
    btn_refresh.bind("<Leave>", lambda e: btn_refresh.configure(bg=THEME["highlight"]))
    sort_var = tk.StringVar(value="Sort by: Apply Date")
    sort_menu = ttk.OptionMenu(btn_frame, sort_var, "Sort by: Apply Date", "Sort by: Apply Date", "Sort by: Status")
    sort_menu.pack(side="left", padx=10)

    jobs_container = tk.Frame(dash, bg=THEME["bg"])
    canvas_jobs = tk.Canvas(jobs_container, bg=THEME["bg"], highlightthickness=0, height=420)
    scrollbar_jobs = tk.Scrollbar(jobs_container, orient="vertical", command=canvas_jobs.yview)
    scroll_frame_jobs = tk.Frame(canvas_jobs, bg=THEME["bg"])
    scroll_frame_jobs.bind("<Configure>", lambda e: canvas_jobs.configure(scrollregion=canvas_jobs.bbox("all")))
    canvas_jobs.create_window((0, 0), window=scroll_frame_jobs, anchor="nw")
    canvas_jobs.configure(yscrollcommand=scrollbar_jobs.set)
    canvas_jobs.pack(side="left", fill="both", expand=True)
    scrollbar_jobs.pack(side="right", fill="y")
    setup_scrolling(canvas_jobs)

    apps_container = tk.Frame(dash, bg=THEME["bg"])
    canvas_apps = tk.Canvas(apps_container, bg=THEME["bg"], highlightthickness=0, height=420)
    scrollbar_apps = tk.Scrollbar(apps_container, orient="vertical", command=canvas_apps.yview)
    scroll_frame_apps = tk.Frame(canvas_apps, bg=THEME["bg"])
    scroll_frame_apps.bind("<Configure>", lambda e: canvas_apps.configure(scrollregion=canvas_apps.bbox("all")))
    canvas_apps.create_window((0, 0), window=scroll_frame_apps, anchor="nw")
    canvas_apps.configure(yscrollcommand=scrollbar_apps.set)
    canvas_apps.pack(side="left", fill="both", expand=True)
    scrollbar_apps.pack(side="right", fill="y")
    setup_scrolling(canvas_apps)

    def load_jobs():
        for w in scroll_frame_jobs.winfo_children():
            w.destroy()
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM jobs ORDER BY last_date_to_apply ASC")
        jobs = cursor.fetchall()
        cursor.close()
        db.close()
        if not jobs:
            tk.Label(scroll_frame_jobs, text="No jobs available at the moment.", font=("Arial", 11), fg=THEME["fg"], bg=THEME["bg"]).pack(pady=10)
            return
        for job in jobs:
            frame = tk.Frame(scroll_frame_jobs, bg="#F8F9FA", bd=1, relief="solid")
            frame.pack(fill="x", pady=5, padx=10)
            tk.Label(frame, text=f"{job['title']}  —  {job['company_name']}", font=("Arial", 13, "bold"), fg=THEME["fg"], bg="#F8F9FA").pack(anchor="w", padx=10)
            tk.Label(frame, text=job['description'], wraplength=dash.winfo_width() - 100, justify="left", font=("Arial", 10), fg=THEME["fg"], bg="#F8F9FA").pack(anchor="w", padx=10, pady=5)
            tk.Label(frame, text=f"Apply By: {job['last_date_to_apply']}", font=("Arial", 10), fg=THEME["fg"], bg="#F8F9FA").pack(anchor="w", padx=10)
            btn_apply = tk.Button(frame, text="Apply", command=lambda j_id=job['id']: apply_job(j_id), bg=THEME["success"], fg=THEME["bg"],
                                  font=("Arial", 10, "bold"), relief="flat", bd=0, width=10)
            btn_apply.pack(anchor="e", padx=10, pady=5)
            btn_apply.bind("<Enter>", lambda e, b=btn_apply: b.configure(bg=THEME["secondary"]))
            btn_apply.bind("<Leave>", lambda e, b=btn_apply: b.configure(bg=THEME["success"]))

    def apply_job(j_id):
        db_check = get_db()
        cur_check_prof = db_check.cursor(dictionary=True)
        cur_check_prof.execute("SELECT resume_path, technical_skills FROM students WHERE id=%s", (student_id,))
        profile = cur_check_prof.fetchone()
        cur_check_prof.close()
        db_check.close()
        if not profile or not profile.get('resume_path') or not profile.get('technical_skills') or not profile['technical_skills'].strip():
            show_popup("Error", "Please complete your profile (resume & skills) before applying.", "error")
            return
        db_apply = get_db()
        cur_check = db_apply.cursor()
        cur_check.execute("SELECT * FROM applications WHERE student_id=%s AND job_id=%s", (student_id, j_id))
        if cur_check.fetchone():
            show_popup("Info", "You have already applied for this job.", "info")
            cur_check.close()
            db_apply.close()
            return
        cur_apply = db_apply.cursor()
        cur_apply.execute("INSERT INTO applications (student_id, job_id, apply_date) VALUES (%s, %s, CURDATE())", (student_id, j_id))
        db_apply.commit()
        cur_apply.close()
        db_apply.close()
        show_popup("Success", "You have successfully applied for this job!", "success")
        load_jobs()
        if apps_container.winfo_ismapped():
            load_applications()

    def load_applications():
        for w in scroll_frame_apps.winfo_children():
            w.destroy()
        db = get_db()
        cursor = db.cursor(dictionary=True)
        sort_order = "CASE a.status WHEN 'Under Review' THEN 1 WHEN 'Selected' THEN 2 WHEN 'Rejected' THEN 3 ELSE 4 END" if sort_var.get() == "Sort by: Status" else "a.apply_date DESC"
        cursor.execute(f"""
            SELECT a.id as app_id, j.title, j.company_name, a.apply_date, a.status
            FROM applications a
            JOIN jobs j ON a.job_id = j.id
            WHERE a.student_id = %s
            ORDER BY {sort_order}
        """, (student_id,))
        apps = cursor.fetchall()
        cursor.close()
        db.close()
        if not apps:
            tk.Label(scroll_frame_apps, text="You have not applied to any jobs yet.", font=("Arial", 11), fg=THEME["fg"], bg=THEME["bg"]).pack(pady=10)
            return
        for app in apps:
            frame = tk.Frame(scroll_frame_apps, bg="#F8F9FA", bd=1, relief="solid")
            frame.pack(fill="x", pady=5, padx=10)
            tk.Label(frame, text=f"{app['title']}  —  {app['company_name']}", font=("Arial", 12, "bold"), fg=THEME["fg"], bg="#F8F9FA").pack(anchor="w", padx=10)
            tk.Label(frame, text=f"Applied On: {app['apply_date']}", font=("Arial", 10), fg=THEME["fg"], bg="#F8F9FA").pack(anchor="w", padx=10, pady=2)
            status_color = THEME["warning"] if app['status'] == "Under Review" else THEME["success"] if app['status'] == "Selected" else THEME["error"]
            status_frame = tk.Frame(frame, bg=status_color)
            status_frame.pack(anchor="w", padx=10, pady=2)
            tk.Label(status_frame, text=f"Status: {app['status']}", font=("Arial", 10, "bold"), fg=THEME["bg"], bg=status_color).pack(padx=10, pady=5)
            if app['status'] == "Under Review":
                btn_withdraw = tk.Button(frame, text="Withdraw", command=lambda a_id=app['app_id'], status=app['status']: withdraw(a_id, status),
                                         bg=THEME["error"], fg=THEME["bg"], font=("Arial", 10, "bold"), relief="flat", bd=0, width=10)
                btn_withdraw.pack(anchor="e", padx=10, pady=5)
                btn_withdraw.bind("<Enter>", lambda e, b=btn_withdraw: b.configure(bg=THEME["secondary"]))
                btn_withdraw.bind("<Leave>", lambda e, b=btn_withdraw: b.configure(bg=THEME["error"]))

    def withdraw(a_id, status):
        if status != "Under Review":
            show_popup("Info", "You can withdraw only when status is 'Under Review'.", "info")
            return
        popup = tk.Toplevel()
        popup.title("Confirm Withdrawal")
        popup.geometry("350x150")
        popup.configure(bg=THEME["bg"])
        popup.lift()
        popup.grab_set()
        tk.Label(popup, text="Are you sure you want to withdraw this application?", font=("Arial", 11), fg=THEME["fg"], bg=THEME["bg"], wraplength=300).pack(pady=20)
        btn_frame = tk.Frame(popup, bg=THEME["bg"])
        btn_frame.pack(pady=10)
        btn_yes = tk.Button(btn_frame, text="Yes", command=lambda: confirm_withdraw(a_id, popup), bg=THEME["error"], fg=THEME["bg"],
                            font=("Arial", 10, "bold"), relief="flat", bd=0)
        btn_yes.pack(side="left", padx=5)
        btn_yes.bind("<Enter>", lambda e: btn_yes.configure(bg=THEME["secondary"]))
        btn_yes.bind("<Leave>", lambda e: btn_yes.configure(bg=THEME["error"]))
        btn_no = tk.Button(btn_frame, text="No", command=popup.destroy, bg=THEME["highlight"], fg=THEME["bg"],
                           font=("Arial", 10, "bold"), relief="flat", bd=0)
        btn_no.pack(side="left", padx=5)
        btn_no.bind("<Enter>", lambda e: btn_no.configure(bg=THEME["secondary"]))
        btn_no.bind("<Leave>", lambda e: btn_no.configure(bg=THEME["highlight"]))

    def confirm_withdraw(a_id, popup):
        db_w = get_db()
        cur_w = db_w.cursor()
        cur_w.execute("DELETE FROM applications WHERE id=%s", (a_id,))
        db_w.commit()
        cur_w.close()
        db_w.close()
        show_popup("Success", "Application withdrawn.", "success")
        popup.destroy()
        load_applications()

    def show_jobs():
        apps_container.pack_forget()
        jobs_container.pack(fill="both", expand=True, padx=10, pady=10)
        load_jobs()
        btn_refresh.config(command=load_jobs)
        canvas_jobs.focus_set()

    def show_applications():
        jobs_container.pack_forget()
        apps_container.pack(fill="both", expand=True, padx=10, pady=10)
        load_applications()
        btn_refresh.config(command=load_applications)
        canvas_apps.focus_set()

    btn_jobs.config(command=show_jobs)
    btn_apps.config(command=show_applications)
    sort_var.trace("w", lambda *args: load_applications())

    show_jobs() # Load jobs first
    canvas_jobs.focus_set() # Set initial focus

root.mainloop()