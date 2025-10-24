from django.db import models

from hub_insight.common.models import BaseModel, TypeChoices


class Job(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    help = models.CharField(max_length=255)
    script_filename = models.CharField(max_length=255, default="test.py")
    version = models.CharField(max_length=255, default="v1")
    response_type = models.CharField(max_length=255,
                                choices=TypeChoices.choices,
                                default=TypeChoices.string
                                )

    def __str__(self):
        return self.name



        

MAP_PYTHON_VAR = {
    int: TypeChoices.interger,
    str: TypeChoices.string,
    bool: TypeChoices.boolean,
    float: TypeChoices.float
}

class Variable(BaseModel):



    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='variables')
    name = models.CharField(max_length=255)
    var_type = models.CharField(max_length=255,
                                choices=TypeChoices.choices,
                                )
    default = models.CharField(max_length=255, null=True, default=None)

    def __str__(self):
        if self.default:
            return f"{self.name}:{self.var_type} = {self.default}"
        return f"{self.name}:{self.var_type}"
