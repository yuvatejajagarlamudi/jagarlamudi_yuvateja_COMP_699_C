from django.contrib import admin
from .models import Ticket, RuleConfig


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "status", "priority_score", "resident", "assigned_staff", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("title", "description", "location")


@admin.register(RuleConfig)
class RuleConfigAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "base_score", "image_bonus", "urgent_keyword_bonus")
