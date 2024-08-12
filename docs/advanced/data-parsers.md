# Create your own data parser

To convert your payloads and responses to your favourite format. A typical use case for this could be to deserialize
responses as python classes. It may be a good place to convert from snake case and camelCase (and viceversa).

In this library we have a basic example using NamedTuples: `NamedTupleParser`.

```python
from api_client_framework.protocols import Parser
from typing import Type, NamedTuple, Any


class NamedTupleParser(Parser):
    def __init__(self, model: Type[NamedTuple], **kwargs):
        self.model = model

    def to_dict(self, instance: NamedTuple) -> dict:
        return instance._asdict()

    def to_class(self, dictionary: dict) -> NamedTuple:
        return self.model(**dictionary)
```