"""
Database Schema Utilities

Provides schema inspection and migration utilities.
"""
from typing import Dict, List, Any, Optional
from django.db import connection


def get_table_list() -> List[str]:
    """Get list of all tables"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        return [row[0] for row in cursor.fetchall()]


def get_table_columns(table_name: str) -> List[Dict[str, Any]]:
    """Get columns for a table"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                column_name,
                data_type,
                character_maximum_length,
                is_nullable,
                column_default
            FROM information_schema.columns
            WHERE table_name = %s
            ORDER BY ordinal_position
        """, [table_name])
        
        columns = []
        for row in cursor.fetchall():
            columns.append({
                'name': row[0],
                'type': row[1],
                'length': row[2],
                'nullable': row[3] == 'YES',
                'default': row[4]
            })
        return columns


def get_table_indexes(table_name: str) -> List[Dict[str, Any]]:
    """Get indexes for a table"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                i.relname as index_name,
                a.attname as column_name,
                ix.indisprimary as is_primary
            FROM pg_class t
            JOIN pg_index ix ON t.oid = ix.indrelid
            JOIN pg_class i ON i.oid = ix.indexrelid
            JOIN pg_attribute a ON a.attrelid = t.oid AND a.attnum = ANY(ix.indkey)
            WHERE t.relname = %s
        """, [table_name])
        
        indexes = []
        for row in cursor.fetchall():
            indexes.append({
                'name': row[0],
                'column': row[1],
                'primary': row[2]
            })
        return indexes


def get_foreign_keys(table_name: str) -> List[Dict[str, str]]:
    """Get foreign keys for a table"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                kcu.column_name,
                ccu.table_name AS ref_table,
                ccu.column_name AS ref_column
            FROM information_schema.table_constraints AS tc
            JOIN information_schema.key_column_usage AS kcu
                ON tc.constraint_name = kcu.constraint_name
            JOIN information_schema.constraint_column_usage AS ccu
                ON ccu.constraint_name = tc.constraint_name
            WHERE tc.table_name = %s
                AND tc.constraint_type = 'FOREIGN KEY'
        """, [table_name])
        
        fks = []
        for row in cursor.fetchall():
            fks.append({
                'column': row[0],
                'ref_table': row[1],
                'ref_column': row[2]
            })
        return fks


def get_table_size(table_name: str) -> Dict[str, int]:
    """Get table size"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                pg_size_pretty(pg_total_relation_size(%s)),
                pg_total_relation_size(%s) as bytes
        """, [table_name, table_name])
        
        row = cursor.fetchone()
        return {
            'pretty': row[0],
            'bytes': row[1]
        }


def table_exists(table_name: str) -> bool:
    """Check if table exists"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1
                FROM information_schema.tables
                WHERE table_name = %s
            )
        """, [table_name])
        return cursor.fetchone()[0]


def column_exists(table_name: str, column_name: str) -> bool:
    """Check if column exists"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1
                FROM information_schema.columns
                WHERE table_name = %s AND column_name = %s
            )
        """, [table_name, column_name])
        return cursor.fetchone()[0]


def get_database_info() -> Dict[str, Any]:
    """Get database information"""
    return {
        'vendor': connection.vendor,
        'version': connection.settings_dict.get('VERSION'),
        'name': connection.settings_dict.get('NAME'),
    }