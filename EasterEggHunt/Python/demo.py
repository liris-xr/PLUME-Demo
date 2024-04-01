from os import path

import plume_python as plm
from plotly import graph_objects as go

from analysis import *

# Parse Record
record_filepath = path.join(path.dirname(path.abspath(__file__)), "record.plm")
record = plm.parser.parse_record_from_file(record_filepath)

# Compute stats
select_stats = compute_select_stats(record)
hover_stats = compute_hover_stats(record)
n_teleport = compute_teleport_count(record)
room_visit_duration_stats = compute_room_visit_duration_stats(record)

travelled_distance_world = compute_travelled_distance("Main Camera", record)
travelled_distance_local = compute_travelled_distance("Main Camera", record, local_space=True)

cumulated_egg, collected_eggs_rolling = compute_cumulated_egg(record)

# Print stats
n = 10

# Print select stats
print("Number of distinct objects selected:", len(select_stats))
print("Most selected objects:")
for guid, count in select_stats[:n]:
    print(f"  - {find_first_name_by_guid(record, guid)}: {count} times")
print("  - ...\n")

# Print hover stats
print("Number of distinct objects hovered:", len(hover_stats))
print("Most hovered objects:")
for guid, count in hover_stats[:n]:
    print(f"  - {find_first_name_by_guid(record, guid)}: {count} times")
print("  - ...\n")

# Print room visit duration stats
print("Number of distinct rooms visited:", len(room_visit_duration_stats))
print("Room visit duration stats:")
for room, duration in room_visit_duration_stats:
    print(f"  - {room}: {duration:.2f} s")
print()

# Print travelled distance
print(f"Travelled distance (world space): {travelled_distance_world:.2f} m")
print(f"Travelled distance (local space): {travelled_distance_local:.2f} m")
print(f"Number of teleportation: {n_teleport}")

# Plot eggs collected stats
fig_cumulated_eggs = go.Figure()
fig_cumulated_eggs.add_trace(go.Scatter
                             (x=cumulated_egg['time'].dt.total_seconds(),
                              y=cumulated_egg['value'],
                              mode='lines', name='Eggs Collected'))
fig_cumulated_eggs.update_layout(title='Cumulated eggs over time', xaxis_title='Time (s)', yaxis_title='Eggs Count')
fig_cumulated_eggs.update_yaxes(tick0=0, dtick=1)
fig_cumulated_eggs.show()

fig_collected_eggs_rolling = go.Figure()
fig_collected_eggs_rolling.add_trace(go.Scatter(x=collected_eggs_rolling['time'].dt.total_seconds(),
                                                y=collected_eggs_rolling['value'],
                                                mode='lines', name='Eggs Collected (10s rolling sum)'))
fig_collected_eggs_rolling.update_layout(title='Eggs collected during the last 10s', xaxis_title='Time (s)',
                                         yaxis_title='Eggs Count')
fig_collected_eggs_rolling.update_yaxes(tick0=0, dtick=1)
fig_collected_eggs_rolling.show()
