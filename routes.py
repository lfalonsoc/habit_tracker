import datetime
import uuid
from typing import Any

from flask import (
    Blueprint, current_app, render_template, request, redirect, url_for
)

pages: Blueprint = Blueprint(
    "habits",
    __name__,
    template_folder="templates",
    static_folder="static"
)


@pages.context_processor
def add_calc_date_range() -> dict[str, Any]:
    def date_range(start: datetime.datetime) -> Any:
        dates: list[str | Any] = [start + datetime.timedelta(days=diff)\
            for diff in range(-3, 4)]
        return dates

    return {"date_range": date_range}


def today_at_midnight() -> Any:
    today: Any = datetime.datetime.today()
    return datetime.datetime(today.year, today.month, today.day)


@pages.route("/")
def index() -> Any:
    date_str: str | None = request.args.get("date")
    if date_str:
        selected_date: Any = datetime.datetime.fromisoformat(date_str)
    else:
        selected_date: Any = today_at_midnight()

    habits_on_date: Any = current_app.db.habits.find(
        {"added": {"$lte": selected_date}}
    )

    completions: list[Any] = [
        habit["habit"]
        for habit in current_app.db.completions.find({"date": selected_date})
    ]
    
    return render_template(
        "index.html",
        habits=habits_on_date,
        selected_date=selected_date,
        completions=completions,
        title="Habit Tracker - Home",
    )


@pages.route("/complete", methods=["POST"])
def complete() -> Any:
    date_string: Any = request.form.get("date")
    habit: Any = request.form.get("habitId")
    date: Any = datetime.datetime.fromisoformat(date_string)
    current_app.db.completions.insert_one({"date": date, "habit": habit})
    
    return redirect(url_for(".index", date=date_string))


@pages.route("/add", methods=['GET', 'POST'])
def add_habit() -> Any:
    today: Any = today_at_midnight()
    
    if request.form:
        current_app.db.habits.insert_one(
            {"_id": uuid.uuid4().hex, "added": today, "name": request.form.get("habit")}
        )
        
    return render_template(
        "add_habit.html",
        title="Habit Tracker - Add Habit",
        selected_date=today,
    )
