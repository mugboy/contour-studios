from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel

from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.search import index


class HomePage(Page):
    body = RichTextField(blank=True)
    contact_email = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
        FieldPanel("contact_email"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # Add extra variables and return the updated context
        context["blog_entries"] = BlogPage.objects.child_of(self).live()
        context["services"] = ServicePage.objects.child_of(self).live()
        return context


class BlogPage(Page):

    # Database fields

    body = RichTextField()
    date = models.DateField("Post date")
    feed_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    # Search index configuration

    search_fields = Page.search_fields + [
        index.SearchField("body"),
        index.FilterField("date"),
    ]

    # Editor panels configuration

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("body"),
        InlinePanel("related_links", heading="Related links", label="Related link"),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        FieldPanel("feed_image"),
    ]

    # Parent page / subpage type rules

    parent_page_types = ["home.HomePage"]
    subpage_types = []


class BlogPageRelatedLink(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name="related_links")
    name = models.CharField(max_length=255)
    url = models.URLField()

    panels = [
        FieldPanel("name"),
        FieldPanel("url"),
    ]


class ServicePage(Page):
    description = RichTextField()
    template = "home/home_page.html"

    parent_page_types = ["home.HomePage"]

    content_panels = Page.content_panels + [
        FieldPanel("description"),
    ]
