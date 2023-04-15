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

    c.execute("SELECT name FROM restaurants WHERE building = ? ORDER BY rating DESC", (building_num,))
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

    # get the highest-rated category and its average rating
    c.execute("SELECT category, AVG(rating) FROM restaurants GROUP BY category ORDER BY AVG(rating) DESC LIMIT 1")
    category_data = c.fetchone()

    # get the highest-rated building and its average rating
    c.execute("SELECT building, AVG(rating) FROM restaurants GROUP BY building ORDER BY AVG(rating) DESC LIMIT 1")
    building_data = c.fetchone()

    conn.close()

    highest_rating = [(category_data[0], category_data[1]), (building_data[0], building_data[1])]

    # plot the bar charts
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    # plot the category ratings chart
    c.execute("SELECT category, AVG(rating) FROM restaurants GROUP BY category ORDER BY AVG(rating) DESC")
    cat_data = c.fetchall()
    categories, ratings = zip(*cat_data)
    ax1.bar(categories, ratings, color='blue')
    ax1.set_xlabel('Category')
    ax1.set_ylabel('Average Rating')
    ax1.set_title('Highest Rated Restaurant Categories')

    # plot the building ratings chart
    c.execute("SELECT building, AVG(rating) FROM restaurants GROUP BY building ORDER BY AVG(rating) DESC")
    building_data = c.fetchall()
    buildings, ratings = zip(*building_data)
    ax2.bar(buildings, ratings, color='red')
    ax2.set_xlabel('Building Number')
    ax2.set_ylabel('Average Rating')
    ax2.set_title('Highest Rated Buildings')

    plt.tight_layout()
    plt.show()

    return highest_rating

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
