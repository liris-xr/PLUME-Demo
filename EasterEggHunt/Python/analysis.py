import numpy as np
import pandas as pd
from plume_python.record import Record
from plume_python.samples.common.marker_pb2 import Marker
from plume_python.samples.unity.xritk.xr_base_interactable_pb2 import XRBaseInteractableHoverEnter, \
    XRBaseInteractableSelectEnter
from plume_python.utils.game_object import find_first_identifier_by_name, find_first_name_by_guid
from plume_python.utils.transform import compute_transform_time_series


def compute_select_stats(record: Record) -> list[tuple[str, int]]:
    selected_objects = {}
    for select_sample in record.get_samples_by_type(XRBaseInteractableSelectEnter):
        object_id = select_sample.payload.id.parent_id.game_object_id
        if object_id not in selected_objects:
            selected_objects[object_id] = 0
        selected_objects[object_id] += 1
    return sorted(selected_objects.items(), key=lambda x: x[1], reverse=True)


def compute_hover_stats(record: Record) -> list[tuple[str, int]]:
    hovered_objects = {}
    for hover_sample in record.get_samples_by_type(XRBaseInteractableHoverEnter):
        object_id = hover_sample.payload.id.parent_id.game_object_id
        if object_id not in hovered_objects:
            hovered_objects[object_id] = 0
        hovered_objects[object_id] += 1
    return sorted(hovered_objects.items(), key=lambda x: x[1], reverse=True)


def compute_teleport_count(record: Record) -> int:
    count = 0
    for select_sample in record.get_samples_by_type(XRBaseInteractableSelectEnter):
        game_object_guid = select_sample.payload.id.parent_id.game_object_id
        game_object_name = find_first_name_by_guid(record, game_object_guid)
        if game_object_name == "Teleportation Area":
            count += 1
    return count


def compute_room_visit_duration_stats(record: Record) -> list[tuple[str, float]]:
    marker_samples = record.get_samples_by_type(Marker)
    marker_enter_room = [s for s in marker_samples if s.payload.label.startswith("Enter Room")]
    marker_exit_room = [s for s in marker_samples if s.payload.label.startswith("Exit Room")]

    room_visit_duration = {}
    for enter_room in marker_enter_room:
        room_name = enter_room.payload.label.replace("Enter Room : ", "")
        enter_timestamp = enter_room.timestamp
        exit_room = next((s for s in marker_exit_room if s.timestamp > enter_timestamp), None)
        exit_timestamp = exit_room.timestamp if exit_room else record.last_timestamp
        if room_name not in room_visit_duration:
            room_visit_duration[room_name] = 0
        room_visit_duration[room_name] += (exit_timestamp - enter_timestamp) / 1000000000

    return sorted(room_visit_duration.items(), key=lambda x: x[1], reverse=True)


def compute_travelled_distance(game_object_name: str, record: Record, local_space: bool = False) -> float:
    distance = 0
    identifier = find_first_identifier_by_name(record, game_object_name)
    transform_time_series = compute_transform_time_series(record, identifier.transform_id)
    positions = [t.local_position if local_space else t.get_world_position() for t in transform_time_series]

    for i in range(len(positions) - 1):
        distance += np.linalg.norm(positions[i + 1] - positions[i])

    return distance


def compute_cumulated_egg(record: Record) -> (pd.DataFrame, pd.DataFrame):
    marker_samples = record.get_samples_by_type(Marker)
    last_timestamp = marker_samples[-1].timestamp // 1000000000

    collected_eggs = pd.DataFrame()
    collected_eggs["time"] = pd.to_timedelta(pd.Series(range(0, last_timestamp), dtype=float), unit="s")
    collected_eggs["value"] = [0] * last_timestamp

    for marker_sample in marker_samples:
        if marker_sample.payload.label == "Egg Pick Up":
            timestamp_seconds = marker_sample.timestamp // 1000000000
            collected_eggs.at[timestamp_seconds, "value"] += 1

    cumulated_eggs = pd.DataFrame()
    cumulated_eggs["time"] = collected_eggs["time"]
    cumulated_eggs["value"] = collected_eggs["value"].cumsum()

    collected_eggs_rolling = pd.DataFrame()
    collected_eggs_rolling["time"] = collected_eggs["time"]
    collected_eggs_rolling["value"] = collected_eggs.rolling('10s', on="time", min_periods=1)['value'].sum()

    return cumulated_eggs, collected_eggs_rolling
