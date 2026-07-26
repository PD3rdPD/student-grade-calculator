"""Simple command-line student grade calculator."""


def letter_grade(average: float) -> str:
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
    return sum(grades) / len(grades)


def main() -> None:
    print("Student Grade Calculator")
    name = input("Student name: ").strip()
    raw_grades = input("Enter grades separated by commas: ")
    grades = [float(value.strip()) for value in raw_grades.split(",")]
    average = calculate_average(grades)
    print(f"Student: {name}")
    print(f"Average: {average:.2f}")
    print(f"Letter grade: {letter_grade(average)}")


if __name__ == "__main__":
    main()
