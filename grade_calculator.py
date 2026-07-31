"""Command-line student grade calculator with validation, CSV export, and grade goal prediction."""

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


def calculate_required_grade(
    current_average: float,
    target_average: float,
    remaining_assignments: int,
) -> float:
    """Calculate the average needed on remaining assignments to reach a target grade."""
    if remaining_assignments <= 0:
        raise ValueError("Remaining assignments must be greater than zero.")

    if not 0 <= target_average <= 100:
        raise ValueError("Target grade must be between 0 and 100.")

    total_needed = target_average * (remaining_assignments + 1)
    required_score = (total_needed - current_average) / remaining_assignments

    return required_score


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


def export_result(
    name: str,
    grades: list[float],
    output_file: str = "grade_report.csv",
) -> Path:
    """Export the result to a CSV file and return its path."""
    average = calculate_average(grades)

    path = Path(output_file)

    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(
            ["Student", "Grades", "Average", "Letter Grade"]
        )

        writer.writerow(
            [
                name,
                "; ".join(f"{grade:g}" for grade in grades),
                f"{average:.2f}",
                letter_grade(average),
            ]
        )

    return path


def main() -> None:
    print("Student Grade Calculator")

    name = input("Student name: ").strip()

    if not name:
        print("Error: Student name is required.")
        return

    try:
        grades = parse_grades(
            input("Enter grades separated by commas: ")
        )

    except ValueError as error:
        print(f"Error: {error}")
        return

    average = calculate_average(grades)

    print(f"\nStudent: {name}")
    print(f"Average: {average:.2f}")
    print(f"Letter grade: {letter_grade(average)}")

    goal = input(
        "\nWould you like to calculate a target grade? (y/n): "
    ).strip().lower()

    if goal == "y":
        try:
            target = float(
                input("Desired final grade: ")
            )

            remaining = int(
                input("Number of remaining assignments: ")
            )

            needed = calculate_required_grade(
                average,
                target,
                remaining,
            )

            if needed <= 100:
                print(
                    f"You need an average of {needed:.2f}% "
                    "on your remaining assignments."
                )
            else:
                print(
                    "The target grade is not achievable "
                    "with the remaining assignments."
                )

        except ValueError as error:
            print(f"Error: {error}")

    save = input(
        "\nSave the result to grade_report.csv? (y/n): "
    ).strip().lower()

    if save == "y":
        path = export_result(name, grades)
        print(f"Saved: {path.resolve()}")


if __name__ == "__main__":
    main()