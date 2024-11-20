import sys
from typing import List
from build_data import get_data, CountyDemographics

# Display all entries in a user-friendly format
def display(data: List[CountyDemographics]) -> None:
    """
    Print the county information for each county in a user-friendly format.
    """
    for entry in data:
        print(f"County: {entry.county}, State: {entry.state}, Population: {entry.population['2014 Population']}")

# Filter entries by state abbreviation
def filter_state(data: List[CountyDemographics], state_abbr: str) -> List[CountyDemographics]:
    """
    Filter the collection of counties to those with matching state abbreviation.
    """
    filtered_data = [entry for entry in data if entry.state == state_abbr]
    print(f"Filter: state == {state_abbr} ({len(filtered_data)} entries)")
    return filtered_data

# Filter entries where a field is greater than a specified value
def filter_gt(data: List[CountyDemographics], field: str, number: float) -> List[CountyDemographics]:
    """
    Filter the collection of entries to those for which the value in the specified field is greater-than the specified number.
    """
    field_parts = field.split('.')
    filtered_data = [entry for entry in data if float(entry.__dict__[field_parts[0]][field_parts[1]]) > number]
    print(f"Filter: {field} gt {number} ({len(filtered_data)} entries)")
    return filtered_data

# Filter entries where a field is less than a specified value
def filter_lt(data: List[CountyDemographics], field: str, number: float) -> List[CountyDemographics]:
    """
    Filter the collection of entries to those for which the value in the specified field is less-than the specified number.
    """
    field_parts = field.split('.')
    filtered_data = [entry for entry in data if float(entry.__dict__[field_parts[0]][field_parts[1]]) < number]
    print(f"Filter: {field} lt {number} ({len(filtered_data)} entries)")
    return filtered_data

# Calculate and print the total 2014 population
def population_total(data: List[CountyDemographics]) -> None:
    """
    Print the total 2014 population across all current counties.
    """
    total_population = sum(float(entry.population['2014 Population']) for entry in data)
    print(f"2014 population: {total_population}")

# Calculate and print the population for a specific field
def population(data: List[CountyDemographics], field: str) -> float:
    """
    Compute the total 2014 sub-population across all current counties.
    """
    field_parts = field.split('.')
    total_population = sum(float(entry.population['2014 Population']) for entry in data)
    sub_population = sum(float(entry.population['2014 Population']) * (float(entry.__dict__[field_parts[0]][field_parts[1]]) / 100.0) for entry in data)
    print(f"2014 {field} population: {sub_population}")
    print(f"Total 2014 population: {total_population}")
    return sub_population

# Calculate and print the percentage for a specific field
def percent(data: List[CountyDemographics], field: str) -> None:
    """
    Print the percentage of the total population within the sub-population specified by field.
    """
    sub_population = population(data, field)
    total_population = sum(float(entry.population['2014 Population']) for entry in data)
    percentage = (sub_population / total_population) * 100
    print(f"2014 {field} percentage: {percentage}")

def main(operations_file: str) -> None:
    """
    Main function to load data and execute operations from the operations file.
    """
    try:
        data = get_data()
        print(f"Loaded data with {len(data)} entries")
    except Exception as e:
        print(f"Error loading data: {e}")
        sys.exit(1)

    try:
        with open(operations_file, 'r') as file:
            operations = file.readlines()

        for i, line in enumerate(operations, start=1):
            parts = line.strip().split(':')
            try:
                if parts[0] == "display":
                    display(data)
                elif parts[0] == "filter-state":
                    data = filter_state(data, parts[1])
                elif parts[0] == "filter-gt":
                    data = filter_gt(data, parts[1], float(parts[2]))
                elif parts[0] == "filter-lt":
                    data = filter_lt(data, parts[1], float(parts[2]))
                elif parts[0] == "population-total":
                    population_total(data)
                elif parts[0].startswith("population"):
                    population(data, parts[1])
                elif parts[0].startswith("percent"):
                    percent(data, parts[1])
                else:
                    print(f"Unknown operation: {line.strip()}")
            except Exception as e:
                print(f"Error processing line {i}: {line.strip()} - {e}")

    except FileNotFoundError:
        print(f"Error: Cannot open operations file '{operations_file}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing operations file: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python hw4.py <operations_file>")
        sys.exit(1)

    main(sys.argv[1])
