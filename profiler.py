import time
import cProfile


def update_user(stage, program_start_time, snippet_start_time):

    curr_time = time.time()
    snippet_time = curr_time - snippet_start_time
    total_time = curr_time - program_start_time
    print('{} || Last Snippet Time: {} || Total Time: {}'.format(stage, round(snippet_time, 4), round(total_time, 4)))

