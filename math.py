def calculate_sum(num_list):
    """Calculate the sum of a list of numbers."""
    total = 0
    for num in num_list:
        total += num
    return total


def main():
    """Main function that demonstrates the use of calculate_sum."""
    numbers = [1, 2, 3, 4, 5]
    result = calculate_sum(numbers)
    print(f"The sum of {numbers} is {result}.")


if __name__ == '__main__':
    main()
