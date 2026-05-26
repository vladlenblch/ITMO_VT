from recognizer.geometry import calculate_distance, calculate_angle

FINGER_IDS = {
    "thumb": {"tip": 4, "ip": 3, "mcp": 2, "cmc": 1},
    "index": {"tip": 8, "pip": 6, "mcp": 5},
    "middle": {"tip": 12, "pip": 10, "mcp": 9},
    "ring": {"tip": 16, "pip": 14, "mcp": 13},
    "pinky": {"tip": 20, "pip": 18, "mcp": 17},
}
WRIST_ID = 0

def is_finger_up(landmarks, finger_name):
    wrist = landmarks[WRIST_ID]

    tip_id = FINGER_IDS[finger_name]["tip"]
    pip_id = FINGER_IDS[finger_name]["pip"]
    mcp_id = FINGER_IDS[finger_name]["mcp"]

    tip = landmarks[tip_id]
    pip = landmarks[pip_id]
    mcp = landmarks[mcp_id]

    dist_tip_wrist = calculate_distance(tip, wrist)
    dist_pip_wrist = calculate_distance(pip, wrist)
    dist_mcp_wrist = calculate_distance(mcp, wrist)

    return dist_tip_wrist > dist_pip_wrist * 1.2 and dist_tip_wrist > dist_mcp_wrist

def is_thumb_up(landmarks):
    wrist = landmarks[WRIST_ID]

    thumb_tip = landmarks[FINGER_IDS["thumb"]["tip"]]
    thumb_ip = landmarks[FINGER_IDS["thumb"]["ip"]]
    thumb_mcp = landmarks[FINGER_IDS["thumb"]["mcp"]]
    thumb_cmc = landmarks[FINGER_IDS["thumb"]["cmc"]]
    index_mcp = landmarks[FINGER_IDS["index"]["mcp"]]

    thumb_mcp_angle = calculate_angle(thumb_cmc, thumb_mcp, thumb_ip)
    thumb_cmc_angle = calculate_angle(thumb_mcp, thumb_cmc, index_mcp)

    dist_thumb_tip_wrist = calculate_distance(thumb_tip, wrist)
    dist_index_mcp_wrist = calculate_distance(index_mcp, wrist)

    return (
        (thumb_mcp_angle > 165 or thumb_cmc_angle > 30)
        and dist_thumb_tip_wrist > dist_index_mcp_wrist * 0.7
    )

def is_draw_hand(landmarks):
    return (
        is_finger_up(landmarks, "index")
        and not is_finger_up(landmarks, "middle")
        and not is_finger_up(landmarks, "ring")
        and not is_finger_up(landmarks, "pinky")
    )

def is_open_palm(landmarks):
    return (
        is_thumb_up(landmarks)
        and is_finger_up(landmarks, "index")
        and is_finger_up(landmarks, "middle")
        and is_finger_up(landmarks, "ring")
        and is_finger_up(landmarks, "pinky")
    )

def is_fist(landmarks):
    return (
        not is_thumb_up(landmarks)
        and not is_finger_up(landmarks, "index")
        and not is_finger_up(landmarks, "middle")
        and not is_finger_up(landmarks, "ring")
        and not is_finger_up(landmarks, "pinky")
    )

def is_rock_hand(landmarks):
    return (
        is_finger_up(landmarks, "index")
        and not is_finger_up(landmarks, "middle")
        and not is_finger_up(landmarks, "ring")
        and is_finger_up(landmarks, "pinky")
    )

def is_exit_hand(landmarks):
    return (
        not is_finger_up(landmarks, "index")
        and is_finger_up(landmarks, "middle")
        and not is_finger_up(landmarks, "ring")
        and not is_finger_up(landmarks, "pinky")
    )
