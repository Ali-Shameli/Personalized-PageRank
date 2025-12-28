def get_valid_input(prompt, parse_func, condition=lambda x: True, error_msg="Invalid input."):
    """
    Helper function to ensure user input is valid.
    """
    while True:
        try:
            user_input = input(prompt).strip()
            if not user_input:
                continue
            parsed_value = parse_func(user_input)
            if condition(parsed_value):
                return parsed_value
            else:
                print(error_msg)
        except ValueError:
            print(error_msg)
        except Exception as e:
            print(f"Unexpected error: {e}")