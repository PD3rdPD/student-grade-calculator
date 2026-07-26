"""Command-line student grade calculator with validation and CSV export."""

from __future__ import annotations

import csv
from pathlib import Path


def letter_grade(average: float) -> str:
    """Return the standard letter grade for a numeric average."""
    if average >= 90:
        return "A"
    if average >= 80:
        return "B"
    if average >= 70:
        return "C"
    if average >= 60:
        return "D"
    return "F"


def calculate_average(grades: list[float]) -> float:
    """Calculate the arithmetic mean of a non-empty grade list."""
    if not grades:
        raise ValueError("At least one grade is required.")
    return sum(grades) / len(grades)


def parse_grades(raw_grades: str) -> list[float]:
    """Parse and validate comma-separated grades between 0 and 100."""
    if not raw_grades.strip():
        raise ValueError("Enter at least one grade.")

    grades: list[float] = []
    for item in raw_grades.split(","):
        try:
            grade = float(item.strip())
        except ValueError as exc:
            raise ValueError(f"'{item.strip()}' is not a valid number.") from exc
        if not 0 <= grade <= 100:
            raise ValueError("Each grade must be between 0 and 100.")
        grades.append(grade)
    return grades


def export_result(name: str, grades: list[float], output_file: str = "grade_report.csv") -> Path:
    """Export the result to a CSV file and return its path."""
    average = calculate_average(grades)
    path = Path(output_file)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Student", "Grades", "Average", "Letter Grade"])
        writer.writerow([name, "; ".join(f"{grade:g}" for grade in grades), f"{average:.2f}", letter_grade(average)])
    return path


def main() -> None:
    print("Student Grade Calculator")
    name = input("Student name: ").strip()
    if not name:
        print("Error: Student name is required.")
        return

    try:
        grades = parse_grades(input("Enter grades separated by commas: "))
    except ValueError as error:
        print(f"Error: {error}")
        return

    average = calculate_average(grades)
    print(f"Student: {name}")
    print(f"Average: {average:.2f}")
    print(f"Letter grade: {letter_grade(average)}")

    save = input("Save the result to grade_report.csv? (y/n): ").strip().lower()
    if save == "y":
        path = export_result(name, grades)
        print(f"Saved: {path.resolve()}")


if __name__ == "__main__":
    main()
