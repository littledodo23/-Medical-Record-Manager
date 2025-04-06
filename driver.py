import re
import datetime
import statistics
# Define the file where all medical test records will be stored
FILE = "medicalRecord.txt"
test_file="medicalTest.txt"

def display_menu():
    print("===============================")
    print("        Medical Test System")
    print("===============================")
    print("1. Add a new medical test")
    print("2. Add a new medical test record")
    print("3. Update patient records including all fields")
    print("4. Update medical tests in the medicalTest file")
    print("5. Filter medical tests")
    print("6. Exit")
    print("===============================")
    return input("Please choose an option: ")

def is_valid_test_name(test_name):
    with open(test_file, "r") as file:
        for line in file:
            stored_test_name = line.strip().split(', ')[0]
            if test_name == stored_test_name:
                return True
    return False

def validate_turnaround_time(days, hours, minutes):
    if days < 0 or days > 31:
        print("Days must be between 0 and 31.")
        return False
    if hours < 0 or hours >= 24:
        print("Hours must be between 0 and 23.")
        return False
    if minutes < 0 or minutes >= 60:
        print("Minutes must be between 0 and 59.")
        return False
    return True

def is_existing_test(patient_id, test_name):
    try:
        with open(FILE, "r") as file:
            for line in file:
                try:
                    line_patient_id, rest_of_line = line.split(": ", 1)
                    line_test_name = rest_of_line.split(", ")[0]
                    if line_patient_id.strip() == patient_id and line_test_name.strip().upper() == test_name.upper():
                        return True
                except ValueError:
                    print(f"Skipping malformed line: {line.strip()}")
                    continue
    except FileNotFoundError:
        print("Medical record file not found.")
        return False
    return False

def is_future_date(test_date_time):
    try:
        test_datetime = datetime.datetime.strptime(test_date_time, '%Y-%m-%d %H:%M')
        current_datetime = datetime.datetime.now()
        return test_datetime > current_datetime
    except ValueError:
        print("Invalid date and time format. Must be YYYY-MM-DD hh:mm.")
        return False

def load_records(file_path):
    records = []
    try:
        with open(file_path, "r") as file:
            for line in file:
                records.append(line.strip())
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    return records

def save_records(file_path, records):
    with open(file_path, "w") as file:
        for record in records:
            file.write(record + "\n")

def load_test_records(file_path):
    tests = []
    try:
        with open(file_path, "r") as file:
            for line in file:
                tests.append(line.strip())
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    return tests

