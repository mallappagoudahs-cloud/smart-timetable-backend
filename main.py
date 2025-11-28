from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

@app.get("/home")
def home():
    return {"message": "Backend Running Successfully"}

# ------------ INPUT MODEL ---------------
class TimetableRequest(BaseModel):
    classes: List[str]
    subjects: Dict[str, List[str]]
    teachers: Dict[str, str]
    timeslots: List[str]

# ------------ LOGIC ---------------------
@app.post("/generate-timetable")
def generate_timetable(data: TimetableRequest):

    timetable = {}

    for cls in data.classes:
        timetable[cls] = {}
        available_times = data.timeslots.copy()
        sub_list = data.subjects[cls]

        for subject in sub_list:
            if available_times:
                slot = available_times.pop(0)
                teacher = data.teachers.get(subject, "Unknown")
                timetable[cls][slot] = {
                    "subject": subject,
                    "teacher": teacher
                }

    return {"timetable": timetable}
