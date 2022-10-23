from pydantic import BaseModel, Field


class AnnouncementContent(BaseModel):
    matches: dict = Field(title='Next games')


class StatsContent(BaseModel):
    stats: dict = Field(title='User stats')

