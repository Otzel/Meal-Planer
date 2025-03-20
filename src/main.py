from meal_plan import random_meal_plan
from shopping_list import create_shopping_list

if __name__ == '__main__':

    mp = random_meal_plan(4,2)
    print(mp)
    shopping_list = create_shopping_list(mp)