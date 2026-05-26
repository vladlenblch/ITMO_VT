from recognizer.geometry import calculate_distance, calculate_angle

class FingerCounter:
    def __init__(self):
        self.finger_ids = {
            'thumb': {'tip': 4, 'ip': 3, 'mcp': 2, 'cmc': 1},
            'index': {'tip': 8, 'pip': 6, 'mcp': 5},
            'middle': {'tip': 12, 'pip': 10, 'mcp': 9},
            'ring': {'tip': 16, 'pip': 14, 'mcp': 13},
            'pinky': {'tip': 20, 'pip': 18, 'mcp': 17}
        }
        self.wrist_id = 0
    
    def detect(self, landmarks):
        fingers_up = 0
        wrist = landmarks[self.wrist_id]

        thumb_tip = landmarks[self.finger_ids['thumb']['tip']]
        thumb_ip = landmarks[self.finger_ids['thumb']['ip']]
        thumb_mcp = landmarks[self.finger_ids['thumb']['mcp']]
        thumb_cmc = landmarks[self.finger_ids['thumb']['cmc']]

        index_mcp = landmarks[self.finger_ids['index']['mcp']]

        thumb_mcp_angle = calculate_angle(thumb_cmc, thumb_mcp, thumb_ip)

        thumb_cmc_angle = calculate_angle(thumb_mcp, thumb_cmc, index_mcp)

        dist_thumb_tip_wrist = calculate_distance(thumb_tip, wrist)
        dist_index_mcp_wrist = calculate_distance(index_mcp, wrist)

        if (thumb_mcp_angle > 165 or thumb_cmc_angle > 30) and dist_thumb_tip_wrist > dist_index_mcp_wrist * 0.7:
            fingers_up += 1
        
        for finger_name in ['index', 'middle', 'ring', 'pinky']:
            tip_id = self.finger_ids[finger_name]['tip']
            pip_id = self.finger_ids[finger_name]['pip']
            mcp_id = self.finger_ids[finger_name]['mcp']
            
            tip = landmarks[tip_id]
            pip = landmarks[pip_id]
            mcp = landmarks[mcp_id]
            
            dist_tip_wrist = calculate_distance(tip, wrist)
            dist_pip_wrist = calculate_distance(pip, wrist)
            
            dist_mcp_wrist = calculate_distance(mcp, wrist)
            
            if dist_tip_wrist > dist_pip_wrist * 1.2 and dist_tip_wrist > dist_mcp_wrist:
                fingers_up += 1
        
        return fingers_up
    
    def reset(self):
        pass
