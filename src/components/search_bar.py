"""SearchBar Component - Search and filter functionality."""

from typing import Any
import streamlit as st


def render_search_input(
    placeholder: str = "Search agents...",
    key: str = "search_input"
) -> str:
    """Render styled search input."""
    st.markdown("""
    <style>
    .search-container {
        position: relative;
        margin-bottom: 16px;
    }
    
    .search-input {
        width: 100%;
        padding: 12px 16px 12px 44px;
        background: rgba(51, 65, 85, 0.5);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 10px;
        color: #f8fafc;
        font-size: 14px;
        transition: all 0.2s ease;
    }
    
    .search-input:focus {
        outline: none;
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
        background: rgba(51, 65, 85, 0.7);
    }
    
    .search-input::placeholder {
        color: #64748b;
    }
    
    .search-icon {
        position: absolute;
        left: 14px;
        top: 50%;
        transform: translateY(-50%);
        color: #64748b;
        font-size: 16px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f'''
    <div class="search-container">
        <span class="search-icon">🔍</span>
        <input 
            type="text" 
            class="search-input" 
            id="search_{key}"
            placeholder="{placeholder}"
            onkeyup="handleSearch(this.value)"
        >
    </div>
    ''', unsafe_allow_html=True)
    
    # Use Streamlit's text_input as actual input
    query = st.text_input(
        "Search",
        placeholder=placeholder,
        label_visibility="collapsed",
        key=key,
    )
    
    return query


def render_filter_dropdown(
    options: list[str],
    selected: str,
    label: str,
    key: str
) -> str:
    """Render styled filter dropdown."""
    st.markdown(f"""
    <div style="
        padding: 8px 12px;
        background: rgba(51, 65, 85, 0.5);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 8px;
    ">
        <label style="
            font-size: 10px;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            display: block;
            margin-bottom: 4px;
        ">{label}</label>
    </div>
    """, unsafe_allow_html=True)
    
    return st.selectbox(
        label,
        options,
        index=options.index(selected) if selected in options else 0,
        label_visibility="collapsed",
        key=key,
    )


def render_quick_filters(
    categories: list[str],
    statuses: list[str],
    selected_category: str,
    selected_status: str
) -> tuple[str, str]:
    """Render quick filter chips."""
    st.markdown("""
    <style>
    .filter-chips {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-bottom: 16px;
    }
    
    .filter-chip {
        padding: 6px 14px;
        background: rgba(51, 65, 85, 0.5);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 20px;
        font-size: 12px;
        color: #94a3b8;
        cursor: pointer;
        transition: all 0.2s ease;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }
    
    .filter-chip:hover {
        background: rgba(99, 102, 241, 0.2);
        border-color: rgba(99, 102, 241, 0.3);
        color: #f8fafc;
    }
    
    .filter-chip.active {
        background: rgba(99, 102, 241, 0.3);
        border-color: #6366f1;
        color: #f8fafc;
    }
    
    .filter-chip .count {
        background: rgba(255, 255, 255, 0.1);
        padding: 2px 6px;
        border-radius: 10px;
        font-size: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Category chips
    st.markdown("#### Categories")
    chip_html = '<div class="filter-chips">'
    
    for cat in categories:
        active_class = "active" if cat == selected_category else ""
        chip_html += f'''
        <div class="filter-chip {active_class}" onclick="setCategory('{cat}')">
            {cat}
        </div>
        '''
    
    chip_html += '</div>'
    st.markdown(chip_html, unsafe_allow_html=True)
    
    # Use Streamlit selectbox for actual functionality
    col1, col2 = st.columns(2)
    
    with col1:
        selected_category = st.selectbox(
            "Category",
            categories,
            index=categories.index(selected_category) if selected_category in categories else 0,
            label_visibility="collapsed",
            key="filter_category",
        )
    
    with col2:
        status_options = ["All"] + statuses
        current_status = "All" if selected_status == "All" else selected_status
        selected_status = st.selectbox(
            "Status",
            status_options,
            index=status_options.index(current_status) if current_status in status_options else 0,
            label_visibility="collapsed",
            key="filter_status",
        )
    
    return selected_category, selected_status


def search_bar(
    agents: list[dict[str, Any]],
    categories: list[str],
    statuses: list[str]
) -> tuple[str, str, str]:
    """
    Render the complete search bar component.
    
    Returns:
        Tuple of (search_query, category, status)
    """
    st.markdown("### 🔍 Search & Filter")
    
    # Search input
    search_query = render_search_input(
        placeholder="Search by name, description, or mission...",
        key="agent_search"
    )
    
    # Quick filters
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        selected_category = st.selectbox(
            "Category",
            ["All"] + categories,
            label_visibility="visible",
            key="category_filter",
        )
    
    with col2:
        selected_status = st.selectbox(
            "Status",
            ["All"] + statuses,
            label_visibility="visible",
            key="status_filter",
        )
    
    with col3:
        st.markdown("<div style='padding-top: 20px;'></div>", unsafe_allow_html=True)
        if st.button("🔄 Reset", use_container_width=True):
            search_query = ""
            selected_category = "All"
            selected_status = "All"
            st.rerun()
    
    # Results count
    filtered_count = len(agents)
    total_count = filtered_count
    
    st.markdown(f"""
    <div style="
        padding: 10px 14px;
        background: rgba(99, 102, 241, 0.1);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 8px;
        margin-top: 16px;
    ">
        <span style="font-size: 13px; color: #94a3b8;">
            Showing <strong style="color: #f8fafc;">{filtered_count}</strong> 
            of <strong style="color: #f8fafc;">{total_count}</strong> agents
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    return search_query, selected_category, selected_status
