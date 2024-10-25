from typing import TypeVar, Generic, List, Dict, Any, Optional
from rail_forge import fetch_records
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

class QuerySet(Generic[T]):
    def __init__(self, model: T) -> None:
        self.model = model
        self.filters: Dict[str, Any] = {}
        self.excludes: Dict[str, Any] = {}
        self.annotations: Dict[str, Any] = {}
        self.ordering: List[str] = []
    
    def filter(self, **kwargs) -> "QuerySet[T]":
        self.filters.update(kwargs)
        return self
    
    def exclude(self, **kwargs) -> "QuerySet[T]":
        self.excludes.update(kwargs)
        return self
    
    def annotate(self, **kwargs) -> "QuerySet[T]":
        self.annotations.update(kwargs)
        return self
    
    def order_by(self, *args: str) -> "QuerySet[T]":
        self.ordering.extend(args)
        return self
    
    async def execute(self) -> List[T]:
        # Convert to rust compatible parameters
        filter_data = {k: v for k, v in self.filters.items()}
        exclude_data = {k: v for k, v in self.excludes.items()}
        order_data = self.ordering
        annotation_data = self.annotations

        result_data = await fetch_records(
            model=self.model.__name__, 
            filters=filter_data, 
            excludes=exclude_data, 
            ordering=order_data, 
            annotations=annotation_data
        )

        # Convert result data to model instances
        return [self.model.parse_obj(record) for record in result_data]