from pydantic import BaseModel


class BreakdownItem(BaseModel):
    label: str
    count: int
    percentage: float = 0.0


class TimelinePoint(BaseModel):
    date: str
    count: int


class CompanyActivity(BaseModel):
    company: str
    month: str
    count: int


class AnalyticsOverview(BaseModel):
    total_instances: int
    instances_this_week: int
    total_companies: int
    total_people_following: int
    sources_active: int


class IndustryBreakdown(BaseModel):
    items: list[BreakdownItem]


class DomainBreakdown(BaseModel):
    items: list[BreakdownItem]


class SourceBreakdown(BaseModel):
    items: list[BreakdownItem]


class TimelineData(BaseModel):
    points: list[TimelinePoint]


class CompanyActivityData(BaseModel):
    items: list[CompanyActivity]
