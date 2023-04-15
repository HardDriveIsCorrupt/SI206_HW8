# Your name: Ethan Lancaster
# Your student id: 50763057
# Your email: ethanlan@umich.edu
# List who you have worked with on this homework:

import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def load_rest_data(db):
    """
    This function accepts the file name of a database as a parameter and returns a nested
    dictionary. Each outer key of the dictionary is the name of each restaurant in the database, 
    and each inner key is a dictionary, where the key:value pairs should be the category, 
    building, and rating for the restaurant.
    """
    conn = sqlite3.connect(db)
    c = conn.cursor()

    c.execute("SELECT name, category_id, building_id, rating FROM restaurants")
    rows = c.fetchall()

    categories = {}
    c.execute("SELECT id, category FROM categories")
    cat_rows = c.fetchall()
    for cat_row in cat_rows:
        category_id = cat_row[0]
        category_type = cat_row[1]
        categories[category_id] = category_type

    buildings = {}
    c.execute("SELECT id, building FROM buildings")
    build_rows = c.fetchall()
    for build_row in build_rows:
        build_id = build_row[0]
        build_num = build_row[1]
        buildings[build_id] = build_num

    restaurants = {}
    for row in rows:
        name = row[0]
        category_id = row[1]
        building_id = row[2]
        rating = row[3]
        restaurants[name] = {
            "category": categories[category_id],
            "building": buildings[building_id],
            "rating": rating
        }

    conn.close()

    return restaurants

def plot_rest_categories(db):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the count of number of restaurants in each category.
    """
    conn = sqlite3.connect(db)
    c = conn.cursor()

    c.execute("SELECT category_id, COUNT(name) FROM restaurants GROUP BY category_id")
    rows = c.fetchall()

    categoriesName = {}
    c.execute("SELECT id, category FROM categories")
    cat_rows = c.fetchall()
    for cat_row in cat_rows:
        category_id = cat_row[0]
        category_type = cat_row[1]
        categoriesName[category_id] = category_type


    categories = {}
    for row in rows:
        categoryName = categoriesName[row[0]]
        count = row[1]
        categories[categoryName] = count

    conn.close()

    sorted_categories = dict(sorted(categories.items(), key=lambda x: x[1] if x[1] is not None else 0, reverse=False))

    plt.barh(list(sorted_categories.keys()), list(sorted_categories.values()))
    plt.xticks(rotation=90)
    plt.ylabel("Restaurant Category", fontsize=10)
    plt.title("Types of Restaurant on South University Ave", y=1.05, fontsize=16)
    plt.xlabel("Number of Restaurants")
    plt.tight_layout()
    plt.show()

    return sorted_categories

def find_rest_in_building(building_num, db):
    '''
    This function accepts the building number and the filename of the database as parameters and returns a list of 
    restaurant names. You need to find all the restaurant names which are in the specific building. The restaurants 
    should be sorted by their rating from highest to lowest.
    '''
    conn = sqlite3.connect(db)
    c = conn.cursor()

    buildings = {}
    c.execute("SELECT id, building FROM buildings")
    build_rows = c.fetchall()
    for build_row in build_rows:
        build_id = build_row[0]
        build_num = build_row[1]
        buildings[build_num] = build_id

    c.execute("SELECT name FROM restaurants WHERE building_id = ? ORDER BY rating DESC", (buildings[building_num],))
    rows = c.fetchall()
 
    restaurants = []
    for row in rows:
        name = row[0]
        restaurants.append(name)

    conn.close()

    return restaurants

#EXTRA CREDIT
def get_highest_rating(db): #Do this through DB as well
    """
    This function return a list of two tuples. The first tuple contains the highest-rated restaurant category 
    and the average rating of the restaurants in that category, and the second tuple contains the building number 
    which has the highest rating of restaurants and its average rating.

    This function should also plot two barcharts in one figure. The first bar chart displays the categories 
    along the y-axis and their ratings along the x-axis in descending order (by rating).
    The second bar chart displays the buildings along the y-axis and their ratings along the x-axis 
    in descending order (by rating).
    """
    conn = sqlite3.connect(db)
    c = conn.cursor()

    # Get the average rating for each category of restaurants
    c.execute("SELECT category_id, ROUND(AVG(rating), 1) AS avg_rating FROM restaurants GROUP BY category_id ORDER BY avg_rating DESC")
    categories = []
    avg_ratings_by_category = []
    for row in c.fetchall():
        categories.append(row[0])
        avg_ratings_by_category.append(row[1])

    # Get the average rating for each building
    c.execute("SELECT building_id, ROUND(AVG(rating), 1) AS avg_rating FROM restaurants GROUP BY building_id ORDER BY avg_rating DESC")
    buildings = []
    avg_ratings_by_building = []
    for row in c.fetchall():
        buildings.append(row[0])
        avg_ratings_by_building.append(row[1])

    # Plot the bar charts
    fig = plt.figure(figsize=(8,8))
    plt.subplot(211)
    plt.barh(categories, avg_ratings_by_category)
    plt.title("Average ratings by category")
    plt.xlabel("Average rating")
    plt.ylabel("Category")
    plt.xlim(0, 5)

    plt.subplot(212)
    plt.barh(buildings, avg_ratings_by_building)
    plt.title("Average ratings by building")
    plt.xlabel("Average rating")
    plt.ylabel("Building")
    plt.xlim(0, 5)

    plt.tight_layout()
    plt.show()

#Try calling your functions here
def main():
    pass

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.highest_rating = [('Deli', 4.6), (1335, 4.8)]

    def test_load_rest_data(self):
        rest_data = load_rest_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, dict)
        self.assertEqual(rest_data['M-36 Coffee Roasters Cafe'], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_plot_rest_categories(self):
        cat_data = plot_rest_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_find_rest_in_building(self):
        restaurant_list = find_rest_in_building(1140, 'South_U_Restaurants.db')
        self.assertIsInstance(restaurant_list, list)
        self.assertEqual(len(restaurant_list), 3)
        self.assertEqual(restaurant_list[0], 'BTB Burrito')

    def test_get_highest_rating(self):
        highest_rating = get_highest_rating('South_U_Restaurants.db')
        self.assertEqual(highest_rating, self.highest_rating)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
