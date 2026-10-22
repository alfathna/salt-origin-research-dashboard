"""CSS tema visual minimalis & modern; tidak memengaruhi perhitungan penelitian."""
import streamlit as st


def inject_style():
    st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">

    <style>
    /* ============================================================
       Font Strategy: @font-face substitution — safest approach.
       Streamlit uses 'Source Sans Pro' as its UI font.
       We intercept that font name and redirect it to Plus Jakarta Sans.
       'Material Symbols Rounded' is a separate font-family name so
       it is 100% unaffected. We do NOT use !important on html/body
       so that icon spans with their own font-family can always win.
       ============================================================ */
    @font-face {
        font-family: 'Source Sans Pro';
        src: url('https://fonts.gstatic.com/s/plusjakartasans/v12/LDIbaomQNQcsA88c7O9yZ4KMCoOg4IA6-91aHEjcWuA_qU7NSg.ttf') format('truetype');
        font-weight: 300 400;
        font-style: normal;
        font-display: swap;
    }
    @font-face {
        font-family: 'Source Sans Pro';
        src: url('https://fonts.gstatic.com/s/plusjakartasans/v12/LDIbaomQNQcsA88c7O9yZ4KMCoOg4IA6-91aHEjcWuA_d0nNSg.ttf') format('truetype');
        font-weight: 600;
        font-style: normal;
        font-display: swap;
    }
    @font-face {
        font-family: 'Source Sans Pro';
        src: url('https://fonts.gstatic.com/s/plusjakartasans/v12/LDIbaomQNQcsA88c7O9yZ4KMCoOg4IA6-91aHEjcWuA_TknNSg.ttf') format('truetype');
        font-weight: 700;
        font-style: normal;
        font-display: swap;
    }
    @font-face {
        font-family: 'Source Sans Pro';
        src: url('https://fonts.gstatic.com/s/plusjakartasans/v12/LDIbaomQNQcsA88c7O9yZ4KMCoOg4IA6-91aHEjcWuA_KUnNSg.ttf') format('truetype');
        font-weight: 800;
        font-style: normal;
        font-display: swap;
    }

    /* Fallback for any element Streamlit doesn't give an explicit font.
       NO !important here — lets icon spans' own font-family win normally. */
    html, body {
        font-family: 'Plus Jakarta Sans', 'Source Sans Pro', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* ==========================================================================
       Layout
       ========================================================================== */
    .block-container {
        padding-top: 4.8rem !important;
        padding-bottom: 3.5rem !important;
        max-width: 1240px !important;
    }

    header[data-testid="stHeader"] {
        background: transparent !important;
        height: 3.5rem !important;
    }

    .stApp {
        background-color: #FAFCFD;
    }

    /* ==========================================================================
       Sidebar Aesthetics
       ========================================================================== */
    /* ==========================================================================
       Sidebar Aesthetics — Fixed Width, Aligned Monoline, & Cohesive Teal Theme
       ========================================================================== */
    /* 1. Lock sidebar width & prevent user resizing */
    section[data-testid="stSidebar"],
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
        transition: width 0.22s cubic-bezier(0.4, 0, 0.2, 1), min-width 0.22s cubic-bezier(0.4, 0, 0.2, 1), max-width 0.22s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    /* Fixed 244px width when expanded */
    section[data-testid="stSidebar"]:not([aria-expanded="false"]),
    [data-testid="stSidebar"]:not([aria-expanded="false"]) {
        width: 244px !important;
        min-width: 244px !important;
        max-width: 244px !important;
    }

    /* Fixed 68px width when collapsed */
    section[data-testid="stSidebar"][aria-expanded="false"],
    [data-testid="stSidebar"][aria-expanded="false"] {
        width: 68px !important;
        min-width: 68px !important;
        max-width: 68px !important;
        transform: none !important;
        margin-left: 0 !important;
        overflow: hidden !important;
        background: #F8FAFC !important;
        box-shadow: 2px 0 10px rgba(0, 0, 0, 0.04) !important;
    }

    /* Disable Streamlit manual drag resize handle completely */
    section[data-testid="stSidebar"] > div[style*="col-resize"],
    section[data-testid="stSidebar"] div[class*="StyledResizeHandle"],
    section[data-testid="stSidebar"] div[class*="ResizeHandle"],
    div[class*="e6f82ta3"],
    div[style*="cursor: col-resize"] {
        display: none !important;
        pointer-events: none !important;
        width: 0 !important;
        height: 0 !important;
        cursor: default !important;
    }

    /* Sidebar Content container */
    div[data-testid="stSidebarContent"],
    section[data-testid="stSidebar"] div[data-testid="stSidebarContent"],
    [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
        padding: 0 12px 1.5rem 12px !important;
        overflow-y: auto !important;
        scrollbar-width: none !important;
        -ms-overflow-style: none !important;
    }

    div[data-testid="stSidebarContent"]::-webkit-scrollbar,
    section[data-testid="stSidebar"]::-webkit-scrollbar,
    [data-testid="stSidebar"] *::-webkit-scrollbar {
        display: none !important;
        width: 0 !important;
        height: 0 !important;
    }

    /* 2. Header & Hamburger Button — FIX: Always visible & aligned flush left with menu items */
    /* Remove any logo spacer so button is not pushed inward */
    [data-testid="stSidebarHeader"] > div:first-child:not([data-testid="stSidebarCollapseButton"]),
    [data-testid="stSidebarHeader"] [data-testid="stLogoSpacer"],
    [data-testid="stSidebarHeader"] div[class*="StyledNoLogoSpacer"],
    [data-testid="stSidebarHeader"] div[class*="e6f82ta7"] {
        display: none !important;
        width: 0 !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        flex: none !important;
    }

    [data-testid="stSidebarHeader"] {
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        padding: 1.15rem 0 0.5rem 0 !important;
        min-height: auto !important;
        height: auto !important;
        background: transparent !important;
        width: 100% !important;
        box-sizing: border-box !important;
        margin: 0 !important;
    }

    /* FIX: Force visibility and remove any auto-margins pushing it to center/right */
    [data-testid="stSidebarCollapseButton"],
    section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"],
    div[data-testid="stSidebarCollapseButton"],
    div[class*="StyledCollapseSidebarButton"],
    div[class*="e6f82ta8"] {
        visibility: visible !important;
        opacity: 1 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Align Header Button with menu items: exactly 10px 14px padding */
    [data-testid="stSidebarCollapseButton"] button {
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        width: 100% !important;
        padding: 10px 14px !important;
        border-radius: 12px !important;
        background: transparent !important;
        border: none !important;
        cursor: pointer !important;
        transition: background 0.15s ease !important;
        margin: 0 !important;
        margin-left: 0 !important;
        box-sizing: border-box !important;
    }

    [data-testid="stSidebarCollapseButton"] button:hover {
        background: #F0FDFA !important;
    }

    /* Hide default Streamlit chevron */
    [data-testid="stSidebarCollapseButton"] button svg,
    [data-testid="stSidebarCollapseButton"] button span {
        display: none !important;
    }

    /* 3-line Hamburger Icon: 20px width, aligned with menu icons */
    [data-testid="stSidebarCollapseButton"] button::before {
        content: "" !important;
        display: inline-block !important;
        width: 20px !important;
        height: 20px !important;
        margin-right: 12px !important;
        flex-shrink: 0 !important;
        background-color: #0F172A !important;
        -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cline x1='3' y1='5' x2='21' y2='5'/%3E%3Cline x1='3' y1='12' x2='21' y2='12'/%3E%3Cline x1='3' y1='19' x2='21' y2='19'/%3E%3C/svg%3E") !important;
        mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cline x1='3' y1='5' x2='21' y2='5'/%3E%3Cline x1='3' y1='12' x2='21' y2='12'/%3E%3Cline x1='3' y1='19' x2='21' y2='19'/%3E%3C/svg%3E") !important;
        -webkit-mask-size: contain !important;
        mask-size: contain !important;
        -webkit-mask-repeat: no-repeat !important;
        mask-repeat: no-repeat !important;
        -webkit-mask-position: center !important;
        mask-position: center !important;
        transition: background-color 0.15s ease !important;
    }

    [data-testid="stSidebarCollapseButton"] button:hover::before {
        background-color: #0F766E !important;
    }

    /* Salt Origin Text: starts at exact same coordinate as menu texts */
    [data-testid="stSidebarCollapseButton"] button::after {
        content: "Salt Origin" !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        color: #0F172A !important;
        letter-spacing: -0.025em !important;
        line-height: 1 !important;
        white-space: nowrap !important;
        transition: color 0.15s ease !important;
    }

    [data-testid="stSidebarCollapseButton"] button:hover::after {
        color: #0F766E !important;
    }

    /* 3. Navigation Radio Group — Aligned with Header */
    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"],
    section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] {
        gap: 4px !important;
        display: flex !important;
        flex-direction: column !important;
        margin-top: 4px !important;
    }

    /* Radio Label: Exactly matching header button padding & geometry */
    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label,
    section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 10px 14px !important;
        border-radius: 12px !important;
        margin: 0 !important;
        cursor: pointer !important;
        transition: all 0.15s ease !important;
        display: flex !important;
        align-items: center !important;
        width: 100% !important;
        box-sizing: border-box !important;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label:hover,
    section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label:hover {
        background: #F0FDFA !important;
    }

    /* Hide standard radio dot completely */
    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child,
    section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child {
        position: absolute !important;
        opacity: 0 !important;
        width: 0 !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        pointer-events: none !important;
        overflow: hidden !important;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label p,
    section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label p {
        font-weight: 500 !important;
        font-size: 0.92rem !important;
        color: #334155 !important;
        margin: 0 !important;
        transition: color 0.15s ease !important;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label:hover p,
    section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label:hover p {
        color: #0F766E !important;
    }

    /* Base outline icon for navigation items: 20px width, aligned with hamburger */
    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label::before,
    section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label::before {
        content: "" !important;
        display: inline-block !important;
        width: 20px !important;
        height: 20px !important;
        margin-right: 12px !important;
        flex-shrink: 0 !important;
        background-color: #475569 !important;
        -webkit-mask-size: contain !important;
        mask-size: contain !important;
        -webkit-mask-repeat: no-repeat !important;
        mask-repeat: no-repeat !important;
        -webkit-mask-position: center !important;
        mask-position: center !important;
        transition: background-color 0.15s ease !important;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label:hover::before,
    section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label:hover::before {
        background-color: #0F766E !important;
    }

    /* 1. Overview — Minimalist House Outline */
    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label:nth-of-type(1)::before,
    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label:has(input[value*="Overview"])::before {
        -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z'/%3E%3Cpolyline points='9 22 9 12 15 12 15 22'/%3E%3C/svg%3E") !important;
        mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z'/%3E%3Cpolyline points='9 22 9 12 15 12 15 22'/%3E%3C/svg%3E") !important;
    }

    /* 2. Eksplorasi Data — Minimalist Chart/Analytics Outline */
    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label:nth-of-type(2)::before,
    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label:has(input[value*="Eksplorasi"])::before {
        -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cline x1='18' y1='20' x2='18' y2='10'/%3E%3Cline x1='12' y1='20' x2='12' y2='4'/%3E%3Cline x1='6' y1='20' x2='6' y2='14'/%3E%3Cline x1='3' y1='20' x2='21' y2='20'/%3E%3C/svg%3E") !important;
        mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cline x1='18' y1='20' x2='18' y2='10'/%3E%3Cline x1='12' y1='20' x2='12' y2='4'/%3E%3Cline x1='6' y1='20' x2='6' y2='14'/%3E%3Cline x1='3' y1='20' x2='21' y2='20'/%3E%3C/svg%3E") !important;
    }

    /* 3. Analisis Box-Cox — Minimalist Flask Outline */
    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label:nth-of-type(3)::before,
    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label:has(input[value*="Box-Cox"])::before {
        -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M10 2v7.31L4.1 19.34A1.5 1.5 0 0 0 5.4 22h13.2a1.5 1.5 0 0 0 1.3-2.66L14 9.31V2'/%3E%3Cpath d='M8.5 2h7M7 16h10'/%3E%3C/svg%3E") !important;
        mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M10 2v7.31L4.1 19.34A1.5 1.5 0 0 0 5.4 22h13.2a1.5 1.5 0 0 0 1.3-2.66L14 9.31V2'/%3E%3Cpath d='M8.5 2h7M7 16h10'/%3E%3C/svg%3E") !important;
    }

    /* 4. Evaluasi Model — Minimalist Check Circle Outline */
    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label:nth-of-type(4)::before,
    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label:has(input[value*="Evaluasi"])::before {
        -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='12' cy='12' r='9'/%3E%3Cpolyline points='9 12 11.5 14.5 15.5 9.5'/%3E%3C/svg%3E") !important;
        mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='12' cy='12' r='9'/%3E%3Cpolyline points='9 12 11.5 14.5 15.5 9.5'/%3E%3C/svg%3E") !important;
    }

    /* 5. Hasil Klasifikasi — Minimalist Drawer/Threads Outline */
    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label:nth-of-type(5)::before,
    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label:has(input[value*="Klasifikasi"])::before {
        -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Crect x='3' y='4' width='18' height='16' rx='2'/%3E%3Cline x1='8' y1='9' x2='16' y2='9'/%3E%3Cline x1='8' y1='13' x2='14' y2='13'/%3E%3C/svg%3E") !important;
        mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Crect x='3' y='4' width='18' height='16' rx='2'/%3E%3Cline x1='8' y1='9' x2='16' y2='9'/%3E%3Cline x1='8' y1='13' x2='14' y2='13'/%3E%3C/svg%3E") !important;
    }

    /* 4. Active State — Harmonized with App Teal Palette (#0F766E) */
    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked),
    section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) {
        background: linear-gradient(135deg, #0F766E 0%, #115E59 100%) !important;
        border: none !important;
        box-shadow: 0 4px 14px rgba(15, 118, 110, 0.24) !important;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) p,
    section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) p {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked)::before,
    section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked)::before {
        background-color: #FFFFFF !important;
    }

    /* ==========================================================================
       5. Collapsed Sidebar State: 68px Icon Rail with Centered Vertical Axis
       ========================================================================== */
    section[data-testid="stSidebar"][aria-expanded="false"] div[data-testid="stSidebarContent"] {
        padding: 0 12px 1.5rem 12px !important;
        width: 68px !important;
        max-width: 68px !important;
        box-sizing: border-box !important;
        overflow-x: hidden !important;
    }

    section[data-testid="stSidebar"][aria-expanded="false"] div[data-testid="stSidebarUserContent"],
    section[data-testid="stSidebar"][aria-expanded="false"] div[data-testid="stRadio"],
    section[data-testid="stSidebar"][aria-expanded="false"] div[role="radiogroup"] {
        padding: 0 !important;
        margin: 0 !important;
        width: 44px !important;
        max-width: 44px !important;
        box-sizing: border-box !important;
    }

    /* Hide text labels AND stMarkdownContainer in collapsed rail to prevent off-center shift */
    section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarCollapseButton"] button::after,
    section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stRadio"] div[role="radiogroup"] > label div[data-testid="stMarkdownContainer"],
    section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stRadio"] div[role="radiogroup"] > label [data-testid="stMarkdownContainer"],
    section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stRadio"] div[role="radiogroup"] > label p,
    section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stRadio"] div[role="radiogroup"] > label span {
        display: none !important;
        width: 0 !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Center Header Button on the 68px rail — matches exactly 44px content area */
    section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarHeader"] {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 1.15rem 0 0.5rem 0 !important;
        width: 100% !important;
        max-width: 44px !important;
        box-sizing: border-box !important;
        margin: 0 auto !important;
    }

    section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarCollapseButton"],
    section[data-testid="stSidebar"][aria-expanded="false"] div[class*="StyledCollapseSidebarButton"],
    section[data-testid="stSidebar"][aria-expanded="false"] div[class*="e6f82ta8"] {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 44px !important;
        min-width: 44px !important;
        max-width: 44px !important;
        height: 44px !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarCollapseButton"] button {
        width: 44px !important;
        min-width: 44px !important;
        max-width: 44px !important;
        height: 44px !important;
        padding: 0 !important;
        margin: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        border-radius: 12px !important;
        box-sizing: border-box !important;
    }

    section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarCollapseButton"] button::before {
        margin: 0 !important;
        margin-left: 0 !important;
        margin-right: 0 !important;
        width: 20px !important;
        height: 20px !important;
        flex-shrink: 0 !important;
    }

    /* Center all Nav Items on the 68px rail: exactly 44px width inside 44px content area */
    section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stRadio"] div[role="radiogroup"] > label {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 0 !important;
        width: 44px !important;
        min-width: 44px !important;
        max-width: 44px !important;
        height: 44px !important;
        margin: 4px 0 !important;
        border-radius: 12px !important;
        box-sizing: border-box !important;
    }

    /* Center the icon perfectly in the 44px box */
    section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stRadio"] div[role="radiogroup"] > label::before {
        margin: 0 !important;
        margin-right: 0 !important;
        margin-left: 0 !important;
        width: 20px !important;
        height: 20px !important;
        flex-shrink: 0 !important;
    }

    /* Active icon in collapsed rail: clean white pill with teal border & teal icon */
    section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) {
        background: #FFFFFF !important;
        border: 1.5px solid #0F766E !important;
        box-shadow: 0 3px 12px rgba(15, 118, 110, 0.18) !important;
    }

    section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked)::before {
        background-color: #0F766E !important;
    }

    /* Hide external floating expand button since the rail's internal button is perfectly aligned */
    button[data-testid="stExpandSidebarButton"],
    div[class*="StyledOpenSidebarButton"],
    div[class*="e1o8oa9v3"] {
        display: none !important;
        width: 0 !important;
        height: 0 !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }

    /* Push main container smoothly when rail is present */
    div[data-testid="stAppViewContainer"]:has(section[data-testid="stSidebar"][aria-expanded="false"]) .main {
        margin-left: 68px !important;
    }

    /* ==========================================================================
       Typography & Headers
       ========================================================================== */
    h1 {
        font-size: 2.1rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.035em !important;
        color: #0F172A !important;
        line-height: 1.22 !important;
        margin-bottom: 0.35rem !important;
    }

    h2 {
        font-size: 1.35rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.025em !important;
        color: #0F172A !important;
        margin-top: 1.75rem !important;
        margin-bottom: 0.65rem !important;
    }

    h3 {
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.015em !important;
        color: #1E293B !important;
        margin-top: 1.35rem !important;
        margin-bottom: 0.5rem !important;
    }

    h4 {
        font-size: 0.98rem !important;
        font-weight: 600 !important;
        letter-spacing: -0.01em !important;
        color: #334155 !important;
        margin-top: 1rem !important;
        margin-bottom: 0.4rem !important;
    }

    .salt-eyebrow {
        display: inline-flex !important;
        align-items: center !important;
        gap: 6px !important;
        padding: 5px 14px !important;
        background: rgba(15, 118, 110, 0.08) !important;
        color: #0F766E !important;
        font-size: 0.72rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
        border-radius: 9999px !important;
        border: 1px solid rgba(15, 118, 110, 0.16) !important;
        margin-top: 0.4rem !important;
        margin-bottom: 0.75rem !important;
        line-height: 1.4 !important;
        box-sizing: border-box !important;
    }

    .salt-lead {
        color: #475569;
        font-size: 1.02rem;
        line-height: 1.68;
        max-width: 960px;
        margin-bottom: 1.6rem;
    }

    /* Minimalist Highlight Callout */
    .salt-note {
        background: #F0FDF4;
        border: 1px solid #BBF7D0;
        border-left: 4px solid #0F766E;
        padding: 14px 18px;
        border-radius: 0 12px 12px 0;
        color: #14532D;
        line-height: 1.62;
        margin: 1.25rem 0 1.6rem;
        font-size: 0.92rem;
        box-shadow: 0 1px 3px rgba(15, 118, 110, 0.04);
    }

    .salt-footer {
        color: #94A3B8;
        font-size: 0.8rem;
        text-align: center;
        margin-top: 3.5rem;
        padding-top: 1.25rem;
        border-top: 1px solid #E2E8F0;
    }

    /* ==========================================================================
       Metrics Cards
       ========================================================================== */
    div[data-testid="stMetric"] {
        background: #FFFFFF;
        padding: 18px 20px 16px;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.03), 0 1px 2px rgba(15, 23, 42, 0.02);
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }

    div[data-testid="stMetric"]:hover {
        border-color: #CBD5E1;
        box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06);
        transform: translateY(-2px);
    }

    div[data-testid="stMetricLabel"] {
        color: #64748B !important;
        font-size: 0.78rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.03em !important;
        text-transform: uppercase;
    }

    div[data-testid="stMetricValue"] {
        color: #0F172A !important;
        font-size: 1.75rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.025em !important;
        margin-top: 4px;
    }

    /* ==========================================================================
       Form Controls (Selectbox, Multiselect, Inputs)
       ========================================================================== */
    div[data-testid="stSelectbox"] > div,
    div[data-testid="stMultiSelect"] > div,
    div[data-testid="stTextInput"] > div {
        border-radius: 10px !important;
        border: 1px solid #CBD5E1 !important;
        background: #FFFFFF !important;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.02) !important;
        transition: all 0.15s ease-in-out;
    }

    div[data-testid="stSelectbox"] label,
    div[data-testid="stMultiSelect"] label,
    div[data-testid="stTextInput"] label {
        font-weight: 600 !important;
        font-size: 0.84rem !important;
        color: #334155 !important;
        letter-spacing: -0.01em;
        margin-bottom: 4px;
    }

    /* Focus state */
    div[data-testid="stSelectbox"] > div:focus-within,
    div[data-testid="stMultiSelect"] > div:focus-within,
    div[data-testid="stTextInput"] > div:focus-within {
        border-color: #0F766E !important;
        box-shadow: 0 0 0 3px rgba(15, 118, 110, 0.12) !important;
    }

    /* Buttons */
    button[kind="secondary"],
    button[data-testid="baseButton-secondary"] {
        border-radius: 9px !important;
        border: 1px solid #CBD5E1 !important;
        background: #FFFFFF !important;
        color: #334155 !important;
        font-weight: 600 !important;
        font-size: 0.84rem !important;
        padding: 0.45rem 1rem !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.03) !important;
    }

    button[kind="secondary"]:hover,
    button[data-testid="baseButton-secondary"]:hover {
        border-color: #0F766E !important;
        color: #0F766E !important;
        background: #F0FDFA !important;
        box-shadow: 0 3px 10px rgba(15, 118, 110, 0.14) !important;
        transform: translateY(-1px) !important;
    }

    /* Expanders */
    div[data-testid="stExpander"] {
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        background: #FFFFFF !important;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.02) !important;
        margin: 0.85rem 0 !important;
        overflow: hidden;
    }

    div[data-testid="stExpander"] summary {
        /* Do NOT set font-family here — let it inherit from body naturally.
           The icon span inside summary has its own Material Symbols font set
           via Streamlit's own CSS class, which will override body inheritance. */
        font-weight: 600 !important;
        color: #1E293B !important;
        font-size: 0.9rem !important;
        padding: 0.85rem 1.1rem !important;
        background: #F8FAFC !important;
        border-radius: 11px !important;
        transition: background 0.15s ease, color 0.15s ease;
    }

    div[data-testid="stExpander"] summary:hover {
        background: #F1F5F9 !important;
        color: #0F766E !important;
    }

    /* DataFrames */
    div[data-testid="stDataFrame"] {
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        background: #FFFFFF !important;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.02) !important;
    }

    /* Captions */
    div[data-testid="stCaptionContainer"] {
        color: #64748B !important;
        font-size: 0.81rem !important;
        line-height: 1.55 !important;
        margin-top: 4px;
    }

    /* Divider */
    hr {
        border-color: #E8EDF2 !important;
        margin: 1.35rem 0 !important;
    }

    /* Alert Banners */
    div[data-testid="stAlert"] {
        border-radius: 11px !important;
        border-width: 1px !important;
        padding: 12px 18px !important;
        font-size: 0.9rem !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02) !important;
    }

    /* ==========================================================================
       CRITICAL: Restore Material Symbols icon font — placed LAST for cascade priority.
       Streamlit uses Material Symbols Rounded for all icons (expander arrows,
       selectbox chevrons, etc.). This rule ensures the icon font is NEVER lost
       regardless of any other font-family rules above.
       ========================================================================== */
    .material-symbols-rounded,
    [class*="material-symbols"] {
        font-family: 'Material Symbols Rounded' !important;
        font-weight: normal !important;
        font-style: normal !important;
        line-height: 1 !important;
        letter-spacing: normal !important;
        text-transform: none !important;
        white-space: nowrap !important;
        word-wrap: normal !important;
        -webkit-font-feature-settings: 'liga' !important;
        font-feature-settings: 'liga' !important;
        -webkit-font-smoothing: antialiased !important;
    }
    </style>
    """, unsafe_allow_html=True)
