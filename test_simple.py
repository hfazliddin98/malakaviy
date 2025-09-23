#!/usr/bin/env python
"""
Simple test uchun Django server
"""
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'asosiy.settings')
    
    try:
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000'])
    except ImportError as exc:
        print(f"Django import error: {exc}")
        print("Django o'rnatilganligini tekshiring: pip install django")
    except Exception as e:
        print(f"Xatolik: {e}")