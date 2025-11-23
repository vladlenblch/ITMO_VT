import json
from dataclasses import asdict, dataclass
from typing import Any, Optional

from dataclasses_json import dataclass_json
from kafka import KafkaConsumer, KafkaProducer

from state import State

@dataclass_json
@dataclass
class AgentInput:
    hits_last_10: int
    current_radius: float

    @classmethod
    def from_state(cls, state: State) -> "AgentInput":
        return cls(
            hits_last_10=state.hits_last_10,
            current_radius=state.current_radius,
        )

    def to_state(self) -> State:
        return State(
            hits_last_10=self.hits_last_10,
            current_radius=self.current_radius,
        )

@dataclass_json
@dataclass
class AgentOutput:
    action_index: int
    action_label: str
    new_radius: Optional[float] = None
    reward: Optional[float] = None

class KafkaIO:
    def __init__(
        self,
        brokers: list[str],
        input_topic: str,
        output_topic: str,
        group_id: str = "rl-agent",
    ) -> None:
        self.input_topic = input_topic
        self.output_topic = output_topic
        self.consumer = KafkaConsumer(
            input_topic,
            bootstrap_servers=brokers,
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            auto_offset_reset="latest",
            enable_auto_commit=True,
            group_id=group_id,
        )
        self.producer = KafkaProducer(
            bootstrap_servers=brokers,
            value_serializer=lambda m: json.dumps(m).encode("utf-8"),
        )

    def poll_state(self, timeout_ms: int = 5000) -> Optional[State]:
        msg = self.consumer.poll(timeout_ms=timeout_ms, max_records=1)
        if not msg:
            return None
        _, batch = next(iter(msg.items()))
        record = batch[0]
        raw = record.value
        if isinstance(raw, dict):
            payload = AgentInput(**raw)
        else:
            payload = AgentInput.schema().loads(raw)
        return payload.to_state()

    def send_action(self, output: AgentOutput) -> None:
        payload: Any = output.to_dict() if hasattr(output, "to_dict") else asdict(output)
        self.producer.send(self.output_topic, payload)
        self.producer.flush()
