from django.contrib import admin
from .models import Calculator, HomepageContent, Feature, Testimonial, SEOContent, GPAEntry

@admin.register(Calculator)
class CalculatorAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'featured', 'order', 'usage_count', 'created_at']
    list_filter = ['is_active', 'featured', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']
    list_editable = ['is_active', 'featured', 'order']

@admin.register(HomepageContent)
class HomepageContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'show_features', 'show_statistics', 'show_testimonials']
    list_filter = ['is_active', 'show_features', 'show_statistics', 'show_testimonials']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'subtitle', 'hero_text', 'about_section')
        }),
        ('Display Options', {
            'fields': ('show_features', 'show_statistics', 'show_testimonials', 'features_title')
        }),
        ('SEO Settings', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one homepage content
        return not HomepageContent.objects.exists()

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['title', 'description']
    ordering = ['order']
    list_editable = ['is_active', 'order']

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'occupation', 'rating', 'is_active', 'created_at']
    list_filter = ['rating', 'is_active', 'created_at']
    search_fields = ['name', 'occupation', 'message']
    ordering = ['-created_at']
    list_editable = ['is_active']

@admin.register(SEOContent)
class SEOContentAdmin(admin.ModelAdmin):
    list_display = ['page_name', 'title', 'is_active']
    list_filter = ['is_active']
    search_fields = ['page_name', 'title', 'description']
    
    fieldsets = (
        ('Page Information', {
            'fields': ('page_name', 'is_active')
        }),
        ('SEO Settings', {
            'fields': ('title', 'description', 'keywords')
        }),
        ('Additional Content', {
            'fields': ('additional_content',)
        }),
        ('Advanced', {
            'fields': ('schema_markup',),
            'classes': ('collapse',)
        }),
    )

@admin.register(GPAEntry)
class GPAEntryAdmin(admin.ModelAdmin):
    list_display = ['subject_name', 'grade', 'credit_hours', 'session_id', 'created_at']
    list_filter = ['grade', 'created_at']
    search_fields = ['subject_name', 'session_id']
    readonly_fields = ['created_at']
    ordering = ['-created_at']