from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

from posts.enums import PostTypes, PostStatuses
from posts.utils import upload_to, custom_slugify


class AbstractModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Company(AbstractModel):
    slug = models.SlugField(
        verbose_name=_("Slug"),
        editable=False,
        unique=True,
        max_length=100,
        blank=True,
        null=True,
    )
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    email = models.EmailField(verbose_name=_("E-mail"))
    logo = models.ImageField(
        upload_to=upload_to, default="company-logo.png", verbose_name=_("Logo")
    )
    www = models.URLField(verbose_name=_("Web site"), unique=True)
    twitter = models.CharField(max_length=15, verbose_name=_("Twitter username"))
    linkedin = models.URLField(verbose_name=_("Linkedin url"))
    # TODO: What is the pub_date?
    pub_date = models.DateTimeField(blank=True, null=True, verbose_name=_("Pub date"))

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")

    def __str__(self):
        return f"{self.name}"

    def clean(self):
        self.slug = custom_slugify(self.name)


class Tag(AbstractModel):
    name = models.CharField(max_length=50, verbose_name=_("Name"))
    slug = models.SlugField(
        verbose_name=_("Slug"),
        editable=False,
        unique=True,
        max_length=50,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.name}"

    def clean(self):
        self.slug = custom_slugify(self.name)


class Post(AbstractModel):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, verbose_name=_("Company")
    )
    slug = models.SlugField(
        verbose_name=_("Slug"),
        editable=False,
        unique=True,
        max_length=200,
        blank=True,
        null=True,
    )
    tags = models.ManyToManyField(Tag, verbose_name=_("Tags"))
    position = models.CharField(max_length=101, verbose_name=_("Position"))
    description = models.TextField(verbose_name=_("Description"), max_length=100000)
    apply_url = models.URLField(null=True, blank=True, verbose_name=_("Apply url"))
    apply_email = models.EmailField(
        null=True, blank=True, verbose_name=_("Apply e-mail")
    )
    location = models.CharField(max_length=200, verbose_name=_("Location"))
    type = models.PositiveSmallIntegerField(
        choices=PostTypes.choices, default=PostTypes.FULL_TIME, verbose_name=_("Type")
    )
    status = models.PositiveSmallIntegerField(
        choices=PostStatuses.choices,
        default=PostStatuses.DISAPPROVED,
        verbose_name=_("Status"),
    )
    is_featured = models.BooleanField(verbose_name=_("Is featured?"), default=False)
    activation_code = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name=_("Activation code"),
        editable=False,
        unique=True,
    )
    renewal_code = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name=_("Renewal code"),
        editable=False,
        unique=True,
    )
    # TODO: I don't see notes on kodilan.com. What is this?
    notes = models.TextField(
        null=True, blank=True, max_length=1000, verbose_name=_("Notes")
    )
    pub_date = models.DateTimeField(
        null=True, blank=True, verbose_name=_("Pub date"), editable=False
    )

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ("-pub_date",)

    def __str__(self):
        return f"{self.company.name} > {self.position}"

    def clean(self):
        position = custom_slugify(self.position)
        self.slug = f"{self.company.slug}-{position}"

        if not self.renewal_code:
            self.renewal_code = get_random_string(length=50)
        if not self.activation_code:
            self.activation_code = get_random_string(length=50)

        if not self.pub_date and self.status == PostStatuses.APPROVED.value:
            self.pub_date = timezone.now()
