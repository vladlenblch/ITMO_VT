from agent import RLAgent
from kafka_io import AgentOutput, KafkaIO
from state import State
from reward import compute_reward, ACTIONS

def handle_state(agent: RLAgent, state: State) -> AgentOutput:
    action_index, action = agent.select_action(state)
    proposed_radius = state.current_radius + action.radius_delta * 1

    reward = compute_reward(state, ACTIONS[action_index])
    next_state = State(
        hits_last_10=state.hits_last_10,
        current_radius=proposed_radius,
    )
    agent.update(state, action_index, reward, next_state)

    return AgentOutput(
        action_index=action_index,
        action_label=action.label,
        new_radius=proposed_radius,
        reward=reward,
    )

def main() -> None:
    agent = RLAgent()
    io = KafkaIO(["localhost:9092"], "rl_state_in", "rl_action_out")

    while True:
        state = io.poll_state()
        if state is None:
            continue
        output = handle_state(agent, state)
        io.send_action(output)

if __name__ == "__main__":
    main()
