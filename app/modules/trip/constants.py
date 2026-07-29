from enum import Enum


class TripStatus(str, Enum):
    DRAFT = "Draft"
    GENERATING = "Generating"
    GENERATED = "Generated"
    COMPLETED = "Completed"
    FAILED = "Failed"
    ARCHIVED = "Archived"