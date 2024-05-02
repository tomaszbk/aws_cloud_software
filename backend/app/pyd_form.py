from fastapi import Form
from sqlmodel import SQLModel


def as_form(cls: SQLModel):
    import inspect
    from typing import Annotated

    new_params = [
        inspect.Parameter(
            field_name,
            inspect.Parameter.POSITIONAL_ONLY,
            default=model_field.default,
            annotation=Annotated[model_field.annotation, *model_field.metadata, Form()],
        )
        for field_name, model_field in cls.model_fields.items()
        if field_name != "id"
    ]
    cls2 = cls
    cls2.__signature__ = cls.__signature__.replace(parameters=new_params)
    try:
        cls2.model_fields.pop("id")
    except:
        pass
    return cls2
