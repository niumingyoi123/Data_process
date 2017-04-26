def rpc_find_rough(user_locations,times_threshold,time_span):
    """
    Confirm the users' belong to the target_region
    :param user_locations: Users locations{deviceid:'deviceid' ,
     pos:'[{'timestamp:'timestamp','lat':'lat','lng':'lng'},]'}
    :param target_region: target region
    :return: new user location list
    """
    find_resident_rough = []
    for user_location in user_locations:
        appear_times = len(user_location['pos'])
        fisrt_time = user_location['pos'][0]['timestamp']
        last_time = user_locations['pos'][appear_times-1]['timestamp']
        if appear_times < times_threshold and last_time-fisrt_time < time_span:
            continue
        else:
            find_resident_rough.append(user_location)

    return find_resident_rough
