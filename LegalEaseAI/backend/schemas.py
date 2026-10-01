from pydantic import BaseModel, field_validator


class DocumentRequest(BaseModel):
    document_type: str
    parties: str
    terms: str
    effective_date: str = ""

    @field_validator("document_type", "parties", "terms")
    @classmethod
    def validate_required_fields(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("This field is required.")

        return value

    @field_validator("effective_date")
    @classmethod
    def clean_effective_date(cls, value: str) -> str:
        return value.strip()


class DocumentResponse(BaseModel):
    document_type: str
    content: str