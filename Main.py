
import F1


while 1:
    print("1. Create Student Info")
    print("2. Delete Student Info")
    print("3. Change Student Info")
    print("4. Search Student Info")
    print("5. Create Course Info")
    print("6. Delete Course Info")
    print("7. Change Course Info")
    print("8. Search Course Info")
    print("9. Exit")
    Choice = input("Enter your choice: ")
    if Choice == "1":
        F1.CreateStudent()
    elif Choice == "2":
        F1.DeleteStudent()
    elif Choice == "3":
        F1.ChangeStudent()
    elif Choice == "4":
        F1.SearchStudent()
    elif Choice == "5":
        F1.CreateCourse()
    elif Choice == "6":
        F1.DeleteCourse()
    elif Choice == "7":
        F1.ChangeCourse()
    elif Choice == "8":
        F1.SearchCourse()
    else:
        break
