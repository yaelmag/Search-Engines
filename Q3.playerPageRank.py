# Yael Magid 209134956
import random
NUM_OF_ITER = 100000
PROB_FOR_LINK = 0.85


# teleport function
def choose_random_page(page_dict):
    return random.sample(page_dict.keys(), 1)[0]


# the algo' for finding the next page
def random_surfer(curr_page, page_dict):
    # add to the sum of visits 1 (later used for finding the importance)
    page_dict[curr_page]['countOfVisits'] +=1

    rand = random.random()
    # Means we shouldn't damp
    if rand < PROB_FOR_LINK and page_dict[curr_page]['outLinks']:
        # follow the link
        nextPage = random.sample(page_dict[curr_page]['outLinks'], 1)[0]
        return page_dict, nextPage
    # teleport
    nextPage = choose_random_page(page_dict)
    return page_dict, nextPage


# update the dict after 100000 iterations
def enter_importance(page_dict, output_dict):
    for url in page_dict:
        if url in output_dict.keys():
            (output_dict[url]).append(page_dict[url]['countOfVisits'] / NUM_OF_ITER)
        else:
            output_dict[url] = [page_dict[url]['countOfVisits'] / NUM_OF_ITER]
    return output_dict



# initialize the helper dict
def initialize_page_dict(listOfPairs):
    page_dict = dict()
    for l in listOfPairs:
        if not l[0] in page_dict:
            page_dict[l[0]] = {'countOfVisits': 0, 'outLinks': []}
        if not l[1] in page_dict:
            page_dict[l[1]] = {'countOfVisits': 0, 'outLinks': []}
        page_dict[l[0]]['outLinks'].append(l[1])

    return page_dict


# the main function
def playerPageRank(listOfPairs):
    # helper dictionary
    page_dict = initialize_page_dict(listOfPairs)
    output_dict = dict()

    # at first - choose randomly
    curr_page = choose_random_page(page_dict)

    # first 100000 iter
    for i in range(NUM_OF_ITER):
        page_dict, curr_page = random_surfer(curr_page, page_dict)

    # update the output_dict with the importance for every page after the first iterations
    output_dict = enter_importance(page_dict, output_dict)
    # initialize the dict
    page_dict = initialize_page_dict(listOfPairs)

    # # second 100000 iter
    for i in range(NUM_OF_ITER):
        page_dict, curr_page = random_surfer(curr_page, page_dict)

    # update the output_dict with the importance for every page after the second iterations
    output_dict = enter_importance(page_dict, output_dict)

    return output_dict