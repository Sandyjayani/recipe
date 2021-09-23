import requests

''' app_id = f79ed4b2
    app_key = 758ec61e53ffcfdba764003d0c8ceb29
'''


# Ask user to enter an ingredient that they want to search for
def get_ingredient():
    ingredient = input("Please enter an ingredient that you want to search for: ")
    return ingredient


# Check if ingredient is empty
def check_ingredient(ingredient):
    if ingredient.isdigit() or ingredient is None or ingredient == "":
        bad_ingredient = input("I am sorry, Please enter a valid ingredients: ")
        check_ingredient(bad_ingredient)
    else:
        return ingredient


def meal_type():
    chosen_meal = input("Please choose a meal type from Breakfast, Lunch, Dinner, Snack, Teatime: ").lower()
    return chosen_meal


def check_meal_type(chosen_meal):
    meals = ['breakfast', 'lunch', 'dinner', 'snack', 'teatime']
    if chosen_meal not in meals:
        check_meal = input(
            "Invalid meal, Please choose a meal type from Breakfast, Lunch, Dinner, Snack, Teatime: ").lower()
        check_meal_type(check_meal)
    else:
        return chosen_meal


def get_app_id():
    app_id = input("Please enter your app_id: ")
    return app_id


def check_app_id(app_id):
    if app_id is None or app_id == "0" or app_id == "":
        new_app_id = input('Invalid ID, Please enter valid API ID: ')
        check_app_id(new_app_id)
    else:
        return app_id


def get_app_key():
    app_key = input("Please enter your app_key: ")
    return app_key


def check_app_key(app_key):
    if app_key is None or app_key == "0" or app_key == "":
        new_app_key = input('Invalid Key, Please enter valid API KEY: ')
        check_app_key(new_app_key)
    else:
        return app_key


# function to connect with the API
def recipe_search(ingredient, app_id, app_key, chosen_meal):
    result = requests.get(
        f'https://api.edamam.com/search?q={ingredient}&app_id={app_id}&app_key={app_key}&mealType={chosen_meal}')
    recipes = result.json()
    return recipes['hits']


def get_recipes(recipes):
    with open('recipes.txt', 'w') as file:
        for result in recipes:
            recipe_data = result['recipe']
            # find serving size for each recipe and calculate calories per serving
            calories_per_serving = int(recipe_data['calories'] / int(recipe_data['yield']))
            file.write('Recipe: ' + recipe_data['label'] + '\n')
            file.write('Calories: ' + str(recipe_data['calories']) + '\n')
            file.write('Calories per serving: ' + str(calories_per_serving) + '\n')
            file.write('Time to cook: ' + str(recipe_data['totalTime']) + '\n')
            file.write('Ingredients: ' + str(recipe_data['ingredientLines']) + '\n')
            file.write('Link: ' + recipe_data['url'] + '\n')
            file.write('\n')
    file.close()
    return recipes


def get_user_choice(recipes):
    recipe_index = 0
    for result in recipes:
        recipe_data = result['recipe']
        recipe_index += 1
        print(f"Recipe number {recipe_index} has {recipe_data['calories']} calories")
        recipe_name = recipe_data['label']
        print(f"Recipe name: {recipe_name}")
        diet_labels = recipe_data['dietLabels']
        health_labels = recipe_data['healthLabels']
        print(f"Diet and health labels: {diet_labels}, {health_labels}")
        ingredients = recipe_data['ingredientLines']
        print(f"Ingredients: {ingredients}")
        print("\n")

    user_choice = int(input("Please enter the recipe number that you would like to choose: "))
    return user_choice - 1


def add_to_shopping_list(recipes, user_choice):
    ingredients = recipes[user_choice]['recipe']['ingredientLines']
    with open("shopping_list.txt", "a") as file:
        for ingredient in ingredients:
            file.write(ingredient + "\n")
    file.close()


def show_shopping_list():
    with open("shopping_list.txt", "r") as file:
        shopping_list = file.readlines()
        for item in shopping_list:
            print(item.strip())
    file.close()


def another_search():
    search_again = input("Do you want to search for another recipe? (Y/N): ").upper()
    return search_again


def repeat_search(search_again):
    if search_again == "Y":
        main()
    elif search_again == "N":
        show_shopping_list()
    else:
        new_search = input("Do you want to search for another recipe? (Y/N): ").upper()
        repeat_search(new_search)


def main():
    ingredient = get_ingredient()
    check_ingredient(ingredient)

    chosen_meal = meal_type()
    check_meal_type(chosen_meal)

    app_id = get_app_id()
    check_app_id(app_id)

    app_key = get_app_key()
    check_app_key(app_key)

    recipes = recipe_search(ingredient, app_id, app_key, chosen_meal)
    get_recipes(recipes)

    user_choice = get_user_choice(recipes)
    add_to_shopping_list(recipes, user_choice)

    search_again = another_search()
    repeat_search(search_again)


if __name__ == '__main__':
    main()

