from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import mysql.connector
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# connecting to edupedia database
edupedia = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root1234",
    database="edupedia"
)
edupedia_cursor = edupedia.cursor()

# Tkinter window
window = Tk()
window.geometry('1280x700')
window.title("home".center(100))  # centering the title ?
window.config(bg="black")
eqe=""

# login
def student(s,button_stud,button_inst,button_comp,logo_label1):
    user = s
    logo_label.place_forget()
    logo_label1.place_forget()

    login(frame_stud_log, user,button_stud,button_inst,button_comp)


def institute(i,button_stud,button_inst,button_comp,logo_label1):
    user = i
    logo_label.place_forget()
    logo_label1.place_forget()
    login(frame_inst_log, user,button_stud,button_inst,button_comp)


def company(c,button_stud,button_inst,button_comp,logo_label1):
    user = c
    logo_label.place_forget()
    logo_label1.place_forget()
    login(frame_comp_log, user,button_stud,button_inst,button_comp)


# validating username and password
def validate_account(frame, entry_usr, entry_pwd, user):
    # cheking which category is loging in
    if user == "student":
        table = "student_login"
    elif user == "institute":
        table = "institute_login"
    else:
        table = "company_login"

    # validating account
    sql = f"select * from {table} where user_name = %s and password = %s"
    values = (entry_usr.get(), entry_pwd.get())
    edupedia_cursor.execute(sql, values)
    # collecting the matches from the login table
    results = edupedia_cursor.fetchall()
    # checking if any matches found for given username and password
    if results:
        # messagebox.showinfo("success", "Login Successful")

        profile(frame, entry_usr.get(), user)
    # if username and password does not match or exist
    else:
        messagebox.showerror("Failed", "Username or password is incorrect")


def forget(frame,button_stud,button_inst,button_comp):
    def home(frame):
        frame.place_forget()
        into()

    def back(frame_forget):
        frame_forget.place_forget()
        frame.place(x=350, y=200)

    def recovery_mail(entry_mail):
        if entry_mail.get() == "":
            messagebox.showerror("Oops..!", "Enter mail adddress")
        else:
            messagebox.showinfo("Success", f"Recovery mail has been sent to \"{entry_mail.get()}\"")
            frame_forget.place_forget()
            frame.place(x=350, y=200)

    frame.place_forget()

    frame_forget = Frame(label_main,bg="#0572b5")
    frame_forget.place(x=350, y=200)

    button_back = Button(frame_forget, text="X",width=2,bg="red", command=lambda: back(frame_forget))
    inside_frame = Frame(frame_forget, bg="#b2e9f7")
    button_back.grid(row=0, column=0, sticky="e")
    inside_frame.grid(row=1, column=0, pady=10, padx=10)

    label_mail = Label(inside_frame, text="Enter mail address ", bg="#b2e9f7", font=("Helvetica", "16"))
    entry_mail = Entry(inside_frame, font=("Helvetica", "16"))
    button_submit = Button(inside_frame, text="Send recovery mail", height=1, width=15, bg="green",fg="yellow",font=("Comic Sans MS", 15, "bold"),
                           activebackground="#b2e9f7",activeforeground="#040742",
                           command=lambda: recovery_mail(entry_mail))

    label_mail.grid(row=1, column=0, padx=20, pady=20)
    entry_mail.grid(row=1, column=1, padx=20, pady=20)
    button_submit.grid(row=2, column=1, pady=20)


# login window
def login(frame, user,button_stud,button_inst,button_comp):

    button_stud.place_forget()
    button_inst.place_forget()
    button_comp.place_forget()


    def home(frame):
        inside_frame.place_forget()
        frame.place_forget()
        # button_stud.place(x=540, y=300)
        # button_inst.place(x=540, y=375)
        # button_comp.place(x=540, y=450)
        into()


    frame.place(x=350,y=200)
    button_back = Button(frame, text="X",width=2,bg="red",fg="white" ,font=("Helvetica", "12"),command=lambda: home(frame))
    inside_frame=Frame(frame,bg="#b2e9f7")
    button_back.grid(row=0,column=0,sticky="e")
    inside_frame.grid(row=1,column=0,pady=10,padx=10)
    label_usr = Label(inside_frame, text="Enter Username ", bg="#b2e9f7", font=("Helvetica", "16"))
    entry_usr = Entry(inside_frame, font=("Helvetica", "16"))
    label_pwd = Label(inside_frame, text="Enter Password ", bg='#b2e9f7', font=("Helvetica", "16"))
    entry_pwd = Entry(inside_frame, show="*", font=("Helvetica", "16"))
    v = IntVar(value=0)
    check_pwd = Checkbutton(inside_frame, text="show password", variable=v, onvalue=1, offvalue=0,
                            command=lambda: showpsd(v, entry_pwd))
    button_submit = Button(inside_frame, text="log-in", height=1, width=10, bg="blue",fg="white",font=("Comic Sans MS", 15, "bold"),
                           command=lambda: validate_account(frame, entry_usr, entry_pwd, user),activebackground="#b2e9f7",activeforeground="#040742")
    button_forget = Button(inside_frame, text="forgot password", fg="blue", command=lambda: forget(frame,button_stud,button_inst,button_comp))
    button_create = Button(inside_frame, text="Create account", fg="blue", command=lambda: create_uesr(frame, user,button_stud,button_inst,button_comp))

    label_usr.grid(row=1, column=0, padx=10, pady=20)
    entry_usr.grid(row=1, column=1)
    label_pwd.grid(row=2, column=0)
    entry_pwd.grid(row=2, column=1,padx=10)
    check_pwd.grid(row=2, column=2, padx=10)
    button_submit.grid(row=3, column=1, pady=20)
    button_forget.grid(row=3, column=2,padx=10)
    button_create.grid(row=1, column=2)


def showpsd(v, entry_pwd):
    if v.get() == 1:
        entry_pwd.config(show='')
    else:
        entry_pwd.config(show='*')


