# Generated manually to fix invalid donation values

from django.db import migrations


def fix_invalid_donation_values(apps, schema_editor):
    """Fix any invalid donation values in the database using raw SQL"""
    db_alias = schema_editor.connection.alias
    
    # Use raw SQL to fix invalid values directly
    # Reset any desired_donation values that are problematic
    with schema_editor.connection.cursor() as cursor:
        # First, try to find and fix values that are too large or invalid
        # We'll reset them to 0 or cap at 1000000
        cursor.execute("""
            UPDATE core_registereddonor 
            SET desired_donation = CASE 
                WHEN CAST(desired_donation AS TEXT) = 'NaN' OR 
                     CAST(desired_donation AS TEXT) = 'Infinity' OR
                     CAST(desired_donation AS TEXT) = '-Infinity' OR
                     desired_donation > 1000000
                THEN 0
                ELSE desired_donation
            END
            WHERE desired_donation IS NOT NULL
        """)
        
        # Also fix total_donated and amount_pledged if they have issues
        cursor.execute("""
            UPDATE core_registereddonor 
            SET total_donated = CASE 
                WHEN CAST(total_donated AS TEXT) = 'NaN' OR 
                     CAST(total_donated AS TEXT) = 'Infinity' OR
                     CAST(total_donated AS TEXT) = '-Infinity'
                THEN 0
                ELSE total_donated
            END
            WHERE total_donated IS NOT NULL
        """)
        
        cursor.execute("""
            UPDATE core_registereddonor 
            SET amount_pledged = CASE 
                WHEN CAST(amount_pledged AS TEXT) = 'NaN' OR 
                     CAST(amount_pledged AS TEXT) = 'Infinity' OR
                     CAST(amount_pledged AS TEXT) = '-Infinity'
                THEN 0
                ELSE amount_pledged
            END
            WHERE amount_pledged IS NOT NULL
        """)


def reverse_fix(apps, schema_editor):
    """Reverse migration - no action needed"""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_registereddonor_amount_pledged_and_more'),
    ]

    operations = [
        migrations.RunPython(fix_invalid_donation_values, reverse_fix),
    ]

