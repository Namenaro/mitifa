from cogmap import *


def get_n_biggest_events(cogmap, n=None):
    events_list = list(cogmap.LUE_events.values())
    sorted_events_list = sorted(events_list, key=lambda event: event.mass, reverse=True)
    events_ids_list = [LUE_event.local_cogmap_id for LUE_event in sorted_events_list]
    if n is None:
        return events_ids_list

    if len(events_ids_list) < n:
        return events_ids_list

    return events_ids_list[:n]