def profile(frame, username, user):

    frame.place_forget()

    def update_profile(frame, username, user):
        def save_profile():
            # values enetered by user
            update_value = []
            update_value.append(entry_Name.get())
            update_value.append(entry_email.get())
            update_value.append(entry_phone_number.get())
            update_value.append(entry_address.get())
            if user == "student":
                update_value.append(entry_college.get())
                update_value.append(entry_course.get())
                update_value.append(entry_interested_areas.get())
                # respective column name in table
                update_column = ["name", "email", "phone_number", "address", "college", "course", "interested_areas"]
                # table name
                table = "student_profile"
            elif user == "institute":
                update_value.append(entry_courses_offered.get())
                update_column = ["institute_name", "email", "phone_number", "address", "courses_offered"]
                table = "institute_profile"

            else:
                update_value.append(entry_services_offered.get())
                update_column = ["company_name", "email", "phone_number", "address", "services_provided"]
                table = "company_profile"


            try:
                for i in range(len(update_column)):
                    if update_value[i] != "":
                        sql_update_profile = f"UPDATE {table} SET {update_column[i]} = %s WHERE (username = %s)"
                        value_update_profile = (str(update_value[i]), username)
                        edupedia_cursor.execute(sql_update_profile, value_update_profile)
                        edupedia.commit()
                messagebox.showinfo("Success", "Profile updated succesfully")
                frame_update_profile.place_forget()
            except Exception as error:
                messagebox.showerror("Error...!", f"{error}\nPlease contact the administrators")

        def cancel():
            frame_update_profile.place_forget()

        frame_update_profile = Frame(center_frame, bg="#0572b5")
        button_back = Button(frame_update_profile, text="X", width=2, bg="red", command=lambda: cancel())
        inside_frame = Frame(frame_update_profile, bg="#b2e9f7",)
        button_back.grid(row=0, column=0, sticky="e")
        inside_frame.grid(row=1, column=0, pady=10, padx=10)
        frame_update_profile.place(x=200, y=50)

        label_Name = Label(inside_frame, text="Name ", bg="#b2e9f7", font=("Helvetica", "16"))
        entry_Name = Entry(inside_frame, font=("Helvetica", "16"),width=30)
        label_email = Label(inside_frame, text="email ", bg="#b2e9f7", font=("Helvetica", "16"))
        entry_email = Entry(inside_frame, font=("Helvetica", "16"),width=30)
        label_phone_number = Label(inside_frame, text="Phone number ", bg="#b2e9f7", font=("Helvetica", "16"))
        entry_phone_number = Entry(inside_frame, font=("Helvetica", "16"),width=30)
        label_address = Label(inside_frame, text="Address ", bg="#b2e9f7", font=("Helvetica", "16"))
        entry_address = Entry(inside_frame, font=("Helvetica", "16"),width=30)

        button_submit = Button(inside_frame, text="save", height=2, width=15, bg="blue",fg="white",
                               command=lambda: save_profile())
        if user == "student":
            label_college = Label(inside_frame, text="College ", bg="#b2e9f7", font=("Helvetica", "16"))
            entry_college = Entry(inside_frame, font=("Helvetica", "16"),width=30)
            label_course = Label(inside_frame, text="Course ", bg="#b2e9f7", font=("Helvetica", "16"))
            entry_course = Entry(inside_frame, font=("Helvetica", "16"),width=30)
            label_interested_areas = Label(inside_frame, text="Interested areas ", bg="#b2e9f7",
                                           font=("Helvetica", "16"))
            entry_interested_areas = Entry(inside_frame, font=("Helvetica", "16"),width=30)

            label_college.grid(row=4, column=0, pady=10,sticky="w")
            entry_college.grid(row=4, column=1,sticky="e",padx=10)
            label_course.grid(row=5, column=0,sticky="w")
            entry_course.grid(row=5, column=1,sticky="e",padx=10)
            label_interested_areas.grid(row=6, column=0,pady=10,sticky="w")
            entry_interested_areas.grid(row=6, column=1,sticky="e",padx=10)

        elif user == "institute":
            label_courses_offered = Label(inside_frame, text="Courses Offered ", bg="#b2e9f7",
                                          font=("Helvetica", "16"),)
            entry_courses_offered = Entry(inside_frame, font=("Helvetica", "16"),width=30)
            label_courses_offered.grid(row=4, column=0,sticky="w",pady=10)
            entry_courses_offered.grid(row=4, column=1,sticky="e",padx=10)
        else:
            label_services_offered = Label(inside_frame, text="Services Providing ", bg="#b2e9f7",
                                           font=("Helvetica", "16"))
            entry_services_offered = Entry(inside_frame, font=("Helvetica", "16"),width=30)
            label_services_offered.grid(row=4, column=0,sticky="w",pady=10)
            entry_services_offered.grid(row=4, column=1,sticky="e",padx=10)

        label_Name.grid(row=0, column=0, pady=10,sticky="w")
        entry_Name.grid(row=0, column=1,sticky="e",padx=10)
        label_email.grid(row=1, column=0,sticky="w")
        entry_email.grid(row=1, column=1,sticky="e",padx=10)
        label_phone_number.grid(row=2, column=0,pady=10,sticky="w")
        entry_phone_number.grid(row=2, column=1,sticky="e",padx=10)
        label_address.grid(row=3, column=0,sticky="w")
        entry_address.grid(row=3, column=1,sticky="e",padx=10)
        button_submit.grid(row=8, column=1, pady=20)
    def create_blog(frame, username, user):

        def submit_create_blog():
            sql_submit_blog = f"INSERT INTO blogs (username,author_name,category,blog_name,blog,tags) VALUES (%s,%s,%s,%s,%s,%s)"
            create_blog_values = (
            username, author_name_entry.get(), category_entry.get(), blog_name_entry.get(), blog_text_value,
            tags_entry.get())
            edupedia_cursor.execute(sql_submit_blog, create_blog_values)
            edupedia.commit()
            messagebox.showinfo("Success", "Your blog has been uploaded succesfully")
            close(create_blog_frame)

        create_blog_frame = Frame(center_frame, width=800, height=550, bg="#0572b5")
        button_back =  Button(create_blog_frame,text="X",width=2,bg="red",fg="white" ,font=("Helvetica", "12"),command=lambda: close(create_blog_frame))
        inside_frame = Frame(create_blog_frame, bg="#b2e9f7")
        button_back.grid(row=0, column=0, sticky="e")
        inside_frame.grid(row=1, column=0, pady=10, padx=10)

        author_name_label = Label(inside_frame, text="Author_name", font=("Helvetica", "16"),
                                  bg="#b2e9f7", anchor="nw", width=15)
        author_name_entry = Entry(inside_frame, font=("Helvetica", "16"), width=50)
        category_label = Label(inside_frame, text="Category", font=("Helvetica", "16"),   bg="#b2e9f7",
                               anchor="nw", width=15)
        category_entry = Entry(inside_frame, font=("Helvetica", "16"), width=50)
        blog_name_label = Label(inside_frame, text="Blog_name", font=("Helvetica", "16"),
                                bg="#b2e9f7", anchor="nw", width=15)
        blog_name_entry = Entry(inside_frame, font=("Helvetica", "16"), width=50)
        blog_label = Label(inside_frame, text="Blog", font=("Helvetica", "16"),   bg="#b2e9f7",
                           anchor="nw", width=15)
        blog_text = Text(inside_frame, font=("Helvetica", "16"), width=50, height=5)
        blog_text_value = blog_text.get(1.0, "end-1c")
        tags_label = Label(inside_frame, text="Tags", font=("Helvetica", "16"),
                           bg="#b2e9f7", anchor="nw", width=15)
        tags_entry = Entry(inside_frame, font=("Helvetica", "16"), width=50)
        create_button = Button(inside_frame, text="Create", width=6,bg="blue",fg="white",font=("Helvetica", "16"), command=lambda: submit_create_blog())

        create_blog_frame.place(x=100, y=20)
        author_name_label.grid(row=2, column=0,pady=10,padx=5)
        author_name_entry.grid(row=2, column=1,sticky="e",padx=10)
        category_label.grid(row=3, column=0, pady=10)
        category_entry.grid(row=3, column=1,sticky="e",padx=10)
        blog_name_label.grid(row=4, column=0)
        blog_name_entry.grid(row=4, column=1,sticky="e",padx=10)
        blog_label.grid(row=5, column=0, pady=10)
        blog_text.grid(row=5, column=1, pady=10)
        tags_label.grid(row=6, column=0)
        tags_entry.grid(row=6, column=1,sticky="e",padx=10)
        create_button.grid(row=8, column=1, pady=10,sticky="e",padx=50)

    def view_profile(frame, username, user):
        if user == "student":
            table = "student_profile"
        elif user == "institute":
            table = "institute_profile"
        else:
            table = "company_profile"

        def back():
            frame_view_profile.place_forget()

        frame_view_profile = Frame(center_frame, bg="#0572b5")
        button_back = Button(frame_view_profile, text="X", width=2, bg="red", command=lambda: back())
        inside_frame = Frame(frame_view_profile, bg="#b2e9f7")
        button_back.grid(row=0, column=0, sticky="e")
        inside_frame.grid(row=1, column=0, pady=10, padx=10)
        frame_view_profile.pack()
        frame_view_profile.place(x=200, y=50)

        try:
            sql = f"SELECT * FROM {table} where username = %s"
            val = [f"{username}"]
            edupedia_cursor.execute(sql, val)
            profile_values = edupedia_cursor.fetchall()

            label_Name = Label(inside_frame, text="Name ", bg="#b2e9f7", font=("Helvetica", "16"),width=18,anchor="nw")
            show_Name = Label(inside_frame, text=f":  {profile_values[0][1]}", bg="#b2e9f7", font=("Helvetica", "16"),width=25,anchor="nw")
            label_email = Label(inside_frame, text="email ", bg="#b2e9f7", font=("Helvetica", "16"),width=18,anchor="nw")
            show_email = Label(inside_frame, text=f":  {profile_values[0][3]}", bg="#b2e9f7", font=("Helvetica", "16"),width=25,anchor="nw")
            label_phone_number = Label(inside_frame, text="Phone number ", bg="#b2e9f7", font=("Helvetica", "16"),width=18,anchor="nw")
            show_phone_number = Label(inside_frame, text=f":  {profile_values[0][4]}", bg="#b2e9f7",
                                      font=("Helvetica", "16"),width=25,anchor="nw")
            label_address = Label(inside_frame, text="Address ", bg="#b2e9f7", font=("Helvetica", "16"),width=18,anchor="nw")
            show_address = Label(inside_frame, text=f":  {profile_values[0][5]}", bg="#b2e9f7", font=("Helvetica", "16"),width=25,anchor="nw")

            button_back = Button(inside_frame, text="back", height=2, width=15, bg="#b2e9f7",
                                 command=lambda: back())

            if user == "student":
                label_college = Label(inside_frame, text="College ", bg="#b2e9f7", font=("Helvetica", "16"),width=18,anchor="nw")
                show_college = Label(inside_frame, text=f":  {profile_values[0][6]}", bg="#b2e9f7",
                                     font=("Helvetica", "16"),width=25,anchor="nw")
                label_course = Label(inside_frame, text="Course ", bg="#b2e9f7", font=("Helvetica", "16"),width=18,anchor="nw")
                show_course = Label(inside_frame, text=f":  {profile_values[0][7]}", bg="#b2e9f7",
                                    font=("Helvetica", "16"),width=25,anchor="nw")
                label_interested_areas = Label(inside_frame, text="Interested areas ", bg="#b2e9f7",
                                               font=("Helvetica", "16"),width=18,anchor="nw")
                show_interested_areas = Label(inside_frame, text=f":  {profile_values[0][8]}", bg="#b2e9f7",
                                              font=("Helvetica", "16"),width=25,anchor="nw")

                label_college.grid(row=4, column=0,sticky="w",pady=10)
                show_college.grid(row=4, column=1,sticky="w",padx=10)
                label_course.grid(row=5, column=0,sticky="w",pady=10)
                show_course.grid(row=5, column=1,sticky="w",padx=10)
                label_interested_areas.grid(row=6, column=0,sticky="w",pady=10)
                show_interested_areas.grid(row=6, column=1,sticky="w",padx=10)

            elif user == "institute":
                label_courses_offered = Label(inside_frame, text="Courses Offered ", bg="#b2e9f7",
                                              font=("Helvetica", "16"),width=18,anchor="nw")
                show_courses_offered = Label(inside_frame, text=f":  {profile_values[0][6]}", bg="#b2e9f7",
                                             font=("Helvetica", "16"),width=25,anchor="nw")
                label_courses_offered.grid(row=4, column=0,sticky="w",pady=10)
                show_courses_offered.grid(row=4, column=1,sticky="w",padx=10)
            else:
                label_services_offered = Label(inside_frame, text="Services Providing ", bg="#b2e9f7",
                                               font=("Helvetica", "16"),width=18,anchor="nw")
                show_services_offered = Label(inside_frame, text=f":  {profile_values[0][6]}", bg="#b2e9f7",
                                              font=("Helvetica", "16"),width=25,anchor="nw")
                label_services_offered.grid(row=4, column=0,sticky="w",pady=10)
                show_services_offered.grid(row=4, column=1,sticky="w",padx=10)

            label_Name.grid(row=0, column=0,sticky="w",pady=10)
            show_Name.grid(row=0, column=1,sticky="w",padx=10)
            label_email.grid(row=1, column=0,sticky="w",pady=10)
            show_email.grid(row=1, column=1,sticky="w",padx=10)
            label_phone_number.grid(row=2, column=0,sticky="w",pady=10)
            show_phone_number.grid(row=2, column=1,sticky="w",padx=10)
            label_address.grid(row=3, column=0,sticky="w",pady=10)
            show_address.grid(row=3, column=1,sticky="w",padx=10)

        except Exception as error:
            messagebox.showerror("Error...!", f"{error}\nPlease contact the administrators")
            frame_view_profile.place_forget()

    def search_window():
        sercch_frame.place(x=150, y=100)

    def close(frame):
        frame.place_forget()

    def logout(frame):
        frame.pack_forget()
        into()

    # index
    def index():
        # index in profile
        index_frame = Frame(center_frame,bg="#0572b5")
        button_back =  Button(index_frame,text="X",width=2,bg="red",fg="white" ,font=("Helvetica", "12"),command=lambda:close(index_frame))
        inside_frame = Frame(index_frame, bg="#b2e9f7")
        button_back.grid(row=0, column=0, sticky="e")
        inside_frame.grid(row=1, column=0, pady=10, padx=10)

        def goto():
            def show():

                close(index_frame)

                show_frame = Frame(center_frame, bg="#0572b5")
                result_label = Label(show_frame, text="Results", fg="blue",font=("Helvetica", "16"))
                text_widget = Text(show_frame, width=70,height=15, bg='white', pady=20, padx=10,font=("Helvetica", "16"))
                scrollbar = Scrollbar(show_frame)
                text_widget.config(yscrollcommand=scrollbar.set)
                scrollbar.config(command=text_widget.yview)
                close_button = Button(show_frame, text="X", bg="red", fg="white", width=2,font=("Helvetica", "12"),
                                      command=lambda: close(show_frame))
                # result_label.grid(row=1, column=0, sticky='w', padx=10)
                close_button.grid(row=0, column=0, sticky='e')
                text_widget.grid(row=2, column=0, sticky='w',padx=10,pady=10)
                scrollbar.grid(row=2, column=0, sticky='e',pady=10)
                show_frame.place(x=50, y=35)

                try:
                    index_of_item = list_box_index.curselection()
                    # getting index results (row values)
                    sql_index_search_show = f"SELECT * FROM {selected_table_index} WHERE {selection} = %s"
                    value_index_search_show = [f"{list_box_index.get(index_of_item)}"]
                    edupedia_cursor.execute(sql_index_search_show, value_index_search_show)
                    result_index_search_show = edupedia_cursor.fetchall()
                    # getting colunm details for each row
                    sql_index_search_row = f"show columns from {selected_table_index}"
                    edupedia_cursor.execute(sql_index_search_row)
                    result_index_search_column_detail = edupedia_cursor.fetchall()
                    # getting colunm name for each row
                    columns_names = []
                    for column_name in result_index_search_column_detail:
                        columns_names.append(column_name[0])

                    # showing index result
                    for i in range(len(columns_names)):
                        fact = f"{columns_names[i].upper()} :\n \n {result_index_search_show[0][i]} \n\n\n"
                        text_widget.insert(END, fact)
                except Exception as e:
                    show_frame.place_forget()
                    index()
                    messagebox.showinfo("oops", "select at least one")

            def back(frame):
                frame.place_forget()
                index()

            try:
                index_of_item = list_box_index.curselection()
                if list_box_index.get(index_of_item) == "blogs":
                    selection = "blog_name"
                    selected_table_index = "blogs"
                elif list_box_index.get(index_of_item) == "books":
                    selection = "title"
                    selected_table_index = "books"
                elif list_box_index.get(index_of_item) == "colleges":
                    selection = "College_Name"
                    selected_table_index = "colleges"
                elif list_box_index.get(index_of_item) == "company_profile":
                    selection = "company_name"
                    selected_table_index = "company_profile"
                elif list_box_index.get(index_of_item) == "online_courses":
                    selection = "title"
                    selected_table_index = "online_courses"

                sql_index_search = f"select {selection} from {selected_table_index}"
                edupedia_cursor.execute(sql_index_search)
                result_tables = edupedia_cursor.fetchall()
                list_box_index.delete(0, END)
                for columns_value in result_tables:
                    list_box_index.insert(END, columns_value[0])

            except Exception as e:
                messagebox.showinfo("oops", "select at least one")
                index_frame.place_forget()
                index()

            back_button = Button(inside_frame, text="Back", fg="blue", bg="white",font=("Helvetica", "12"),
                                 command=lambda: back(index_frame))
            back_button.grid(row=2, column=0, sticky='e', padx=100)
            show_button = Button(inside_frame, text="Show ", bg='blue', fg='white',font=("Helvetica", "12"), command=lambda: show())
            goto_button.grid_forget()
            show_button.grid(row=2, column=0, pady=10, sticky='e', padx=20)

        def sort_reverse():
            data = list(list_box_index.get(0, END))

            def sort_true():
                list_box_index.delete(0, END)
                data.sort()
                for values in data:
                    list_box_index.insert(END, values)
                sort_button = Button(inside_frame, text="A-Z", bg="light green",fg="blue",font=("Helvetica", "8"), command=lambda: sort_reverse())
                sort_button.grid(row=0, column=0, pady=10, sticky='w',padx=10)

            list_box_index.delete(0, END)
            data.sort(reverse=True)
            for values in data:
                list_box_index.insert(END, values)
            sort_button = Button(inside_frame, text="Z-A",  bg="light green",fg="blue",font=("Helvetica", "8"), command=lambda: sort_true())
            sort_button.grid(row=0, column=0, pady=10, sticky='w',padx=10)

        index_frame.place(x=600,y=20)
        tables_index = ["blogs", "books", "colleges", "company_profile", "online_courses"]
        tables_index.sort()

        sort_button = Button(inside_frame, text="Z-A", bg="light green",fg="blue",font=("Helvetica", "8"), command=lambda: sort_reverse())
        list_box_index = Listbox(inside_frame, width=32, height=10,font=("Helvetica", "16"))
        scrollbar_index = Scrollbar(inside_frame)
        list_box_index.delete(0, END)
        for values in tables_index:
            list_box_index.insert(END, values)

        goto_button = Button(inside_frame, text="Go to", bg='blue', font=("Helvetica", "12"),fg='white', command=lambda: goto())

        sort_button.grid(row=0, column=0, pady=10, sticky='w',padx=10)
        list_box_index.grid(row=1, column=0, sticky='w', padx=10)
        scrollbar_index.grid(row=1, column=0, sticky='e')
        list_box_index.config(yscrollcommand=scrollbar_index.set)
        scrollbar_index.config(command=list_box_index.yview)
        goto_button.grid(row=2, column=0, pady=10, sticky='e', padx=40)

    # calculator

    def calculator(fra):

        base_frame = Frame(center_frame, width=340, height=530, bg="#0572b5")
        base_frame.place(x=600, y=10)
        frame = Frame(base_frame, width=320, height=480,bg="#b2e9f7")
        frame.place(x=10, y=40)

        # label

        lb = Label(frame, height=2, width=16, text='', bg='white', fg='black', anchor="se",
                   font=("Times", 24, "italic bold"))
        lb.place(x=11, y=10, )

        # number button click action  add

        opvalue = 0
        oldvalue = ''
        newvalue = ''
        eqe = ""

        dot_button_clicked = False

        def button1_clicked(value):
            global eqe
            eqe += value
            lb.config(text=eqe)

        def button2_clicked(value):
            global eqe
            eqe += value
            lb.config(text=eqe)

        def button3_clicked(value):
            global eqe
            eqe += value
            lb.config(text=eqe)

        def button4_clicked(value):
            global eqe
            eqe += value
            lb.config(text=eqe)

        def button5_clicked(value):
            global eqe
            eqe += value
            lb.config(text=eqe)

        def button6_clicked(value):
            global eqe
            eqe += value
            lb.config(text=eqe)

        def button7_clicked(value):
            global eqe
            eqe += value
            lb.config(text=eqe)

        def button8_clicked(value):
            global eqe
            eqe += value
            lb.config(text=eqe)

        def button9_clicked(value):
            global eqe
            eqe += value
            lb.config(text=eqe)

        def button0_clicked(value):
            global eqe
            eqe += value
            lb.config(text=eqe)

        def buttondot_clicked(value):
            global eqe
            eqe += value
            lb.config(text=eqe)

        # control button click action

        def buttonce_clicked():
            global eqe
            eqe = ''

            lb.config(text=eqe)

        def buttonc_clicked():
            global oldvalue
            global newvalue
            global opvalue
            global eqe

            oldvalue = ''
            newvalue = ''
            opvalue = 0
            eqe = ''
            lb.config(text=eqe)

        def buttonX_clicked():
            global eqe
            eqe = ''
            num = lb['text']
            cout = 1
            for i in num:
                if cout < len(num):
                    eqe += i
                    cout += 1

                else:
                    break
            lb.config(text=eqe)

        # operator button click action

        def add_but_clicked():
            global oldvalue
            global eqe
            global opvalue
            check = len(lb['text'])

            if check == 0:
                eqe = ''
                lb.config(text=eqe)
                opvalue = 0
            else:
                eqe = ''
                oldvalue = lb['text']
                lb.config(text=eqe)
                opvalue = 1

        def sub_but_clicked():
            global oldvalue
            global eqe
            global opvalue
            check = len(lb['text'])

            if check == 0:
                eqe = ''
                lb.config(text=eqe)
                opvalue = 0
            else:
                eqe = ''
                oldvalue = lb['text']
                lb.config(text=eqe)
                opvalue = 2

        def mult_but_clicked():
            global oldvalue
            global eqe
            global opvalue
            check = len(lb['text'])

            if check == 0:
                eqe = ''
                lb.config(text=eqe)
                opvalue = 0
            else:
                eqe = ''
                oldvalue = lb['text']
                lb.config(text=eqe)
                opvalue = 3

        def div_but_clicked():
            global oldvalue
            global opvalue
            global eqe
            check = len(lb['text'])

            if check == 0:
                eqe = ''
                lb.config(text=eqe)
                opvalue = 0
            else:
                eqe = ''
                oldvalue = lb['text']
                lb.config(text=eqe)
                opvalue = 4

        def equal_button_clicked():
            global opvalue
            global oldvalue
            global newvalue
            newvalue = lb['text']

            if opvalue == 1:

                resuil = float(oldvalue) + float(newvalue)
                resuil = str(resuil)
                lb.config(text=resuil)
                opvalue = 0


            elif opvalue == 2:
                resuil = float(oldvalue) - float(newvalue)
                resuil = str(resuil)
                lb.config(text=resuil)
                opvalue = 0

            elif opvalue == 3:
                resuil = float(oldvalue) * float(newvalue)
                resuil = str(resuil)
                lb.config(text=resuil)
                opvalue = 0

            elif opvalue == 4:
                resuil = float(oldvalue) / float(newvalue)
                resuil = str(resuil)
                lb.config(text=resuil)
                opvalue = 0
            else:
                initial = lb['text']
                lb.config(text=initial)

        # control buttons

        buttce = Button(frame, text='CE', bg='#fc475f', width=3, height=1, activebackground='red',
                        command=lambda: buttonce_clicked(), font=("Times", 25, "italic bold"))
        buttce.place(x=10, y=110)
        buttc = Button(frame, text='C', bg='#fc475f', width=3, height=1, activebackground='red',
                       command=lambda: buttonc_clicked(), font=("Times", 25, "italic bold"))
        buttc.place(x=80, y=110)
        buttx = Button(frame, text='X', bg='#fc475f', width=3, height=1, activebackground='red',
                       command=lambda: buttonX_clicked(), font=("Times", 25, "italic bold"))
        buttx.place(x=150, y=110)

        # number buttons

        butt7 = Button(frame, text='7', bg='gray', width=3, height=1, activebackground='#62bce3',
                       command=lambda: button7_clicked('7'), font=("Times", 25, "italic bold"))
        butt7.place(x=10, y=190)
        butt8 = Button(frame, text='8', bg='gray', width=3, height=1, activebackground='#62bce3',
                       command=lambda: button8_clicked('8'), font=("Times", 25, "italic bold"))
        butt8.place(x=80, y=190)
        butt9 = Button(frame, text='9', bg='gray', width=3, height=1, activebackground='#62bce3',
                       command=lambda: button9_clicked('9'), font=("Times", 25, "italic bold"))
        butt9.place(x=150, y=190)
        butt4 = Button(frame, text='4', bg='gray', width=3, height=1, activebackground='#62bce3',
                       command=lambda: button4_clicked('4'), font=("Times", 25, "italic bold"))
        butt4.place(x=10, y=260)
        butt5 = Button(frame, text='5', bg='gray', width=3, height=1, activebackground='#62bce3',
                       command=lambda: button5_clicked('5'), font=("Times", 25, "italic bold"))
        butt5.place(x=80, y=260)
        butt6 = Button(frame, text='6', bg='gray', width=3, height=1, activebackground='#62bce3',
                       command=lambda: button6_clicked('6'), font=("Times", 25, "italic bold"))
        butt6.place(x=150, y=260)
        butt1 = Button(frame, text='1', bg='gray', width=3, height=1, activebackground='#62bce3',
                       command=lambda: button1_clicked('1'), font=("Times", 25, "italic bold"))
        butt1.place(x=10, y=330)
        butt2 = Button(frame, text='2', bg='gray', width=3, height=1, activebackground='#62bce3',
                       command=lambda: button2_clicked('2'), font=("Times", 25, "italic bold"))
        butt2.place(x=80, y=330)
        butt3 = Button(frame, text='3', bg='gray', width=3, height=1, activebackground='#62bce3',
                       command=lambda: button3_clicked('3'), font=("Times", 25, "italic bold"))
        butt3.place(x=150, y=330)
        butt0 = Button(frame, text='0', bg='gray', width=3, height=1, activebackground='#62bce3',
                       command=lambda: button0_clicked('0'), font=("Times", 25, "italic bold"))
        butt0.place(x=10, y=400)
        butt_dot = Button(frame, text='.', bg='gray', width=3, height=1, activebackground='#62bce3',
                          command=lambda: buttondot_clicked('.'), font=("Times", 25, "italic bold"))
        butt_dot.place(x=80, y=400)

        # operator buttons

        butt_equal = Button(frame, text='=', bg='#5bf0a5', width=8, height=1, activebackground='white',
                            command=lambda: equal_button_clicked(), font=("Times", 25, "italic bold"))
        butt_equal.place(x=150, y=400)
        butt_div = Button(frame, text='/', bg='#695cab', width=4, height=1, activebackground='green',
                          command=lambda: div_but_clicked(), font=("Times", 24, "italic bold"))
        butt_div.place(x=227, y=110)
        butt_mult = Button(frame, text='*', bg='#695cab', width=4, height=1, activebackground='green',
                           command=lambda: mult_but_clicked(), font=("Times", 24, "italic bold"))
        butt_mult.place(x=227, y=190)
        butt_sub = Button(frame, text='-', bg='#695cab', width=4, height=1, activebackground='green',
                          command=lambda: sub_but_clicked(), font=("Times", 24, "italic bold"))
        butt_sub.place(x=227, y=260)
        butt_add = Button(frame, text='+', bg='#695cab', width=4, height=1, activebackground='green',
                          command=lambda: add_but_clicked(), font=("Times", 24, "italic bold"))
        butt_add.place(x=227, y=330)

        close_button = Button(base_frame, text="X", bg='red', fg="white",width=3, command=lambda: close(base_frame))
        close_button.place(x=310,y=0)

    # inside frame
    frame = Frame(label_main, width=1280, height=700,bg="#115e5d")
    frame.pack()
    top_frame = Frame(frame, width=1280, height=80, bg='#069c99')
    left_frame = Frame(frame, width=220, height=620, bg="#041924")
    top_icons = Frame(frame, width=1060, bg='#115e5d', height=40, padx=25)
    center_frame = Frame(frame, width=1060, height=580, bg="light blue")


    # top

    logo_canvas = Canvas(top_frame, height=60, width=60, )
    img_small_logo= Image.open("resources/small_logo.jpg")
    img_small_logo = ImageTk.PhotoImage(img_small_logo)
    logo_canvas.create_image(0, 0, image=img_small_logo, anchor='nw')

    button_logout = Button(top_frame, bg="blue",fg="white",text="log-out", font=("Comic Sans MS", 12, "bold"), width=6, height=1,
                           command=lambda: logout(frame))

    def show_favourite(frame, username):

        def go_favorite():
            index_of_favorite = list_box_favorie.curselection()
            favourite_search = list_box_favorie.get(index_of_favorite)
            frame_favorite.place_forget()
            seacrh_result(favourite_search, frame_favorite)

        frame_favorite = Frame(frame, height=200, width=800,bg="#0572b5")
        frame_favorite.place(x=350, y=200)
        button_back = Button(frame_favorite,text="X",width=2,bg="red",fg="white" ,font=("Helvetica", "12"),command=lambda: close(frame_favorite))
        inside_frame = Frame(frame_favorite, bg="#b2e9f7")
        button_back.grid(row=0, column=0, sticky="e")
        inside_frame.grid(row=1, column=0, pady=10, padx=10)
        list_box_favorie = Listbox(inside_frame, height=10, width=50,font=("Helvetica", "16"))
        scroll_bar_favorite = Scrollbar(inside_frame)
        go_button = Button(inside_frame, bg="blue",fg="white", text="Go",width=4,font=("Helvetica", "13"), command=lambda: go_favorite())

        sql_favourite = "SELECT favourite FROM favourite WHERE username = %s"
        value_favourite = [f"{username}"]
        edupedia_cursor.execute(sql_favourite, value_favourite)
        result_favourite = edupedia_cursor.fetchall()
        for favourite in result_favourite:
            list_box_favorie.insert(END, favourite)
        list_box_favorie.grid(row=1, column=0, sticky="w",padx=10,pady=10)
        scroll_bar_favorite.grid(row=1, column=0, sticky="e",padx=10,pady=10)
        go_button.grid(row=2, column=0, sticky="e", padx=20,pady=10)

    def show_history():

        def go_history():
            index_of_history = list_box_history.curselection()
            history_search = list_box_history.get(index_of_history)
            frame_history.place_forget()
            seacrh_result(history_search, frame_history)

        frame_history = Frame(frame, height=200, width=800,bg="#0572b5")
        frame_history.place(x=350, y=200)
        button_back =  Button(frame_history,text="X",width=2,bg="red",fg="white" ,font=("Helvetica", "12"),command=lambda: close(frame_history))
        inside_frame = Frame(frame_history, bg="#b2e9f7")
        button_back.grid(row=0, column=0, sticky="e")
        inside_frame.grid(row=1, column=0, pady=10, padx=10)
        list_box_history = Listbox(inside_frame, height=10, width=50,font=("Helvetica", "16"))
        scroll_bar_history = Scrollbar(inside_frame)
        go_button = Button(inside_frame, bg="blue",fg="white", text="Go",width=4,font=("Helvetica", "13"), command=lambda: go_history())

        sql_history = "SELECT history FROM history WHERE username = %s"
        value_history = [f"{username}"]
        edupedia_cursor.execute(sql_history, value_history)
        result_history = edupedia_cursor.fetchall()
        for history in result_history:
            list_box_history.insert(END, history)
        list_box_history.grid(row=1, column=0,sticky="w",padx=10,pady=10)
        scroll_bar_history.grid(row=1, column=0,sticky="e",padx=10,pady=10)
        go_button.grid(row=2, column=0, sticky="e",padx=20,pady=10)

    def contribute(frame,username,user):
        def submit_contribute_others(frame):
            messagebox.showinfo("Sorry","we are updating this")
            back()

        def submit_contribute_online_courses(frame):

            label_category.grid_forget()
            button_category1.grid_forget()
            button_category2.grid_forget()
            button_category3.grid_forget()
            button_category4.grid_forget()
            columns = ["title","category","description","level","duration","skills_covered","prerequisites","language","associated_with","instructors","price","rating","url"]
            for i in range(len(columns)):
                label_title = Label(inside_frame, text=f"{columns[i]}", bg="#b2e9f7", font=("Helvetica", "16"))
                entry_title = Entry(inside_frame, font=("Helvetica", "16"))
                label_title.grid(row=i, column=0, pady=1, sticky='w')
                entry_title.grid(row=i, column=1, sticky='e', padx=10)


            button_back = Button(inside_frame, text="back", height=1, width=5, bg="white",fg="blue", font=("Helvetica", "16"),
                                 command=lambda:back(),activeforeground="white",activebackground="blue")
            button_back.grid(row=len(columns) + 1, column=1,sticky='w', pady=10,padx=35)
            button_submit = Button(inside_frame, text="submit", height=1, width=6, bg="blue",fg="white", font=("Helvetica", "16"),
                                   activeforeground="blue",activebackground="white")
            button_submit.grid(row=len(columns) + 1, column=1, sticky='e', pady=20,padx=35)
        def submit_contribute_colleges(frame):

            label_category.grid_forget()
            button_category1.grid_forget()
            button_category2.grid_forget()
            button_category3.grid_forget()
            button_category4.grid_forget()
            columns = ["University_Name","College_Name","College_Type","State_Name","District_Name"]
            for i in range(len(columns)):
                label_title = Label(inside_frame, text=f"{columns[i]}", bg="#b2e9f7", font=("Helvetica", "16"))
                entry_title = Entry(inside_frame, font=("Helvetica", "16"))
                label_title.grid(row=i, column=0,pady=5,sticky='w')
                entry_title.grid(row=i, column=1,sticky='e',padx=10)


            button_back = Button(inside_frame, text="back", height=1, width=5, bg="white",fg="blue", font=("Helvetica", "16"),
                                 command=lambda:back(),activeforeground="white",activebackground="blue")
            button_back.grid(row=len(columns) + 1, column=1,sticky='w', pady=10,padx=35)
            button_submit = Button(inside_frame, text="submit", height=1, width=6, bg="blue",fg="white", font=("Helvetica", "16"),
                                   activeforeground="blue",activebackground="white")
            button_submit.grid(row=len(columns) + 1, column=1, sticky='e', pady=20,padx=35)
        def submit_contribute_books(frame):


            label_category.grid_forget()
            button_category1.grid_forget()
            button_category2.grid_forget()
            button_category3.grid_forget()
            button_category4.grid_forget()


            columns = ["author","image","description","download_link","pages","publisher","year","language","file"]
            for i in range(len(columns)):
                label_title = Label(inside_frame, text=f"{columns[i]}", bg="#b2e9f7", font=("Helvetica", "16"))
                entry_title = Entry(inside_frame, font=("Helvetica", "16"))
                label_title.grid(row=i, column=0,pady=5,sticky='w')
                entry_title.grid(row=i, column=1,sticky='e',padx=10)


            button_back = Button(inside_frame, text="back", height=1, width=5, bg="white",fg="blue", font=("Helvetica", "16"),
                                 command=lambda:back(),activeforeground="white",activebackground="blue")
            button_back.grid(row=len(columns) + 1, column=1,sticky='w', pady=10,padx=35)
            button_submit = Button(inside_frame, text="submit", height=1, width=6, bg="blue",fg="white", font=("Helvetica", "16"),
                                   activeforeground="blue",activebackground="white")
            button_submit.grid(row=len(columns) + 1, column=1, sticky='e', pady=20,padx=35)



        def back():
            frame_contribute_profile.place_forget
            frame_contribute_profile.place_forget()
            contribute(frame,username,user)

        def close(frame):
            frame.place_forget()


        frame_contribute_profile = Frame(center_frame,bg="#0572b5")
        button_back = Button(frame_contribute_profile, text="X", width=2, bg="red",fg="white", command=lambda: close(frame_contribute_profile))
        inside_frame = Frame(frame_contribute_profile, bg="#b2e9f7")
        button_back.grid(row=0, column=0, sticky="e")
        inside_frame.grid(row=1, column=0, pady=10, padx=10)
        frame_contribute_profile.place(x=50,y=20)

        label_category = Label(inside_frame, text="select a category ", bg="#b2e9f7",fg="blue", font=("Helvetica", "18"))
        label_category.grid(row=0, column=0,pady=20,sticky="w")

        button_category1= Button(inside_frame, text=f"books",bg="#0abaf5",font=("Helvetica", "18"), command=lambda: submit_contribute_books(inside_frame)
                                 ,activebackground="blue",activeforeground="white",width=15)
        button_category1.grid(row=1, column=0,sticky="w")
        button_category2 = Button(inside_frame, text=f"colleges",bg="#0abaf5", font=("Helvetica", "18"),width=15,
                                 command=lambda: submit_contribute_colleges(frame_contribute_profile),activebackground="blue",activeforeground="white")
        button_category2.grid(row=2, column=0,pady=10,sticky="w")
        button_category3= Button(inside_frame, text=f"online courses",bg="#0abaf5", font=("Helvetica", "18"),width=15,
                                 command=lambda: submit_contribute_online_courses(frame_contribute_profile),activebackground="blue",activeforeground="white")
        button_category3.grid(row=3, column=0,sticky="w")
        button_category4= Button(inside_frame, text=f"others",bg="#0abaf5", font=("Helvetica", "18"),width=15,
                                 command=lambda: submit_contribute_others(frame_contribute_profile),activebackground="blue",activeforeground="white")
        button_category4.grid(row=4, column=0,pady=10,sticky="w")



    def clubs():
        frame_clubs = Frame(center_frame,bg="#0572b5")
        button_back = Button(frame_clubs, text="X", width=2, bg="red",fg="white", command=lambda: close(frame_clubs))
        inside_frame = Frame(frame_clubs, bg="#b2e9f7")
        button_back.grid(row=0, column=0, sticky="e")
        inside_frame.grid(row=1, column=0, pady=10, padx=10)
        frame_clubs.place(x=150, y=50)
        frame_clubs_manage = Frame(inside_frame,bg="#b2e9f7")
        frame_clubs_detail = Frame(inside_frame,bg="#b2e9f7")
        frame_clubs_notice = Frame(inside_frame,bg="#b2e9f7")

        def manage_clubs():
            frame_clubs_manage.grid(row=1,column=0)
            frame_clubs_detail.grid_forget()
            frame_clubs_notice.grid_forget()

            button_IEEE = Button(frame_clubs_manage, text=f"IEEE", bg="#0abaf5", font=("Helvetica", "14"),width=15)
            button_IEEE.grid(row=1, column=0,pady=10,sticky="w")
            button_ISTE = Button(frame_clubs_manage, text=f"ISTE", bg="#0abaf5", font=("Helvetica", "14"),width=15)
            button_ISTE.grid(row=2, column=0,pady=10,sticky="w")
            button_NSS = Button(frame_clubs_manage, text=f"NSS", bg="#0abaf5", font=("Helvetica", "14"),width=15)
            button_NSS.grid(row=3, column=0,pady=10,sticky="w")
            button_others = Button(frame_clubs_manage, text=f"others", bg="#0abaf5", font=("Helvetica", "14"),width=15)
            button_others.grid(row=4, column=0,pady=10,sticky="w")

        def show_details():
            frame_clubs_detail.grid(row=1,column=1)
            button_cordinators = Button(frame_clubs_detail, text=f"co-ordinators", bg="#0abaf5",
                                        font=("Helvetica", "14"),width=15)
            button_cordinators.grid(row=1, column=1,pady=10,sticky="w")
            button_secretaries = Button(frame_clubs_detail, text=f"secretaries", bg="#0abaf5", font=("Helvetica", "14"),width=15)
            button_secretaries.grid(row=2, column=1,pady=10,sticky="w")
            button_volunteers = Button(frame_clubs_detail, text=f"volunteers", bg="#0abaf5", font=("Helvetica", "14"),width=15)
            button_volunteers.grid(row=4, column=1,pady=10,sticky="w")
            button_others = Button(frame_clubs_detail, text=f"others", bg="#0abaf5", font=("Helvetica", "14"),width=15)
            button_others.grid(row=5, column=1,pady=10,sticky="w")
        def notices():
            frame_clubs_notice.grid(row=1,column=2)

            button_events = Button(frame_clubs_notice, text=f"events", bg="#0abaf5", font=("Helvetica", "14"),width=18)
            button_events.grid(row=1, column=1,pady=10,sticky="w")
            button_circular = Button(frame_clubs_notice, text=f"circular", bg="#0abaf5", font=("Helvetica", "14"),width=18)
            button_circular.grid(row=2, column=1,pady=10,sticky="w")
            button_permission = Button(frame_clubs_notice, text=f"permission request", bg="#0abaf5",
                                       font=("Helvetica", "14"),width=18)
            button_permission.grid(row=3, column=1,pady=10,sticky="w")
            button_others = Button(frame_clubs_notice, text=f"others", bg="#0abaf5", font=("Helvetica", "14"),width=18)
            button_others.grid(row=4, column=1,pady=10,sticky="w")


        label_manage_clubs = Button(inside_frame, font=("Helvetica", "14"), text="Manage clubs", bg="#07f3f7", width=18,
                                 command=lambda: manage_clubs())
        label_show_details = Button(inside_frame, font=("Helvetica", "14"), text="details", bg="#07f3f7", width=18,
                                    command=lambda: show_details())
        label_assign_works = Button(inside_frame, font=("Helvetica", "14"), text="notices", bg="#07f3f7", width=20,
                                     command=lambda: notices())

        label_manage_clubs.grid(row=0, column=0)
        label_show_details.grid(row=0, column=1)
        label_assign_works.grid(row=0, column=2)

    def advertise():
        frame_ad = Frame(center_frame,bg="#0572b5")

        button_back = Button(frame_ad, text="X", width=2, bg="red",fg="white", command=lambda: close(frame_ad))
        inside_frame = Frame(frame_ad, bg="#b2e9f7")
        button_back.grid(row=0, column=0, sticky="e")
        inside_frame.grid(row=1, column=0, pady=10, padx=10)

        frame_ad.place(x=100, y=50)
        frame_track_ad = Frame(inside_frame,bg="#b2e9f7")
        frame_your_ad = Frame(inside_frame,bg="#b2e9f7")
        frame_contact_us = Frame(inside_frame,bg="#b2e9f7")

        def track_ADVT():

            frame_track_ad.grid(row=1,column=0)
            frame_your_ad.grid_forget()
            frame_contact_us.grid_forget()

            button_IEEE = Button(frame_track_ad, text=f"See Progress", bg="#0abaf5", font=("Helvetica", "14"),width=15)
            button_IEEE.grid(row=3, column=1,pady=10,sticky="w")
            button_ISTE = Button(frame_track_ad, text=f"Save Report", bg="#0abaf5", font=("Helvetica", "14"),width=15)
            button_ISTE.grid(row=5, column=1,pady=10,sticky="w")
            button_NSS = Button(frame_track_ad, text=f"Advt. tools", bg="#0abaf5", font=("Helvetica", "14"),width=15)
            button_NSS.grid(row=7, column=1,pady=10,sticky="w")
            button_others = Button(frame_track_ad, text=f"others", bg="#0abaf5", font=("Helvetica", "14"),width=15)
            button_others.grid(row=9, column=1,pady=10,sticky="w")

        def Your_Ads():


            frame_your_ad.grid(row=1,column=1)

            button_cordinators = Button(frame_your_ad, text=f"Create New", bg="#0abaf5",
                                        font=("Helvetica", "14"),width=15)
            button_cordinators.grid(row=1, column=1,pady=10,sticky="w")
            button_secretaries = Button(frame_your_ad, text=f"Update Ads", bg="#0abaf5", font=("Helvetica", "14"),width=15)
            button_secretaries.grid(row=2, column=1,pady=10,sticky="w")
            button_volunteers = Button(frame_your_ad, text=f"Ads Services", bg="#0abaf5", font=("Helvetica", "14"),width=15)
            button_volunteers.grid(row=3, column=1,pady=10,sticky="w")
            button_others = Button(frame_your_ad, text=f"others", bg="#0abaf5", font=("Helvetica", "14"),width=15)
            button_others.grid(row=4, column=1,pady=10,sticky="w")

        def contact_us():


            frame_contact_us.grid(row=1,column=2)

            button_events = Button(frame_contact_us, text=f"Premium Services", bg="#0abaf5", font=("Helvetica", "14"),width=15)
            button_events.grid(row=3, column=1,pady=10,sticky="w")
            button_circular = Button(frame_contact_us, text=f"Report a problem", bg="#0abaf5", font=("Helvetica", "14"),width=15)
            button_circular.grid(row=5, column=1,pady=10,sticky="w")
            button_permission = Button(frame_contact_us, text=f"Help Needed", bg="#0abaf5",
                                       font=("Helvetica", "14"),width=15)
            button_permission.grid(row=7, column=1,pady=10,sticky="w")
            button_others = Button(frame_contact_us, text=f"others", bg="#0abaf5", font=("Helvetica", "14"),width=15)
            button_others.grid(row=9, column=1,pady=10,sticky="w")

        label_track_ad = Button(inside_frame, font=("Helvetica", "14"), text="track ADVT",bg="#07f3f7", width=22,
                                     command=lambda: track_ADVT())
        label_your_ad = Button(inside_frame, font=("Helvetica", "14"), text="Your Ads",bg="#07f3f7",width=22,
                                     command=lambda: Your_Ads())
        label_contat_us = Button(inside_frame, font=("Helvetica", "14"), text="contact us",bg="#07f3f7", width=22,
                                    command=lambda: contact_us())

        label_track_ad.grid(row=0, column=0)
        label_your_ad.grid(row=0, column=1)
        label_contat_us.grid(row=0, column=2)


    # left
    profile_text_label = Label(left_frame, font=("Helvetica", "16"), text="My profile", bg="#041924", width=18,fg="white",
                               anchor="sw",height=2)
    profile_img = Image.open("resources/profile.jpg")
    profile_img = ImageTk.PhotoImage(profile_img)
    profile_canvas = Canvas(left_frame, height=180, width=220)
    profile_canvas.create_image(0, 0, image=profile_img, anchor='nw')
    profile_name_label = Label(left_frame, font=("Helvetica", "16"), text=f"{username}", bg="#041924", width=18,fg="white",
                               anchor='nw')
    view_profile_butt = Button(left_frame, text="view profile", font=("Helvetica", "16"), width=18, height=2,
                               bg="#05b3b0", command=lambda: view_profile(frame, username, user))
    update_profile_butt = Button(left_frame, text="update profile", font=("Helvetica", "16"), width=18, height=2,
                                 bg="#0f5c5b", command=lambda: update_profile(frame, username, user),fg="#aaedf0")
    contirubte_butt = Button(left_frame, text="Contiribute", font=("Helvetica", "16"), bg="#05b3b0", width=18, height=2,
                             command=lambda: contribute(frame,username,user))
    history_butt = Button(left_frame, text="History", font=("Helvetica", "16"), bg="#05b3b0", width=18, height=2, command= lambda : show_history())

    if user == "student":
        favorite_butt = Button(left_frame, text="favorites",fg="#aaedf0", font=("Helvetica", "16"), bg="#0f5c5b", width=18, height=2,command=lambda: show_favourite(frame, username))
        favorite_butt.grid(row=6, column=0)
        contirubte_butt.grid(row=7, column=0)


    elif user == 'institute':
        club_butt = Button(left_frame, text="Clubs", fg="#aaedf0",font=("Helvetica", "16"), bg="#0f5c5b", width=18, height=2, command= lambda : clubs())
        club_butt.grid(row=7, column=0)
        contirubte_butt.grid(row=8, column=0)


    else:
        advertise_butt = Button(left_frame, text="Advertise",fg="#aaedf0", font=("Helvetica", "16"), bg="#0f5c5b", width=18, height=2 ,command= lambda : advertise())
        advertise_butt.grid(row=7, column=0)

    def blog_feed(user):

        frame_blog = Frame(center_frame, height=400, width=600, bg="#0572b5")

        close_button = Button(frame_blog, text="X", bg="red", fg="white", width=2,
                              command=lambda: close(frame_blog),font=("Helvetica", "10"),)
        inside_frame = Frame(frame_blog, bg="#b2e9f7")
        close_button.grid(row=0, column=0, sticky="e")
        inside_frame.grid(row=1, column=0, pady=10, padx=10)

        frame_blog.place(x=50, y=20)

        button_border =Frame(inside_frame, highlightbackground="blue",
                                 highlightthickness=2)
        button_border.grid(row=1, column=0, sticky="w", padx=10,pady=10)

        like_button = Button(button_border, bg="white",fg="blue", text="Like",font=("Helvetica", "10"),width=4)
        like_button.pack()

        button_border =Frame(inside_frame, highlightbackground="green",
                                 highlightthickness=2, bd=0)
        button_border.grid(row=1, column=0, sticky="e", padx=30)
        share_button = Button(button_border, bg="white",fg="green" ,text="share",font=("Helvetica", "10"),width=5)
        share_button.pack()

        button_border =Frame(inside_frame, highlightbackground="red",
                                 highlightthickness=2)
        button_border.grid(row=1, column=0, sticky="w", padx=70)
        favorite_button = Button(button_border, bg="white",fg="red", text="fav",font=("Helvetica", "10"),width=4)
        favorite_button.pack()


        text_widget = Text(inside_frame, width=80, height=16, bg='white', pady=20, padx=10, font=("Helvetica", "14"))
        scrollbar = Scrollbar(inside_frame)
        text_widget.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=text_widget.yview)
        text_widget.grid(row=0, column=0, sticky='w',pady=5,padx=5)
        scrollbar.grid(row=0, column=0, sticky='e',pady=5,padx=5)


        result_blog_columns = ["author_name","category","blog_name","blog"]
        sql_blog_feed = f"SELECT * FROM blogs ORDER BY rating DESC LIMIT 50"
        edupedia_cursor.execute(sql_blog_feed)
        result_blog_feed = edupedia_cursor.fetchall()
        result_blog_feed_value = []

        for blogs in result_blog_feed:
            blog = []
            for blogs_row in blogs:
                blog.append(blogs_row)
            blog = blog[2:6]
            result_blog_feed_value.append(blog)

        for i in range(len(result_blog_feed_value)):
            text_widget.insert(END, f"BLOG.{i+1}\n")
            text_widget.insert(END, f"="*len(f"BLOG.{i+1}"))
            for j in range(len(result_blog_columns)):
                text_widget.insert(END, f"\n{result_blog_columns[j]} :")
                text_widget.insert(END, f"    {result_blog_feed_value[i][j]}")
            text_widget.insert(END, "\n\n")



    def analyse(frame):

        frame_analyse = Frame(center_frame,bg="#0572b5")
        button_back = Button(frame_analyse,text="X",width=2,bg="red",fg="white" ,font=("Helvetica", "12"),command=lambda: close(frame_analyse))
        inside_frame = Frame(frame_analyse, bg="#b2e9f7")
        button_back.grid(row=0, column=0, sticky="e")
        inside_frame.grid(row=1, column=0, pady=10, padx=10)
        frame_analyse.place(x=100,y=30)

        def plot(x,y):
            frame_analyse_graph = Frame(inside_frame, width=800, height=150)
            frame_analyse_graph.grid(row=1,column=0,pady=10)
            fig = Figure(figsize=(7,4),dpi=100)
            graph = fig.add_subplot(111)
            draw = graph.bar(x,y,.3)
            canvas = FigureCanvasTkAgg(fig,master=frame_analyse_graph)
            canvas.draw()
            canvas.get_tk_widget().pack()

        def trending():
            sql_blog_likes = f"SELECT blog_name,likes FROM blogs ORDER BY blog_name LIMIT 10;"
            edupedia_cursor.execute(sql_blog_likes)
            likes = edupedia_cursor.fetchall()
            x_axis = []
            y_axis = []
            for i in range(len(likes)):
                x_axis.append(likes[i][0])
                y_axis.append(int(likes[i][1]))

            plot(x_axis,y_axis)

        def ADVT():
            sql_blog_likes = f"SELECT ADVT_name,rating FROM advertisement ORDER BY ADVT_name LIMIT 10;"
            edupedia_cursor.execute(sql_blog_likes)
            likes = edupedia_cursor.fetchall()
            x_axis = []
            y_axis = []
            for i in range(len(likes)):
                x_axis.append(likes[i][0])
                y_axis.append(float(likes[i][1]))

            plot(x_axis,y_axis)

        def reactions():
            sql_blog_likes = f"SELECT post_name,likes FROM reactions ORDER BY post_name LIMIT 10;"
            edupedia_cursor.execute(sql_blog_likes)
            likes = edupedia_cursor.fetchall()
            x_axis = []
            y_axis = []
            for i in range(len(likes)):
                x_axis.append(likes[i][0])
                y_axis.append(int(likes[i][1]))

            plot(x_axis,y_axis)

        label_tredning = Button(inside_frame, font=("Helvetica", "16"), text="Trending", bg="#07f3f7", width=20,
                               anchor='nw', command= lambda : trending())
        label_ADVT = Button(inside_frame, font=("Helvetica", "16"), text="ADVT.", bg="#07f3f7", width=20,
                               anchor='nw', command= lambda : ADVT())
        label_reactions_to_post = Button(inside_frame, font=("Helvetica", "16"), text="Reactions", bg="#07f3f7", width=20,
                               anchor='nw', command= lambda : reactions())
        label_tredning.grid(row=0 ,column=0,sticky="w",pady=10,padx=10)
        label_ADVT.grid(row=0, column=0,padx=260)
        label_reactions_to_post.grid(row=0, column=0,sticky="e",padx=10)


    # top_icons
    search_button = Button(top_icons, text="search", bg='#22e2f0', foreground='blue',font=("Helvetica", "14"), width=13,
                           command=lambda: search_window())
    vlog_button = Button(top_icons, text="blogs",  bg='#091836', foreground='#22e2f0', font=("Helvetica", "14"), height=1,
                         width=13, command=lambda: blog_feed(user))
    create_vlog_button = Button(top_icons, text="create blogs", bg='#22e2f0', foreground='blue', font=("Helvetica", "14"),
                                height=1, width=13, command=lambda: create_blog(frame, username, user))
    index_button = Button(top_icons, text="index",bg='#091836', foreground='#22e2f0', font=("Helvetica", "14"), height=1,
                          width=13, command=lambda: index())

    if user == 'student' or user == "institute":
        calc_button = Button(top_icons, text="Calc", bg='#22e2f0', foreground='blue', font=("Helvetica", "14"),
                             height=1, width=13, command=lambda: calculator(frame))
        calc_button.grid(row=0, column=5, padx=25)

    else:
        analyse_button = Button(top_icons, text="Analyse", bg='#22e2f0', foreground='blue', font=("Helvetica", "14"),
                                height=1, width=13, command= lambda : analyse(frame))
        analyse_button.grid(row=0, column=5, padx=25)

    # top frame
    top_frame.place(x=0, y=0)
    left_frame.place(x=0, y=88)
    logo_canvas.place(x=10, y=10)

    button_logout.place(x=1150, y=20)
    top_icons.place(x=225, y=80)
    center_frame.place(x=225, y=120)

    # left frame
    profile_text_label.grid(row=0, column=0)
    profile_canvas.grid(row=1, column=0)
    profile_name_label.grid(row=2, column=0,pady=3)
    view_profile_butt.grid(row=3, column=0,)
    update_profile_butt.grid(row=4, column=0)
    history_butt.grid(row=5, column=0)

    # top icons
    search_button.grid(row=0, column=1, padx=25)
    vlog_button.grid(row=0, column=2, padx=25)
    create_vlog_button.grid(row=0, column=3, padx=20)
    index_button.grid(row=0, column=4, padx=25)

    def seacrh_result(search_Entry,frame):
        # search result frame

        def go_search(count_index_table):
            scroll_bar_search.grid_forget()
            list_box_search.grid_forget()
            button_back.grid_forget()
            go_button.grid_forget()




            index_of_search = list_box_search.curselection()
            index_of_table = 0
            if index_of_search[0] > count_index_table[-1]:
                index_of_table = count_index_table[-1]
            else:
                for i in range(len(count_index_table)):
                    if count_index_table[i] > index_of_search[0]:
                        index_of_table = count_index_table[i-1]
                        break

            column_name = list_box_search.get(index_of_search)[5:]
            table_name = list_box_search.get(index_of_table)

            text_widget = Text(inside_frame, width=70, height=15, bg='white', pady=20, padx=10, font=("Helvetica", "14"))
            scrollbar = Scrollbar(inside_frame)
            text_widget.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=text_widget.yview)

            text_widget.grid(row=1, column=0, sticky='w',padx=10,pady=10)
            scrollbar.grid(row=1, column=0, sticky='e',padx=10,pady=10)

            if table_name == "blogs":
                selection = "blog_name"
            elif table_name == "books":
                selection = "title"
            elif table_name == "colleges":
                selection = "College_Name"
            elif table_name == "company_profile":
                selection = "company_name"
            elif table_name == "online_courses":
                selection = "title"

            sql_search_goto = f"SELECT * FROM {table_name} WHERE {selection} = %s"
            value_search_goto = [column_name]
            edupedia_cursor.execute(sql_search_goto, value_search_goto)
            result_seacrh_goto = edupedia_cursor.fetchall()
            sql_search_row = f"show columns from {table_name}"
            edupedia_cursor.execute(sql_search_row)
            result_search_column_detail = edupedia_cursor.fetchall()
            # getting colunm name for each row
            columns_names = []
            for column_name in result_search_column_detail:
                columns_names.append(column_name[0])

            # showing search result
            for i in range(len(columns_names)):
                fact = f"{columns_names[i].upper()} :\n \n {result_seacrh_goto[0][i]} \n\n\n"
                text_widget.insert(END, fact)

            def back(frame):
                frame.pack_forget()
                search_window(search_Entry,frame)

            back_button = Button(frame_search, text="Close", fg="green", bg="yellow",
                                 command=lambda: close(frame_search))
            #show_button = Button(frame_search, text="Show ", bg='blue', fg='white', command=lambda: show())
            #show_button.grid(row=2, column=0, pady=10, sticky='e', padx=10)



        frame_search = Frame(center_frame, height=400, width=850, bg="#0572b5")
        inside_frame = Frame(frame_search, bg="#b2e9f7", width=600, height=300)
        button_back = Button(inside_frame, text="Back", width=4, bg="white", fg="blue", font=("Helvetica", "12"),
                             command=lambda: close(frame_search))
        inside_frame.grid(row=1, column=0, pady=10, padx=10)
        button_back.grid(row=2, column=0, sticky="e",padx=80,pady=10)



        frame_search.place(x=100, y=40)
        list_box_search = Listbox(inside_frame, height=18, width=90,font=("Helvetica", "12"))
        scroll_bar_search = Scrollbar(inside_frame)
        list_box_search.delete(0, END)
        close_button = Button(frame_search,text="X",width=2,bg="red",fg="white" ,font=("Helvetica", "12"),command=lambda: close(frame_search))
        go_button = Button(inside_frame, bg="blue",fg="white",width=4, text="Go",font=("Helvetica", "12"), command=lambda: go_search(count_index_table))


        close_button.grid(row=0, column=0, sticky="e", padx=10)
        list_box_search.grid(row=1, column=0, sticky="w",padx=10,pady=10)
        scroll_bar_search.grid(row=1, column=0, sticky="e",padx=10,pady=10)
        go_button.grid(row=2, column=0, sticky="e", padx=20,pady=10)


        search_tables = ["blogs", "books", "colleges", "company_profile", "online_courses"]
        count_index_table = []
        count = -2
        for table in search_tables:
            if table == "blogs":
                selection = "blog_name"
            elif table == "books":
                selection = "title"
            elif table == "colleges":
                selection = "College_Name"
            elif table == "company_profile":
                selection = "company_name"
            elif table == "online_courses":
                selection = "title"

            list_box_search.insert(END, f"{table}")
            list_box_search.insert(END,"="*len(table))
            sql_search = f"select {selection} from {table} where {selection} like %s"
            val_search = [f"%{search_Entry}%"]
            edupedia_cursor.execute(sql_search, val_search)
            result_tables = edupedia_cursor.fetchall()
            count+=2
            count_index_table.append(count)
            for i in range(len(result_tables)):
                list_box_search.insert(END, f"     {result_tables[i][0]}")
                count+=1
            list_box_search.insert(END, "")
            count+=1


    # seacrh frame
    sercch_frame = Frame(center_frame,bg="#0572b5", width=700, height=300)
    button_back = Button(sercch_frame, text="X", width=2, bg="red", fg="white", font=("Helvetica", "12"),
                         command=lambda: close(sercch_frame))
    inside_frame = Frame(sercch_frame, bg="#b2e9f7",width=600,height=300)
    button_back.grid(row=0, column=0, sticky="e")
    inside_frame.grid(row=1, column=0, pady=10, padx=10)
    search_img = Image.open("resources/search.png")
    search_img = ImageTk.PhotoImage(search_img)
    search_button = Button(sercch_frame, image=search_img, font=("Comic Sans MS", 15, "bold"), anchor='nw', border=0,
                           command=lambda: seacrh_result(search_Entry.get(),frame))
    search_Entry = Entry(sercch_frame, font=("Comic Sans MS", 14), width=40)
    search_Entry_value = search_Entry.get()
    close_img = Image.open("resources/close.png")
    close_img = ImageTk.PhotoImage(close_img)
    close_button = Button(sercch_frame, image=close_img, borderwidth=0, command=lambda: close(sercch_frame))

    search_button.place(x=540, y=150)
    search_Entry.place(x=50, y=150)
    # close_button.place(x=670, y=0)
    window.mainloop()


