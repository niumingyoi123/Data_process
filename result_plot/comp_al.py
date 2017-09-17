import pickle
from user_traj.percision import get_rec_list
from .tradition_al import tradition_al

f_sorted = open('../user_traj/sorted_list_300_30_week_2', 'rb')
sorted_list = pickle.load(f_sorted)
get_rec_list(sorted_list)

