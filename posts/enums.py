from django.db import models
from django.utils.translation import gettext_lazy as _


class PostTypes(models.IntegerChoices):
    FULL_TIME = 1, _("Full time")
    PART_TIME = 2, _("Part time")
    TRAINEE = 3, _("Trainee")
    FREELANCER = 4, _("Freelancer")


class PostStatuses(models.IntegerChoices):
    DISAPPROVED = 0, _("DISAPPROVED")
    APPROVED = 1, _("APPROVED")
    UNPUBLISHED = 2, _("UNPUBLISHED")


class Periods(models.TextChoices):
    DAILY = "daily", _("Daily")
    WEEKLY = "weekly", _("Weekly")
    MONTHLY = "monthly", _("Monthly")
