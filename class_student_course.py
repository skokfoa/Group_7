class Course:
    def __init__(self, 
                 course_id: int,
                 course_name: str,
                 credit: int,
                 is_required: bool,
                 instructor: str,
                 students_limit: int,
                 classroom: str,
                 schedule: dict[str, list[int]]):

        self.course_id = course_id
        self.course_name = course_name
        self.credit = credit
        self.is_required = is_required
        self.instructor = instructor
        self.students_limit = students_limit
        self.classroom = classroom
        self.schedule = schedule

    def print_course_info(self):
        print(f"course_id: {self.course_id}, "
              f"course_name: {self.course_name}, "
              f"credit: {self.credit}, "
              f"is_required: {self.is_required}, "
              f"instructor: {self.instructor}, "
              f"students_limit: {self.students_limit}, "
              f"classroom: {self.classroom}, "
              f"schedule: {self.schedule}")

    def output_json(self):
        return {
            "course_id": self.course_id,
            "course_name": self.course_name,
            "credit": self.credit,
            "is_required": self.is_required,
            "instructor": self.instructor,
            "students_limit": self.students_limit,
            "classroom": self.classroom,
            "schedule": self.schedule  # <--- 直接回傳原有的 dict，不要做列表推導式
        }

class Student:
    def __init__(self, 
                 student_id: int, 
                 name: str, 
                 major: str, 
                 selected_courses: list[Course] | None = None,
                 credit: int = 0):
        
        self.student_id = student_id
        self.name = name
        self.major = major
        self.selected_courses = selected_courses if selected_courses is not None else []
        self.credit = credit

    def print_student_info(self):
        print(f"student_id: {self.student_id}, "
              f"name: {self.name}, "
              f"major: {self.major}, "
              f"selected_courses: {[course.course_name if len(course.course_name) else 'N/A' for course in self.selected_courses]}, "
              f"credit: {self.credit}")

    def output_json(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "major": self.major,
            "selected_courses": [course.course_name for course in self.selected_courses],
            "credit": self.credit
        }
