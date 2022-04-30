# 507Final

A program that access restaurant data from a Yelp API, organizes that data into a tree structure, and then asks users some questions about location, graphs, category, and price) until it provides a list of recommendations that meet the user options.

## Project code

* If users answer yes to ‘Get new data from Yelp?’, Yelp Fusion API will be applied. If users answer no, the cached data will be used.
* Required Packages:
```Pyhthon
import requests
import secrets
import pandas as pd
import matplotlib.pyplot as plt
```

## Data Structure

* I organized data into a tree structure, and stored it in a JSON file named restaurant_tree.json. 
* [Tree Screenshot](https://drive.google.com/file/d/1f0dgDH8j5PbbRuj3tHafWRlQg2mU63ma/view?usp=sharing)

## Demo Link

* [Demo Video](https://drive.google.com/file/d/1mr4vf7c042OTI_1SHDVEj2b67sRCCVom/view?usp=sharing)
