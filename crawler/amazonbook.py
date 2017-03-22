class AmazonBook:
    def __init__(self, abook):
        """
        Makes a amazon book from a book object fetched from the amazon api.
        (Note that we cannot save the fetched book directly because it cannot be pickled.)
        :param abook: book from api
        """

        self.reviews = abook.reviews
        self.nodes = abook.browse_nodes

        self.asin = abook.asin
        self.languages = abook.languages

        if abook.sales_rank is not None:
            self.sales_rank = int(abook.sales_rank)
        else:
            self.sales_rank = None

        # Make genres into list of strings
        self.genres = [n.name for n in self.nodes]
        genre_strings = []
        for g in self.genres:
            genre_strings.append(g.__str__())
        self.genres = genre_strings

#
# # Attributes of abook
# """"
# ['parsed_response', 'aws_associate_tag', 'api', 'parent', 'region', '__module__', '__doc__', '__init__', '__str__',
#  'price_and_currency', 'offer_id', 'asin', 'sales_rank', 'offer_url', 'author', 'authors', 'creators', 'publisher',
#  'label', 'manufacturer', 'brand', 'isbn', 'eisbn', 'binding', 'pages', 'publication_date', 'release_date', 'edition',
#  'large_image_url', 'medium_image_url', 'small_image_url', 'tiny_image_url', 'reviews', 'ean', 'upc', 'color', 'sku',
#  'mpn', 'model', 'part_number', 'title', 'editorial_review', 'editorial_reviews', 'languages', 'features', 'list_price',
#  'get_attribute', 'get_attribute_details', 'get_attributes', 'parent_asin', 'get_parent', 'browse_nodes', 'images',
#  'genre', 'actors', 'directors', 'is_adult', 'product_group', 'product_type_name', 'formatted_price', 'running_time',
#  'studio', 'is_preorder', 'availability', 'availability_type', 'availability_min_hours', 'availability_max_hours',
#  'detail_page_url', 'to_string', '_safe_get_element', '_safe_get_element_text', '_safe_get_element_date', '__dict__',
#  '__weakref__', '__repr__', '__hash__', '__getattribute__', '__setattr__', '__delattr__', '__lt__', '__le__', '__eq__',
#  '__ne__', '__gt__', '__ge__', '__new__', '__reduce_ex__', '__reduce__', '__subclasshook__', '__init_subclass__',
#  '__format__', '__sizeof__', '__dir__', '__class__']
#
# """
