from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class Calculator(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    detailed_description = models.TextField(blank=True, help_text="Detailed description for SEO")
    icon = models.CharField(max_length=10, help_text="Emoji or icon")
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=300, blank=True)
    featured = models.BooleanField(default=False, help_text="Show on homepage as featured")
    usage_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('calculators:calculator_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def increment_usage(self):
        self.usage_count += 1
        self.save(update_fields=['usage_count'])

class HomepageContent(models.Model):
    title = models.CharField(max_length=200, default="Calculator Hub")
    subtitle = models.CharField(max_length=300, default="Your one-stop destination for free online calculators")
    hero_text = models.TextField(blank=True)
    about_section = models.TextField(blank=True, help_text="About section content")
    features_title = models.CharField(max_length=200, default="Why Choose Our Calculators?")
    show_features = models.BooleanField(default=True)
    show_statistics = models.BooleanField(default=True)
    show_testimonials = models.BooleanField(default=False)
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=300, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Homepage Content"
        verbose_name_plural = "Homepage Content"

    def __str__(self):
        return self.title

class Feature(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    detailed_description = models.TextField(blank=True)
    icon = models.CharField(max_length=10)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100, blank=True)
    message = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.rating} stars"

class SEOContent(models.Model):
    page_name = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    keywords = models.CharField(max_length=300)
    additional_content = models.TextField(blank=True, help_text="Additional SEO content")
    schema_markup = models.JSONField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"SEO for {self.page_name}"

class GPAEntry(models.Model):
    GRADE_CHOICES = [
        ('A+', 'A+ (4.0)'),
        ('A', 'A (4.0)'),
        ('A-', 'A- (3.7)'),
        ('B+', 'B+ (3.3)'),
        ('B', 'B (3.0)'),
        ('B-', 'B- (2.7)'),
        ('C+', 'C+ (2.3)'),
        ('C', 'C (2.0)'),
        ('C-', 'C- (1.7)'),
        ('D+', 'D+ (1.3)'),
        ('D', 'D (1.0)'),
        ('F', 'F (0.0)'),
    ]

    subject_name = models.CharField(max_length=200)
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES)
    credit_hours = models.FloatField()
    session_id = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_grade_point(self):
        grade_points = {
            'A+': 4.0, 'A': 4.0, 'A-': 3.7,
            'B+': 3.3, 'B': 3.0, 'B-': 2.7,
            'C+': 2.3, 'C': 2.0, 'C-': 1.7,
            'D+': 1.3, 'D': 1.0, 'F': 0.0
        }
        return grade_points.get(self.grade, 0.0)