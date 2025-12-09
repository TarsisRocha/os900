# app/modules/cache_utils.py
import streamlit as st
from functools import wraps
from typing import Callable

def cached(ttl_seconds: int = 30):
    def deco(fn: Callable):
        @st.cache_data(ttl=ttl_seconds)
        def wrapped(*args, **kwargs):
            return fn(*args, **kwargs)
        return wrapped
    return deco
