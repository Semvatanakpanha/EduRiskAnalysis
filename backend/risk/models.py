from django.db import models


class RiskCheck(models.Model):
    student_name = models.CharField(max_length=100)
    score = models.IntegerField()
    attendance = models.IntegerField()
    risk_level = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_name} - {self.risk_level}"