def update_test(file_path):
    tests = load_test_records(file_path)
    if not tests:
        print("No tests available to update.")
        return
    print("Available Tests:")
    for i, test in enumerate(tests, 1):
        print(f"{i}. {test}")
    while True:
        try:
            choice = int(input("Select the test number to update: "))
            if 1 <= choice <= len(tests):
                selected_test = tests[choice - 1]
                break
            else:
                print("Invalid selection. Please choose a valid test number.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    test_name, normal_range, result_unit, turnaround_time = selected_test.split(', ')
    print("Leave field blank to keep the current value.")
    new_test_name = input(f"Enter new Test Name (current: {test_name}): ").strip() or test_name
    new_normal_range = input(f"Enter new Normal Range (current: {normal_range}): ").strip() or normal_range
    new_result_unit = input(f"Enter new Result Unit (current: {result_unit}): ").strip() or result_unit
    while True:
        new_turnaround_time = input(f"Enter new Turnaround Time (current: {turnaround_time}, format DD-hh-mm): ").strip() or turnaround_time
        try:
            days, hours, minutes = map(int, new_turnaround_time.split('-'))
        except ValueError:
            print("Invalid format. Must be in format DD-hh-mm. Please try again.")
            continue
        if validate_turnaround_time(days, hours, minutes):
            break
        else:
            print("Invalid turnaround time. Please ensure days (0-31), hours (0-23), and minutes (0-59) are correct.")
    tests[choice - 1] = f"{new_test_name}, {new_normal_range}, {new_result_unit}, {new_turnaround_time}"
    save_records(file_path, tests)
    print("Test updated successfully.")

def add_record():
    while True:
        patient_id = input("Enter Patient ID (7-digit integer): ")
        if not patient_id.isdigit() or len(patient_id) != 7:
            print("Invalid Patient ID. Must be a 7-digit integer. Please try again.")
            continue
        break
    while True:
        test_name = input("Enter Test Name (e.g., 'Hgb', 'BGT', 'LDL', 'systole', 'diastole'): ").upper()
        if not is_valid_test_name(test_name):
            print("Invalid Test Name. Please try again.")
            continue
        break
    while True:
        test_date_time = input("Enter Test Date and Time (format YYYY-MM-DD hh:mm): ")
        try:
            datetime.datetime.strptime(test_date_time, '%Y-%m-%d %H:%M')
            if is_future_date(test_date_time):
                print("The test date cannot be in the future. Please try again.")
                continue
        except ValueError:
            print("Invalid Test Date and Time format. Must be YYYY-MM-DD hh:mm. Please try again.")
            continue
        break
    while True:
        result = input("Enter Test Result (numeric value): ")
        try:
            result = float(result)
        except ValueError:
            print("Invalid result. Must be a numeric value. Please try again.")
            continue
        break
    result_unit = input("Enter Result Unit (e.g., 'mg/dL', 'mm Hg'): ")
    while True:
        status = input("Enter Test Status (Pending, Completed, Reviewed): ").capitalize()
        if status not in ["Pending", "Completed", "Reviewed"]:
            print("Invalid Status. Must be one of 'Pending', 'Completed', or 'Reviewed'. Please try again.")
            continue
        break
    results_date_time = ''
    if status == "Completed":
        while True:
            results_date_time = input("Enter Results Date and Time (format YYYY-MM-DD hh:mm): ")
            try:
                datetime.datetime.strptime(results_date_time, '%Y-%m-%d %H:%M')
            except ValueError:
                print("Invalid Results Date and Time format. Must be YYYY-MM-DD hh:mm. Please try again.")
                continue
            break
    with open(FILE, "a") as file:
        file.write(f"{patient_id}: {test_name}, {test_date_time}, {result}, {result_unit}, {status}, {results_date_time}\n")
    print("Record added successfully.")

def add_new_medical_test():
    while True:
        test_name = input("Enter new Test Name: ").strip().upper()
        if not test_name:
            print("Test Name cannot be empty. Please try again.")
            continue
        if test_name.isdigit():
            print("char only ")
            continue
        with open(test_file, "r") as file:
            if any(test_name in line for line in file):
                print("Test Name already exists. Please try again.")
                continue
        break
    while True:
        normal_range = input("Enter normal range (e.g., '> 13.8, < 17.2' or '< 100'): ").strip()
        if not normal_range:
            print("Normal Range cannot be empty. Please try again.")
            continue
        break
    while True:
        result_unit = input("Enter Result Unit (e.g., 'g/dL', 'mg/dL', 'mm Hg'): ").strip()
        if not result_unit:
            print("Result Unit cannot be empty. Please try again.")
            continue
        break
    while True:
        turnaround = input("Enter turnaround time (format DD-hh-mm): ").strip()
        match = re.match(r"^(\d{2})-(\d{2})-(\d{2})$", turnaround)
        if not match:
            print("Invalid turnaround time format. Must be DD-hh-mm. Please try again.")
            continue
        days, hours, minutes = map(int, match.groups())
        if not validate_turnaround_time(days, hours, minutes):
            continue
        break
    with open(test_file, "a") as file:
        file.write(f"{test_name}, {normal_range}, {result_unit}, {turnaround}\n")
    print("New medical test added successfully.")


def update_record():
    patient_id_to_update = input("Enter Patient ID (7-digit integer) to update: ")
    test_name_to_update = input(
        "Enter Test Name to update (e.g., 'Hgb', 'BGT', 'LDL', 'systole', 'diastole'): ").upper()
    updated = False

    try:
        with open(FILE, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"File {FILE} not found.")
        return

    with open(FILE, "w") as file:
        for line in lines:
            try:
                line_patient_id, rest_of_line = line.split(": ", 1)
                if line_patient_id != patient_id_to_update:
                    file.write(line)
                    continue

                details = rest_of_line.strip().split(", ")
                line_test_name = details[0]
                line_test_date_time = details[1]
                line_result = details[2]
                line_result_unit = details[3]
                line_status = details[4]
                line_results_date_time = details[5] if len(details) > 5 else ''

                if line_test_name != test_name_to_update:
                    file.write(line)
                    continue

                print(f"Updating record for Patient ID: {patient_id_to_update}, Test Name: {test_name_to_update}")

                # Get new values or keep current values
                test_name = input(
                    f"Enter new Test Name (current: {line_test_name}) or press Enter to keep: ").upper() or line_test_name

                while True:
                    test_date_time = input(
                        f"Enter new Test Date and Time (current: {line_test_date_time}) or press Enter to keep: ")
                    if test_date_time == '':
                        test_date_time = line_test_date_time
                        break
                    if is_future_date(test_date_time):
                        print("Test date cannot be in the future. Please try again.")
                        continue
                    break

                while True:
                    result = input(f"Enter new Test Result (current: {line_result}) or press Enter to keep: ")
                    if result == '':
                        result = line_result
                        break
                    try:
                        result = float(result)
                        break
                    except ValueError:
                        print("Invalid result. Must be a numeric value. Please try again.")

                result_unit = input(
                    f"Enter new Result Unit (current: {line_result_unit}) or press Enter to keep: ") or line_result_unit

                # Proper status input handling
                valid_statuses = ["Pending", "Completed", "Reviewed"]
                while True:
                    status = input(
                        f"Enter new Test Status (current: {line_status}) or press Enter to keep: ").capitalize()
                    if status == '':
                        status = line_status
                    if status in valid_statuses:
                        break
                    else:
                        print(f"Invalid Status. Must be one of {', '.join(valid_statuses)}. Please try again.")

                if status == "Completed":
                    while True:
                        results_date_time = input(
                            f"Enter new Results Date and Time (current: {line_results_date_time}) or press Enter to keep: ")
                        if results_date_time == '':
                            results_date_time = line_results_date_time
                            break
                        if is_future_date(results_date_time):
                            print("Results date cannot be in the future. Please try again.")
                            continue
                        break
                else:
                    results_date_time = line_results_date_time

                file.write(
                    f"{patient_id_to_update}: {test_name}, {test_date_time}, {result}, {result_unit}, {status}, {results_date_time}\n")
                updated = True

            except ValueError:
                print(f"Skipping malformed record: {line.strip()}")
                continue

    if updated:
        print("Record updated successfully.")
    else:
        print("No matching record found.")


def generate_summary_report(filtered_records, test_values, turnaround_times):
    """Generate and display a summary report of the filtered records."""
    print("\n--- Summary Report ---")

    if not filtered_records:
        print("No records found matching the criteria.")
        return

    # Display the filtered records
    print("\nFiltered Records:")
    for rec in filtered_records:
        print(rec)

    # Descriptive statistics for test values
    if test_values:
        print("\nTest Value Statistics:")
        print(f"Minimum Test Value: {min(test_values)}")
        print(f"Maximum Test Value: {max(test_values)}")
        print(f"Average Test Value: {statistics.mean(test_values)}")
    else:
        print("\nNo test values available for statistics.")

    # Descriptive statistics for turnaround times
    if turnaround_times:
        print("\nTurnaround Time Statistics (in minutes):")
        print(f"Minimum Turnaround Time: {min(turnaround_times)} minutes")
        print(f"Maximum Turnaround Time: {max(turnaround_times)} minutes")
        print(f"Average Turnaround Time: {statistics.mean(turnaround_times):.2f} minutes")
    else:
        print("\nNo turnaround times available for statistics.")

    print("--- End of Summary Report ---\n")


def filter_tests():
    filters = {}

    # Filter by Patient ID
    while True:
        patient_id = input("Enter Patient ID to filter by or press Enter to skip: ").strip()
        if patient_id and (not patient_id.isdigit() or len(patient_id) != 7):
            print("Invalid Patient ID. Must be a 7-digit integer. Please try again.")
        else:
            break
    if patient_id:
        filters['patient_id'] = patient_id

    # Filter by Test Name
    while True:
        test_name = input("Enter Test Name to filter by or press Enter to skip: ").strip().upper()
        if test_name and not test_name.isalpha():
            print("Invalid Test Name. Please enter alphabetic characters only.")
        else:
            break
    if test_name:
        filters['test_name'] = test_name

    # Filter by Abnormal Tests
    while True:
        abnormal_choice = input("Filter by abnormal tests? (y/n): ").strip().lower()
        if abnormal_choice not in ['y', 'n', '']:
            print("Invalid choice. Please enter 'y' for Yes or 'n' for No.")
        else:
            break
    if abnormal_choice == 'y':
        filters['abnormal'] = True

    # Filter by Date Range
    while True:
        start_date = input("Enter start date (YYYY-MM-DD) to filter by or press Enter to skip: ").strip()
        end_date = input("Enter end date (YYYY-MM-DD) to filter by or press Enter to skip: ").strip()

        if start_date and end_date:
            try:
                # Validate the date formats
                start_date_obj = datetime.datetime.strptime(start_date, '%Y-%m-%d')
                end_date_obj = datetime.datetime.strptime(end_date, '%Y-%m-%d')

                # Check if start date is after end date
                if start_date > end_date:
                    print("Start date cannot be after end date. Please try again.")
                    continue

                # Check if the dates are in the future
                if is_future_date(start_date) or is_future_date(end_date):
                    print("Dates cannot be in the future. Please try again.")
                    continue

            except ValueError:
                print("Invalid date format. Please enter dates in YYYY-MM-DD format.")
                continue
        break

    # If both start_date and end_date are valid, store the filter
    if start_date and end_date:
        filters['date_range'] = (start_date, end_date)
        print("Date range filter applied:", filters['date_range'])

    # Filter by Test Status
    while True:
        status = input(
            "Enter Test Status (Pending, Completed, Reviewed) to filter by or press Enter to skip: ").capitalize()
        if status and status not in ["Pending", "Completed", "Reviewed"]:
            print("Invalid Status. Must be one of 'Pending', 'Completed', or 'Reviewed'. Please try again.")
        else:
            break
    if status:
        filters['status'] = status

    # Filter by Turnaround Time
    while True:
        min_turnaround = input(
            "Enter minimum turnaround time (in minutes) to filter by or press Enter to skip: ").strip()
        max_turnaround = input(
            "Enter maximum turnaround time (in minutes) to filter by or press Enter to skip: ").strip()
        if min_turnaround and max_turnaround:
            try:
                min_turnaround = int(min_turnaround)
                max_turnaround = int(max_turnaround)
                if min_turnaround < 0 or max_turnaround < 0:
                    print("Turnaround time cannot be negative. Please try again.")
                    continue
                if min_turnaround > max_turnaround:
                    print("Minimum turnaround time cannot be greater than maximum. Please try again.")
                    continue
            except ValueError:
                print("Invalid input. Please enter numeric values for turnaround time.")
                continue
        break
    if min_turnaround and max_turnaround:
        filters['turnaround'] = (min_turnaround, max_turnaround)

    filtered_records = []
    test_values = []
    turnaround_times = []

    try:
        records = load_records(FILE)
        for record in records:
            try:
                patient_id_record, details = record.split(": ", 1)
                test_name_record, test_date_time, result, result_unit, status_record, *results_date_time = details.split(
                    ", ")
                result = float(result)
                if 'patient_id' in filters and filters['patient_id'] != patient_id_record:
                    continue
                if 'test_name' in filters and filters['test_name'] != test_name_record.upper():
                    continue
                if 'abnormal' in filters:
                    test_range = None
                    with open(test_file, "r") as file:
                        for line in file:
                            stored_test_name, normal_range, *_ = line.strip().split(', ')
                            if test_name_record.upper() == stored_test_name:
                                test_range = normal_range
                                break
                    if test_range and not eval(f"{result} {test_range}"):
                        continue
                if 'date_range' in filters:
                    test_date = test_date_time.split(' ')[0]
                    if not (filters['date_range'][0] <= test_date <= filters['date_range'][1]):
                        continue
                if 'status' in filters and filters['status'] != status_record:
                    continue
                if 'turnaround' in filters:
                    turnaround_minutes = (int(test_date_time.split('-')[1]) * 60 + int(test_date_time.split('-')[2]))
                    if not (filters['turnaround'][0] <= turnaround_minutes <= filters['turnaround'][1]):
                        continue
                    turnaround_times.append(turnaround_minutes)

                filtered_records.append(record)
                test_values.append(result)

            except ValueError:
                print(f"Skipping malformed record: {record.strip()}")
                continue
    except FileNotFoundError:
        print(f"File {FILE} not found. Please ensure the file exists.")
        return
    except Exception as e:
        print(f"An error occurred while processing records: {e}")
        return

    # Generate the summary report
    generate_summary_report(filtered_records, test_values, turnaround_times)


def main():
    while True:
        choice = display_menu()
        if choice == "1":
            add_new_medical_test()
        elif choice == "2":
            add_record()
        elif choice == "3":
            update_record()
        elif choice == "4":
            update_test(test_file)
        elif choice == "5":
            filter_tests()
        elif choice == "6":
            print("Exiting the program.")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()