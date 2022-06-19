def itemIntCheck(user_number):
    try:
        int(user_number)
        return True
    except ValueError:
        print("Enter a whole number only")
        return False


theyInputRight = False

while not theyInputRight:
    menu_Number_Select = input("Please select from 1 through: ")
    theyInputRight = itemIntCheck(menu_Number_Select)

menu_Number_Select = int(menu_Number_Select)
