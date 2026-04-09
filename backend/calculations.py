
def subjectMarks(marks):
    if len(marks) != 5:
        raise HTTPException(status_code=400, detail="Enter exactly five marks")

    listofmarks = []

    for i in marks:
        try:
            value = float(i)
        except ValueError:
            raise HTTPException(status_code=400, detail="Marks must be numbers")

        if 0 <= value <= 100:
            listofmarks.append(value)
        else:
            raise HTTPException(status_code=400, detail="Marks must be between 0 and 100")

    return listofmarks


def totalMarks(marks):
    total=sum(marks)
    return total

def averageMarks(marks):
    average= sum(marks) / len(marks)
    return average


def gradeAssignment(average):
    if average >= 80:
        return "A Grade"
    elif average >= 60:
        return "B Grade"
    elif average >= 40:
        return "C Grade"
    else:
        return "Fail"