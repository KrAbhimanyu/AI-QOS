"""Reusable UI components for AI-QOS."""
import streamlit as st
from datetime import datetime
from typing import Optional, List, Dict, Any
from utils.helpers import get_status_color, format_timestamp, truncate_text


def metric_card(
    label: str,
    value: str | int | float,
    delta: Optional[str] = None,
    icon: Optional[str] = None,
) -> None:
    """Display a metric card with optional delta and icon."""
    col1, col2 = st.columns([3, 1])
    with col1:
        st.metric(label=label, value=value, delta=delta)
    if icon:
        with col2:
            st.markdown(f"<div style='font-size: 2rem; text-align: right;'>{icon}</div>", unsafe_allow_html=True)


def status_badge(status: str, label: Optional[str] = None) -> None:
    """Display a status badge."""
    color = get_status_color(status)
    display_label = label or status.capitalize()
    st.markdown(f"""<span style=" display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 500; background: {color}20; color: {color}; border: 1px solid {color}40; "> <span style="width: 8px; height: 8px; border-radius: 50%; background: {color};"></span> {display_label} </span>""", unsafe_allow_html=True)


def mission_card(
    title: str,
    description: str,
    status: str,
    agent: str,
    created_at: Optional[datetime] = None,
    progress: Optional[float] = None,
) -> None:
    """Display a mission card component."""
    color = get_status_color(status)
    st.markdown(f"""<div style=" background: linear-gradient(135deg, #1E1E3F 0%, rgba(99, 102, 241, 0.1) 100%); border: 1px solid #334155; border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem; transition: all 0.3s ease; "> <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;"> <div> <h4 style="margin: 0; color: #F1F5F9; font-size: 1.1rem;">{title}</h4> <p style="margin: 0.5rem 0 0; color: #94A3B8; font-size: 0.875rem;">{description}</p> </div> <span style=" padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 500; background: {color}20; color: {color}; ">{status.capitalize()}</span> </div> <div style="display: flex; gap: 1.5rem; color: #94A3B8; font-size: 0.875rem;"> <span>🤖 {agent}</span> <span>📅 {format_timestamp(created_at)}</span> </div> {f'<div style="margin-top: 1rem; height: 4px; background: #334155; border-radius: 2px;"><div style="width: {progress}%; height: 100%; background: {color}; border-radius: 2px;"></div></div>' if progress is not None else ''} </div>""", unsafe_allow_html=True)


def agent_card(
    name: str,
    role: str,
    status: str,
    tasks_completed: int = 0,
    success_rate: float = 0.0,
) -> None:
    """Display an agent card component."""
    color = get_status_color(status)
    st.markdown(f"""<div style=" background: linear-gradient(135deg, #1E1E3F 0%, rgba(99, 102, 241, 0.05) 100%); border: 1px solid #334155; border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem; "> <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;"> <div style=" width: 48px; height: 48px; border-radius: 50%; background: linear-gradient(135deg, #6366F1, #8B5CF6); display: flex; align-items: center; justify-content: center; font-size: 1.5rem; ">🤖</div> <div> <h4 style="margin: 0; color: #F1F5F9;">{name}</h4> <p style="margin: 0; color: #94A3B8; font-size: 0.875rem;">{role}</p> </div> </div> <div style="display: flex; justify-content: space-between; align-items: center;"> <span style=" padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; background: {color}20; color: {color}; ">{status.capitalize()}</span> <div style="text-align: right;"> <p style="margin: 0; color: #F1F5F9; font-weight: 500;">{tasks_completed} tasks</p> <p style="margin: 0; color: #94A3B8; font-size: 0.75rem;">{success_rate}% success</p> </div> </div> </div>""", unsafe_allow_html=True)


def execution_card(
    execution_id: str,
    mission_name: str,
    status: str,
    started_at: Optional[datetime] = None,
    duration: Optional[str] = None,
) -> None:
    """Display an execution card component."""
    color = get_status_color(status)
    st.markdown(f"""<div style=" background: #1E1E3F; border: 1px solid #334155; border-radius: 12px; padding: 1rem 1.5rem; margin-bottom: 0.75rem; display: flex; justify-content: space-between; align-items: center; "> <div> <p style="margin: 0; color: #F1F5F9; font-weight: 500;">{mission_name}</p> <p style="margin: 0.25rem 0 0; color: #64748B; font-size: 0.75rem;">ID: {execution_id}</p> </div> <div style="text-align: right;"> <span style=" padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; background: {color}20; color: {color}; ">{status.capitalize()}</span> <p style="margin: 0.25rem 0 0; color: #64748B; font-size: 0.75rem;">{duration or format_timestamp(started_at)}</p> </div> </div>""", unsafe_allow_html=True)


def page_header(
    title: str,
    subtitle: Optional[str] = None,
    icon: Optional[str] = None,
    actions: Optional[List[str]] = None,
) -> None:
    """Display a page header with breadcrumb and actions."""
    if icon:
        st.markdown(f"<h1 style='font-size: 1.75rem; margin-bottom: 0.25rem;'> {icon} {title}</h1>", unsafe_allow_html=True)
    else:
        st.markdown(f"<h1 style='font-size: 1.75rem; margin-bottom: 0.25rem;'>{title}</h1>", unsafe_allow_html=True)
    
    if subtitle:
        st.markdown(f"<p style='color: #94A3B8; margin-top: 0;'>{subtitle}</p>", unsafe_allow_html=True)
    
    if actions:
        cols = st.columns(len(actions))
        for i, action in enumerate(actions):
            with cols[i]:
                st.button(action, use_container_width=True)


def search_bar(placeholder: str = "Search...") -> str:
    """Display a search bar and return the query."""
    return st.text_input("", placeholder=placeholder, label_visibility="collapsed")


def filter_dropdown(
    label: str,
    options: List[str],
    key: Optional[str] = None,
) -> Optional[str]:
    """Display a filter dropdown."""
    return st.selectbox(label, options, key=key)


def empty_state(
    icon: str,
    title: str,
    description: str,
    action_label: Optional[str] = None,
) -> None:
    """Display an empty state message."""
    st.markdown(f"""<div style="text-align: center; padding: 3rem;"> <div style="font-size: 4rem; margin-bottom: 1rem;">{icon}</div> <h3 style="color: #F1F5F9; margin-bottom: 0.5rem;">{title}</h3> <p style="color: #94A3B8; max-width: 400px; margin: 0 auto;">{description}</p> </div>""", unsafe_allow_html=True)
    if action_label:
        st.button(action_label, type="primary")
