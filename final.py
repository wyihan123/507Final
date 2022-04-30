import requests
import json
import secrets
import pandas as pd
import matplotlib.pyplot as plt

def getData():
    location = input("Please enter the location\n")
    # location = "ann_arbor"
    header = {'authorization': "Bearer " + secrets.API_KEY}
    restaurants = []

    print("Getting data...")
    try:
        for offset in range(0, 1000, 50):  # Utilize offset and request limit to get 1000 results from Yelp API
            baseurl = "https://api.yelp.com/v3/businesses/search?location=" + location + "&limit=50&offset=" + str(
                offset)
            resp = requests.get(baseurl, headers=header)

            result = resp.json()  # Store the API returned result in to result in JSON format

            # print(result)

            for i in result['businesses']:
                category_list = []

                for c in i["categories"]:
                    category_list.append(c["alias"])

                try:
                    restaurants.append({"name": i["name"],
                                        "rating": i["rating"],
                                        "price": i["price"],
                                        "url": i["url"],
                                        "review_count": i["review_count"],
                                        "category": category_list,
                                        "address": i["location"]["display_address"]
                                        })
                except:  # Catch exception if there's no price data for this business
                    restaurants.append({"name": i["name"],
                                        "rating": i["rating"],
                                        "price": 'No Price',
                                        "url": i["url"],
                                        "review_count": i["review_count"],
                                        "category": category_list,
                                        "address": i["location"]["display_address"]
                                        })

        with open('restaurant_data.json', 'w') as data_file:
            data_file.write(json.dumps(restaurants))

    except:
        print("Error calling Yelp API, please try later.")
        exit(0)

    # print(json.dumps(restaurants, indent=2, sort_keys=False))
    # return restaurants


def load_from_file(file):  # Load JSON data from file
    with open(file, 'r') as data_file:
        restaurants = json.loads(data_file.readline())
    return restaurants


def visualize_data(tree):
    output_tree = {'noodles': {}, 'pizza': {}, 'salad': {}, 'sandwiches': {}, 'coffee': {}, 'seafood': {}}
    for food_category in tree:
        rating_total = 0.0
        count = 0
        for price_category in tree[food_category]:
            for item in tree[food_category][price_category]:
                rating_total += item['rating']
                count += 1
        try:
            rating_avg = rating_total / count
            output_tree[food_category]['rating_avg'] = rating_avg
        except:
            output_tree[food_category]['rating_avg'] = 0.0

        output_tree[food_category]['count'] = count

    # Plotting the data
    df = pd.DataFrame(output_tree).T
    plt.subplot(1, 2, 1)
    plt.title("Average Rating by Category")
    df['rating_avg'].plot.bar()
    plt.xlabel('Category')
    plt.ylabel('Average Rating')

    plt.subplot(1, 2, 2)
    df['count'].plot.bar()
    plt.title("Number of Restaurants by Category")
    plt.xlabel('Category')
    plt.ylabel('Number of Restaurants')

    plt.show()


# Construct a price tree using a given tree
def construct_price_tree(tree):
    price_tree = {'$': [], '$$': [], '$$$': [], '$$$$': [], 'No Price': []}
    for i in tree:
        if i["price"] == "$":
            price_tree['$'].append(i)
        elif i["price"] == "$$":
            price_tree['$$'].append(i)
        elif i["price"] == "$$$":
            price_tree['$$$'].append(i)
        elif i["price"] == "$$$$":
            price_tree['$$$$'].append(i)
        else:
            price_tree['No Price'].append(i)
    return price_tree


# Construct a completed restaurant tree
def construct_restaurant_tree(tree):
    category_tree = {'noodles': [], 'pizza': [], 'salad': [], 'sandwiches': [], 'coffee': [], 'seafood': []}
    for i in tree:
        if 'noodles' in i['category']:
            category_tree['noodles'].append(i)
        if 'pizza' in i['category']:
            category_tree['pizza'].append(i)
        if 'salad' in i['category']:
            category_tree['salad'].append(i)
        if 'sandwiches' in i['category']:
            category_tree['sandwiches'].append(i)
        if 'coffee' in i['category']:
            category_tree['coffee'].append(i)
        if 'seafood' in i['category']:
            category_tree['seafood'].append(i)

    for key in category_tree:
        category_tree[key] = construct_price_tree(category_tree[key])

    with open('restaurant_tree.json', 'w') as data_file:
        data_file.write(json.dumps(category_tree))

    # print(category_tree)
    return category_tree


if __name__ == '__main__':
    data_choice = str(input('Get new data from Yelp?\n1. Yes\n2. No\n'))
    if data_choice == '1' or data_choice == 'Yes':
        getData()   # Get data from Yelp API
    elif data_choice == 'exit':
        exit(0)

    data = load_from_file("restaurant_data.json")  # Read from cached data file
    restaurant_tree = construct_restaurant_tree(data)

    graph_choice = str(input('See restaurant data graphs?\n1. Yes\n2. No\n'))
    if graph_choice == '1' or graph_choice == 'Yes':
        visualize_data(restaurant_tree)
    elif graph_choice == 'exit':
        exit(0)

    # Print out menu to take user's selection
    choice = int(input("Enter the category\n1. Noodles\n2. Piazza\n3. Salad\n4. Sandwiches\n5. Coffee\n6. Seafood\n"))
    selection = 'exit'
    if choice == 1:
        selection = 'noodles'
    elif choice == 2:
        selection = 'pizza'
    elif choice == 3:
        selection = 'salad'
    elif choice == 4:
        selection = 'sandwiches'
    elif choice == 5:
        selection = 'coffee'
    elif choice == 6:
        selection = 'seafood'

    if selection == 'exit':
        exit(0)

    price = input("Enter the price of the restaurant using $ ($-$$$$)\n")
    while price not in ['$', '$$', '$$$', '$$$$']:
        price = input("Enter the price of the restaurant using $ ($-$$$$) or Type 'exit' to exit\n")
        if price == 'exit':
            exit(0)

    recommendation = restaurant_tree[selection][price]

    if len(recommendation) == 0:
        print('No recommendation based on your choice.')
    else:
        print("Here's a list of recommended restaurants based on your choice:\n")
        for i in recommendation:
            print('Name: ' + i['name'])
            print('Rating: ' + str(i['rating']))
            print('Price: ' + i['price'])
            print('URL: ' + i['url'])

            restaurant_address = ''
            for adds in i['address']:
                restaurant_address += adds + ', '

            restaurant_address = restaurant_address[:-2]

            print('Address: ' + restaurant_address + '\n')

    # print(json.dumps(restaurant_tree[selection][price], indent=2, sort_keys=False))