def create_uesr(frame, user,button_stud,button_inst,button_comp):
    frame.place_forget()
    def creating_account(entry_usr, entry_pwd, entry_conpwd, entry_mob, entry_email, entry_belongs_to):
        account_details = [entry_usr, entry_pwd, entry_mob, entry_email, entry_belongs_to]
        # checking if the passwords are same
        if entry_pwd.get() != entry_conpwd.get():
            messagebox.showerror("Oops...!", "Passwords are mismatching")
        else:

            if user == "student":
                table_profile = "student_profile"
                table_login = "student_login"
                column_belongs_to = "college"
            elif user == "institute":
                table_profile = "institute_profile"
                table_login = "institute_login"
                column_belongs_to = "institute_name"
            else:
                table_profile = "company_profile"
                table_login = "company_login"
                column_belongs_to = "company_name"

            # checking if the username exists
            sql_user_names = f"SELECT * FROM {table_login} WHERE user_name = %s"
            values_user_names = (entry_usr.get(),)
            edupedia_cursor.execute(sql_user_names, values_user_names)
            result = edupedia_cursor.fetchall()
            if result:
                messagebox.showerror("Oops",
                                     "username already exists\nTry another one or Log in to your account with this username")
            else:
                # creating mew user with details provided
                try:
                    sql_profile = f"INSERT INTO {table_profile} (username,email,phone_number,{column_belongs_to}) VALUES (%s,%s,%s,%s)"
                    values_profile = (entry_usr.get(), entry_email.get(), entry_mob.get(), entry_belongs_to.get())
                    sql_login_details = f"INSERT INTO {table_login} (user_name,password) VALUES (%s,%s)"
                    value_login_details = (entry_usr.get(), entry_pwd.get())
                    edupedia_cursor.execute(sql_profile, values_profile)
                    edupedia_cursor.execute(sql_login_details, value_login_details)
                    messagebox.showinfo("Success",
                                        "Account created\nLogin and go to update profile to complete your account details")
                    edupedia.commit()
                    frame_create_usr.place_forget()
                    login(frame_comp_log, user, button_stud, button_inst, button_comp)

                except Exception as error:
                    messagebox.showerror("Error...!", f"{error}\nPlease contact the administrators")

    def close(frame,button_stud,button_inst,button_comp):
        frame_create_usr.place_forget()
        login(frame, user,button_stud,button_inst,button_comp)

    frame.pack_forget()
    frame_create_usr = Frame(label_main,bg="#0572b5" )

    close_button = Button(frame_create_usr, text="X", bg="red", fg="white", width=3, command=lambda: close(frame,button_stud,button_inst,button_comp))
    inside_frame = Frame(frame_create_usr, bg="#b2e9f7")
    close_button.grid(row=0, column=0, sticky="e")
    inside_frame.grid(row=1, column=0, pady=10, padx=10)


    label_usr = Label(inside_frame, text="Enter Username ", bg="#b2e9f7", font=("Helvetica", "16"), width=16,
                      anchor='nw')
    entry_usr = Entry(inside_frame, font=("Helvetica", "16"))
    label_pwd = Label(inside_frame, text="Enter Password ", bg='#b2e9f7', font=("Helvetica", "16"), width=16,
                      anchor='nw')
    v = IntVar(value=0)
    check_pwd = Checkbutton(inside_frame, text="show password", variable=v, onvalue=1, offvalue=0,
                            command=lambda: showpsd(v, entry_pwd))
    entry_pwd = Entry(inside_frame, show="*", font=("Helvetica", "16"))
    label_conpwd = Label(inside_frame, text="Conform Password ", bg='#b2e9f7', font=("Helvetica", "16"), width=16,
                         anchor='nw')
    entry_conpwd = Entry(inside_frame, show="*", font=("Helvetica", "16"))
    label_mob = Label(inside_frame, text="Enter Mobile no ", bg="#b2e9f7", font=("Helvetica", "16"), width=16,
                      anchor='nw')
    entry_mob = Entry(inside_frame, font=("Helvetica", "16"))
    label_email = Label(inside_frame, text="Enter Email id", bg="#b2e9f7", font=("Helvetica", "16"), width=16,
                        anchor='nw')
    entry_email = Entry(inside_frame, font=("Helvetica", "16"))
    entry_belongs_to = Entry(inside_frame, font=("Helvetica", "16"))
    entry_belongs_to.grid(row=6, column=1)

    if user == "student":
        label_collge = Label(inside_frame, text="Enter Collage name ", bg="#b2e9f7", font=("Helvetica", "16"),
                             width=16, anchor='nw')
        label_collge.grid(row=6, column=0, pady=10)

    elif user == "institute":
        label_institue = Label(inside_frame, text="Enter institute name", bg="#b2e9f7", font=("Helvetica", "16"),
                               width=16, anchor='nw')
        label_institue.grid(row=6, column=0, pady=10)
    else:
        label_company = Label(inside_frame, text="Enter company name", bg="#b2e9f7", font=("Helvetica", "16"),
                              width=16, anchor='nw')
        label_company.grid(row=6, column=0, pady=10)

    submit_button = Button(inside_frame, text="submit", bg="blue", fg="white", font=("Helvetica", "16"),
                           command=lambda: creating_account(entry_usr, entry_pwd, entry_conpwd, entry_mob, entry_email,
                                                            entry_belongs_to))

    frame_create_usr.place(x=350, y=100)
    label_usr.grid(row=1, column=0, pady=10, padx=10)
    entry_usr.grid(row=1, column=1, padx=5)
    label_pwd.grid(row=2, column=0, pady=10)
    entry_pwd.grid(row=2, column=1)
    check_pwd.grid(row=2, column=2, padx=10)
    label_conpwd.grid(row=3, column=0, pady=10)
    entry_conpwd.grid(row=3, column=1)
    label_mob.grid(row=4, column=0, pady=10)
    entry_mob.grid(row=4, column=1)
    label_email.grid(row=5, column=0, pady=10)
    entry_email.grid(row=5, column=1)
    submit_button.grid(row=7, column=1, pady=10)


