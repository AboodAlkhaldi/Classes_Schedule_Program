from typing import Type, Dict, Any, Tuple
from sqlalchemy import Column, and_, or_
from sqlalchemy.orm import Query


def build_dynamic_filters(
    model: Type,
    filter_params: Dict[str, Any]
) -> list:
    """Build SQLAlchemy filters from dict"""
    filters = []
    
    for field_name, value in filter_params.items():
        if value is None:
            continue
        
        if not hasattr(model, field_name):
            continue
        
        column = getattr(model, field_name)
        
        if isinstance(value, dict):
            # Handle operators like {"gt": 10}, {"like": "%test%"}
            if "gt" in value:
                filters.append(column > value["gt"])
            elif "gte" in value:
                filters.append(column >= value["gte"])
            elif "lt" in value:
                filters.append(column < value["lt"])
            elif "lte" in value:
                filters.append(column <= value["lte"])
            elif "like" in value:
                filters.append(column.like(value["like"]))
            elif "ilike" in value:
                filters.append(column.ilike(value["ilike"]))
            elif "in" in value:
                filters.append(column.in_(value["in"]))
        elif isinstance(value, list):
            filters.append(column.in_(value))
        else:
            filters.append(column == value)
    
    return filters


def apply_pagination(
    query: Query,
    page: int = 1,
    page_size: int = 50
) -> Tuple[Query, Dict[str, int]]:
    """Apply pagination to query"""
    if page < 1:
        page = 1
    if page_size < 1:
        page_size = 50
    
    offset = (page - 1) * page_size
    paginated_query = query.offset(offset).limit(page_size)
    
    pagination_info = {
        "page": page,
        "page_size": page_size,
        "offset": offset
    }
    
    return paginated_query, pagination_info


def apply_sorting(
    query: Query,
    sort_by: str,
    sort_order: str = "asc"
) -> Query:
    """Apply sorting to query"""
    if not sort_by:
        return query
    
    # Handle multi-field sorting (e.g., "name,created_at")
    sort_fields = [s.strip() for s in sort_by.split(",")]
    
    for field in sort_fields:
        if hasattr(query.column_descriptions[0]['entity'], field):
            column = getattr(query.column_descriptions[0]['entity'], field)
            if sort_order.lower() == "desc":
                query = query.order_by(column.desc())
            else:
                query = query.order_by(column.asc())
    
    return query

