import class_student_course as data
import json

#--------------------------------------輸入-----------------------------------------------------------------
def InputStudent( Is_Change : bool ):
    with open("student.json", "r") as f:
            student_data = json.load(f)
    if "Student" not in student_data:
        student_data["Student"] = {}
    if Is_Change :
        student_id = input("Enter student ID to change: ")
        if student_id not in student_data["Student"]:
            print("Student ID not found. Please enter a valid ID.")
            return None
    else:
        student_id = input("Enter student ID: ")
        if student_id in student_data["Student"]:
            print("Student ID already exists. Please enter a unique ID.")
            return None
    name = input("Enter student name: ")
    major = input("Enter student major: ")
    selected_courses = input("Enter selected courses (comma-separated): ").split(",")
    try:
        credit = int(input("Enter student credit: "))
    except ValueError:
        print("Invalid credit value. Please enter a valid integer.")
        return None
    new_student = data.Student(
        student_id=student_id,
        name=name,
        major=major,
        selected_courses=selected_courses,
        credit=credit
    )
    print(f"Student {name} created successfully.")
    return new_student


def InputCourse(Is_Change: bool):
    with open("course.json", "r") as f:
        course_data = json.load(f)
    if "Course" not in course_data:
        course_data["Course"] = {} 
    if Is_Change:
        course_id = input("Enter course ID to change: ")
        if course_id not in course_data["Course"]:
            print("Course ID not found. Please enter a valid ID.")
            return None
    else:
        course_id = input("Enter course ID: ")
        if course_id in course_data["Course"]:
            print("Course ID already exists. Please enter a unique ID.")
            return None
    course_name = input("Enter course name: ")
    credit = int(input("Enter course credit: "))
    is_required = input("Is the course required? (True/False): ").lower()
    instructor = input("Enter instructor name: ")
    students_limit = int(input("Enter students limit: "))
    classroom = input("Enter classroom: ")
    schedule_input = input(
        "Enter schedule (e.g., {'Monday': [1, 2];'Wednesday': [3, 4]}): ").split(";")
    schedule = {}
    for item in schedule_input:
        day, times = item.split(":")
        schedule[day.strip()] = list(map(int, times.strip()[1:-1].split(",")))
    new_course = data.Course(
        course_id=course_id,
        course_name=course_name,
        credit=credit,
        is_required=is_required,
        instructor=instructor,
        students_limit=students_limit,
        classroom=classroom,
        schedule=schedule
    )
    return new_course

#--------------------------------------功能-----------------------------------------------------------------

def CreateStudent():
    new_student = InputStudent(False)
    if new_student is None:
        return
    with open("student.json", "r") as f:
        student_data = json.load(f)
    new_student_data = new_student.output_json()
    print(new_student_data)
        # 2. 將新學生資料安全地更新進去
    student_data["Student"].update(new_student_data["Student"])
    with open("student.json", "w") as f:
        json.dump(student_data, f, indent=4)

def DeleteStudent():
    student_id = input("Enter student ID to delete: ")
    with open("student.json", "r") as f:
        student_data = json.load(f)
    if student_id in student_data["Student"]:
        del student_data["Student"][student_id]
        with open("student.json", "w") as f:
            json.dump(student_data, f, indent=4)
        print(f"Student {student_id} deleted successfully.")
    else:
        print(f"Student ID {student_id} not found.")

def ChangeStudent():
    Changing_student = InputStudent(True)
    if Changing_student is None:
        return
    with open("student.json", "r") as f:
        student_data = json.load(f)
    student_data["Student"][Changing_student.student_id] = Changing_student.output_json()["Student"][Changing_student.student_id]
    with open("student.json", "w") as f:
        json.dump(student_data, f, indent=4)
        

def SearchStudent():
    student_id = input("Enter student ID to search: ")
    with open("student.json", "r") as f:
        student_data = json.load(f)
    if student_id in student_data["Student"]:
        student_info = student_data["Student"][student_id]
        print(f"Student ID: {student_id}")
        print(f"Name: {student_info['name']}")
        print(f"Major: {student_info['major']}")
        print(f"Selected Courses: {', '.join(str(course) for course in student_info['selected_courses'])}")
        print(f"Credit: {student_info['credit']}")
    else:
        print(f"Student ID {student_id} not found.")

def CreateCourse():
    
    course = InputCourse(False)
    if course is None:
        return
    with open("course.json", "r") as f:
        course_data = json.load(f)
    the_new_course_data = course.output_json()
    print(the_new_course_data)
        # 2. 將新課程資料安全地更新進去
    course_data["Course"].update(the_new_course_data["Course"])
    with open("course.json", "w") as f:
        json.dump(course_data, f, indent=4)

def DeleteCourse():
    course_id = input("Enter course ID to delete: ")
    with open("course.json", "r") as f:
        course_data = json.load(f)
    if course_id in course_data["Course"]:
        del course_data["Course"][course_id]
        with open("course.json", "w") as f:
            json.dump(course_data, f, indent=4)
        print(f"Course {course_id} deleted successfully.")
    else:
        print(f"Course ID {course_id} not found.")

def ChangeCourse():
    course = InputCourse(True)
    if course is None:
        return
    with open("course.json", "r") as f:
        course_data = json.load(f)
    course_data["Course"][course.course_id] = course.output_json()["Course"][course.course_id]
    with open("course.json", "w") as f:
        json.dump(course_data, f, indent=4)

def SearchCourse():
    course_id = input("Enter course ID to search: ")
    with open("course.json", "r") as f:
        course_data = json.load(f)
    if course_id in course_data["Course"]:
        course_info = course_data["Course"][course_id]
        print(f"Course ID: {course_id}")
        print(f"Course Name: {course_info['course_name']}")
        print(f"Credit: {course_info['credit']}")
        print(f"Is Required: {course_info['is_required']}")
        print(f"Instructor: {course_info['instructor']}")
        print(f"Students Limit: {course_info['students_limit']}")
        print(f"Classroom: {course_info['classroom']}")
        print(f"Schedule: {','.join(f'{day}的{"第" + "、".join(str(t) for t in times) + "節"}' for day, times in course_info['schedule'].items())}")
    else:
        print(f"Course ID {course_id} not found.")

def CheckDuplicateJson():
    with open("student.json", "r") as f:
        student_data = json.load(f)
    with open("course.json", "r") as f:
        course_data = json.load(f)

    student_ids = student_data.get("Student").keys()
    course_ids = course_data.get("Course").keys()
    print("Student IDs:", list(student_ids))
    print("Course IDs:", list(course_ids))
    print(student_data)