# mian frame categories
# frame_login = Frame(window, width=600, height=300, bg="white")
# frame_login.place(x=350, y=200)

img = Image.open("resources/main.jpg")
img = ImageTk.PhotoImage(img)
label_main=Label(window,image=img)
label_main.pack()

logo_img = Image.open("resources/main_logo.jpg")
logo_img = ImageTk.PhotoImage(logo_img)
logo_label=Label(label_main,image=logo_img)
logo_label.place(x=580,y=80)

def into(w=None,e=None):


    if w!=None and e!=None:
        w.place_forget()
        e.place_forget()
    # else:
    #     img = Image.open("resources/4220050.jpg")
    #     img = ImageTk.PhotoImage(img)
    #     label_main = Label(window, image=img)
    #     label_main.pack()

    logo_img1 = Image.open("resources/main_logo.jpg")
    logo_img1 = ImageTk.PhotoImage(logo_img1)
    logo_label1 = Label(label_main, image=logo_img1)
    logo_label1.place(x=580, y=80)

    s, i, c = "student", "institute", "company"

    # category button
    button_stud = Button(label_main, text="Student login", bg="blue", fg='white', activebackground="green",
                         font=("Comic Sans MS", 15, "bold"), width=18, command=lambda: student(s,button_stud,button_inst,button_comp,logo_label1))
    button_inst = Button(label_main, text="Institute login", bg="blue", fg='white', activebackground="green",
                         font=("Comic Sans MS", 15, "bold"), width=18, command=lambda: institute(i,button_stud,button_inst,button_comp,logo_label1))
    button_comp = Button(label_main, text="Company login", bg="blue", fg='white', activebackground="green",
                         font=("Comic Sans MS", 15, "bold"), width=18, command=lambda: company(c,button_stud,button_inst,button_comp,logo_label1))

    button_stud.place(x=540, y=300)
    button_inst.place(x=540, y=375)
    button_comp.place(x=540, y=450)
    window.mainloop()




welcome_label=Label(label_main,text="Welcome to",font=("Comic Sans MS", 13, "bold"))
edupidia_button=Button(label_main,text="Edupedia",fg="#042866",width=10,font=("Comic Sans MS", 25, "bold"),activebackground="#d3f4f5",activeforeground="#0f9496",command=lambda :into(welcome_label,edupidia_button,))
# welcome_label.place(x=620,y=250)
edupidia_button.place(x=550,y=250)


frame_stud_log = Frame(label_main, bg="#0572b5")
frame_inst_log = Frame(label_main, bg="#0572b5")
frame_comp_log = Frame(label_main, bg="#0572b5")

window.mainloop()
