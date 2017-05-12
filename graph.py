import networkx as nx
from networkx.algorithms import bipartite
import sys
sys.path.append('../')
from crawler.general import *
# import community.community_louvain as community
import pickle
import os

# u_list = read("../crawler/extracted_data/test_data")
# u_list_books = [u for u in u_list if len(u.userbooks) > 0]

def make_user_book_dict(user_list):
	""" Assigns a user ID corresponding to index in user_list to a user's list of book objects. """
	return {i: user_list[i] for i in range(len(user_list))}

def create_bipartite_graph(user_list):
	""" Given a list of user objects (each user with a list of book objects),
	this function will construct a bipartite graph of users and books. """
	b_graph = nx.Graph()
	b_graph.add_nodes_from(range(len(user_list)), bipartite = 0)
	for i in range(len(user_list)):
		book_list = user_list[i].userbooks
		b_graph.add_edges_from(zip([i] * len(book_list), [book.title for book in book_list]))
	for node in b_graph.nodes():
		if 'bipartite' not in b_graph.node[node]:
			b_graph.node[node]['bipartite'] = 1
	return b_graph

def find_weights(book_pair_weights, b_graph, user_dict, users, edge_scheme):
	""" Returns a dictionary mapping book-title pairs to edge weights.
	Argument for edge_scheme is 'min_max' or 'co_rating_len'. """
	# book_pair_weights = {}
	for user in users:
		if edge_scheme == "min_max":
			book_list = [b for b in user_dict[user].userbooks if b.rating > 0]
			for i in range(len(book_list)):
				for j in range(i, len(book_list)):
					book1 = book_list[i]
					book2 = book_list[j]
					if book1.goodreads_id > book2.goodreads_id:
						book1, book2 = book2, book1
					if (book1.title, book2.title) in book_pair_weights:
						book_pair_weights[(book1.title, book2.title)] += [min_max_ratio(book1.rating, book2.rating)]
					else:
						book_pair_weights[(book1.title, book2.title)] = [min_max_ratio(book1.rating, book2.rating)]
					print(book_pair_weights)
			book_pair_weights = {p:sum(book_pair_weights[p])/len(book_pair_weights[p]) for p in book_pair_weights}
		elif edge_scheme == "co_rating_len":
			book_list = [b for b in user_dict[user].userbooks]
			for i in range(len(book_list)):
				for j in range(i, len(book_list)):
					book1 = book_list[i]
					book2 = book_list[j]
					if book1.goodreads_id > book2.goodreads_id:
						book1, book2 = book2, book1
					if (book1.title, book2.title) in book_pair_weights:
						book_pair_weights[(book1.title, book2.title)] += 1
					else:
						book_pair_weights[(book1.title, book2.title)] = 1
		else:
			raise ValueError("Invalid Argument for edge_scheme:%s" % edge_scheme)
	return book_pair_weights


def find_weights_co_rating(book_pair_weights, b_graph, user_dict, users):
	for user in users:
		book_list = [b for b in user_dict[user].userbooks]
		for i in range(len(book_list)):
			for j in range(i, len(book_list)):
				book1 = book_list[i]
				book2 = book_list[j]
				if book1.goodreads_id > book2.goodreads_id:
					book1, book2 = book2, book1
				pair = (book1.title + "__" + str(book1.goodreads_id), book2.title + "__" + str(book2.goodreads_id))
				if pair in book_pair_weights:
					book_pair_weights[pair] += 1
				else:
					book_pair_weights[pair] = 1
	return book_pair_weights

# def project_graph(b_graph, book_weights_dict):
# 	proj_graph = nx.Graph()
# 	for pair in book_weights_dict:
# 		proj_graph.add_edge(*pair, weight = sum(book_weights_dict[pair])/len(book_weights_dict[pair]))
# 	return proj_graph


def min_max_ratio(r1, r2):
	return min(r1, r2)/max(r1, r2)

def main():
	# path = "../data/userlist_4/"
	path = "../crawler/extracted_data/test/"
	# can create bi_partite graphs separately?
	file_list = os.listdir(path)
	# file_list = ["../data/userlist_4/userlist_4_data_counter_70500.dat", "../data/userlist_4/userlist_4_data_counter_66200.dat"]
	# file_list = os.listdir("../data/data_small")
	# u_list = []
	weights_dict = {}
	for file_name in file_list:
		# u_list.extend(read("../" + file_name))
		# u_list = read("../data/userlist_4/" + file_name)
		# u_list = read(file_name)
		u_list = read(path + file_name)
		u_list_books = [u for u in u_list if len(u.userbooks) > 0]
		bi_graph = create_bipartite_graph(u_list_books)
		user_dict = make_user_book_dict(u_list_books)
		users, books = bipartite.sets(bi_graph)
		weights_dict = find_weights_co_rating(weights_dict, bi_graph, user_dict, users)
	with open('weights_dict_co_rating.pickle', 'wb') as f:
	    pickle.dump(weights_dict, f, protocol=2)
 

if __name__ == "__main__":
	main()

# bi_graph = create_bipartite_graph(u_list_books)
# user_dict = make_user_book_dict(u_list_books)
# weights_dict = find_weights(bi_graph, user_dict, "co_rating_len")
# # proj_graph = project_graph(bi_graph, weights_dict)
# with open('weights_dict.pickle', 'wb') as f:
#     pickle.dump(weights_dict, f, protocol=2)

# nx.edges(bi_graph, title)
# users, books = bipartite.sets(bi_graph)





